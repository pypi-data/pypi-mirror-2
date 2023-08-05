# Copyright (c) 2010 OpenStack, LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import errno
import logging
import os
import signal
import socket
import sys
import time
from random import random, shuffle

from eventlet import spawn, patcher, Timeout

from swift.container.server import DATADIR
from swift.common.bufferedhttp import http_connect
from swift.common.db import ContainerBroker
from swift.common.exceptions import ConnectionTimeout
from swift.common.ring import Ring
from swift.common.utils import get_logger, whataremyips


class ContainerUpdater(object):
    """Update container information in account listings."""

    def __init__(self, server_conf, updater_conf):
        self.logger = get_logger(updater_conf, 'container-updater')
        self.devices = server_conf.get('devices', '/srv/node')
        self.mount_check = server_conf.get('mount_check', 'true').lower() in \
                              ('true', 't', '1', 'on', 'yes', 'y')
        swift_dir = server_conf.get('swift_dir', '/etc/swift')
        self.interval = int(updater_conf.get('interval', 300))
        self.account_ring_path = os.path.join(swift_dir, 'account.ring.gz')
        self.account_ring = None
        self.concurrency = int(updater_conf.get('concurrency', 4))
        self.slowdown = float(updater_conf.get('slowdown', 0.01))
        self.node_timeout = int(updater_conf.get('node_timeout', 3))
        self.conn_timeout = float(updater_conf.get('conn_timeout', 0.5))
        self.no_changes = 0
        self.successes = 0
        self.failures = 0

    def get_account_ring(self):
        """Get the account ring.  Load it if it hasn't been yet."""
        if not self.account_ring:
            self.logger.debug(
                'Loading account ring from %s' % self.account_ring_path)
            self.account_ring = Ring(self.account_ring_path)
        return self.account_ring

    def get_paths(self):
        """
        Get paths to all of the partitions on each drive to be processed.

        :returns: a list of paths
        """
        paths = []
        ips = whataremyips()
        for device in os.listdir(self.devices):
            dev_path = os.path.join(self.devices, device)
            if self.mount_check and not os.path.ismount(dev_path):
                self.logger.warn('%s is not mounted' % device)
                continue
            con_path = os.path.join(dev_path, DATADIR)
            if not os.path.exists(con_path):
                continue
            for partition in os.listdir(con_path):
                paths.append(os.path.join(con_path, partition))
        shuffle(paths)
        return paths

    def update_forever(self):   # pragma: no cover
        """
        Run the updator continuously.
        """
        time.sleep(random() * self.interval)
        while True:
            self.logger.info('Begin container update sweep')
            begin = time.time()
            pids = []
            # read from account ring to ensure it's fresh
            self.get_account_ring().get_nodes('')
            for path in self.get_paths():
                while len(pids) >= self.concurrency:
                    pids.remove(os.wait()[0])
                pid = os.fork()
                if pid:
                    pids.append(pid)
                else:
                    signal.signal(signal.SIGTERM, signal.SIG_DFL)
                    patcher.monkey_patch(all=False, socket=True)
                    self.no_changes = 0
                    self.successes = 0
                    self.failures = 0
                    forkbegin = time.time()
                    self.container_sweep(path)
                    elapsed = time.time() - forkbegin
                    self.logger.debug(
                        'Container update sweep of %s completed: '
                        '%.02fs, %s successes, %s failures, %s with no changes'
                        % (path, elapsed, self.successes, self.failures,
                           self.no_changes))
                    sys.exit()
            while pids:
                pids.remove(os.wait()[0])
            elapsed = time.time() - begin
            self.logger.info('Container update sweep completed: %.02fs' %
                             elapsed)
            if elapsed < self.interval:
                time.sleep(self.interval - elapsed)

    def update_once_single_threaded(self):
        """
        Run the updater once.
        """
        patcher.monkey_patch(all=False, socket=True)
        self.logger.info('Begin container update single threaded sweep')
        begin = time.time()
        self.no_changes = 0
        self.successes = 0
        self.failures = 0
        for path in self.get_paths():
            self.container_sweep(path)
        elapsed = time.time() - begin
        self.logger.info('Container update single threaded sweep completed: '
            '%.02fs, %s successes, %s failures, %s with no changes' %
            (elapsed, self.successes, self.failures, self.no_changes))

    def container_sweep(self, path):
        """
        Walk the path looking for container DBs and process them.

        :param path: path to walk
        """
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith('.db'):
                    self.process_container(os.path.join(root, file))
                    time.sleep(self.slowdown)

    def process_container(self, dbfile):
        """
        Process a container, and update the information in the account.

        :param dbfile: container DB to process
        """
        broker = ContainerBroker(dbfile, logger=self.logger)
        info = broker.get_info()
        # Don't send updates if the container was auto-created since it
        # definitely doesn't have up to date statistics.
        if float(info['put_timestamp']) <= 0:
            return
        if info['put_timestamp'] > info['reported_put_timestamp'] or \
                info['delete_timestamp'] > info['reported_delete_timestamp'] \
                or info['object_count'] != info['reported_object_count'] or \
                info['bytes_used'] != info['reported_bytes_used']:
            container = '/%s/%s' % (info['account'], info['container'])
            part, nodes = self.get_account_ring().get_nodes(info['account'])
            events = [spawn(self.container_report, node, part, container,
                            info['put_timestamp'], info['delete_timestamp'],
                            info['object_count'], info['bytes_used'])
                      for node in nodes]
            successes = 0
            failures = 0
            for event in events:
                if 200 <= event.wait() < 300:
                    successes += 1
                else:
                    failures += 1
            if successes > failures:
                self.successes += 1
                self.logger.debug(
                    'Update report sent for %s %s' % (container, dbfile))
                broker.reported(info['put_timestamp'],
                                info['delete_timestamp'], info['object_count'],
                                info['bytes_used'])
            else:
                self.failures += 1
                self.logger.debug(
                    'Update report failed for %s %s' % (container, dbfile))
        else:
            self.no_changes += 1

    def container_report(self, node, part, container, put_timestamp,
                         delete_timestamp, count, bytes):
        """
        Report container info to an account server.

        :param node: node dictionary from the account ring
        :param part: partition the account is on
        :param container: container name
        :param put_timestamp: put timestamp
        :param delete_timestamp: delete timestamp
        :param count: object count in the container
        :param bytes: bytes used in the container
        """
        with ConnectionTimeout(self.conn_timeout):
            try:
                conn = http_connect(
                    node['ip'], node['port'], node['device'], part,
                    'PUT', container,
                    headers={'X-Put-Timestamp': put_timestamp,
                             'X-Delete-Timestamp': delete_timestamp,
                             'X-Object-Count': count,
                             'X-Bytes-Used': bytes,
                             'X-Account-Override-Deleted': 'yes'})
            except:
                self.logger.exception('ERROR account update failed with '
                    '%(ip)s:%(port)s/%(device)s (will retry later): ' % node)
                return 500
        with Timeout(self.node_timeout):
            try:
                resp = conn.getresponse()
                resp.read()
                return resp.status
            except:
                if self.logger.getEffectiveLevel() <= logging.DEBUG:
                    self.logger.exception(
                        'Exception with %(ip)s:%(port)s/%(device)s' % node)
                return 500
