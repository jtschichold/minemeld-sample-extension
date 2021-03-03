import logging
import time
from datetime import datetime, timedelta
from collections import deque

import gevent

from minemeld.ft import ft_states  #pylint: disable=E0401
from minemeld.ft.base import _counting  #pylint: disable=E0401
from minemeld.ft.actorbase import ActorBaseFT  #pylint: disable=E0401
from minemeld.ft.table import Table #pylint: disable=E0401

LOG = logging.getLogger(__name__)

class Output(ActorBaseFT):
    def __init__(self, name, chassis, config):
        self._queue = None

        super(Output, self).__init__(name, chassis, config)

        self._push_glet = None
        self._next_push = None

    def configure(self):
        super(Output, self).configure()

        self.wait_time = int(self.config.get('wait_time', 300))

    def connect(self, inputs, output):
        output = False
        super(Output, self).connect(inputs, output)

    def _initialize_table(self, truncate=False):
        self.table = Table(name=self.name, truncate=truncate)

    def initialize(self):
        self._initialize_table()

    def rebuild(self):
        self._initialize_table(truncate=(self.last_checkpoint is None))

    def reset(self):
        self._initialize_table(truncate=True)

    @_counting('update.processed')
    def filtered_update(self, source=None, indicator=None, value=None):
        self.table.put(indicator, value)
        self._next_push = time.time() + self.wait_time

    @_counting('withdraw.processed')
    def filtered_withdraw(self, source=None, indicator=None, value=None):
        self.table.delete(indicator)
        self._next_push = time.time() + self.wait_time

    def length(self, source=None):
        return self.table.length()

    def _push(self):
        for i, _v in self.table.query(include_value=False):
            # XXX - code to push here
            LOG.info(f'{self.name} - push entry {i}')

    def _push_loop(self):
        while True:
            now = time.time()

            if self._next_push is not None and now > self._next_push:
                self._next_push = None
                self._push()

            gevent.sleep(seconds=10.0)            

    def start(self):
        super(Output, self).start()

        self._push_glet = gevent.spawn(self._push_loop)

    def stop(self):
        super(Output, self).stop()

        if self._push_glet is not None:
            self._push_glet.kill()

        if self._checkpoint_glet is not None:
            self._checkpoint_glet.kill()

        self.table.close()

    def hup(self, source=None):
        LOG.info(f'{self.name} - hup received')
