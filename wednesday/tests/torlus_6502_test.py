from __future__ import print_function

from unittest import TestCase
from unittest import SkipTest

from py65.devices.mpu6502 import MPU
from wednesday.tests.cpu_6502_spec import CPU6502Spec

from py_mini_racer.py_mini_racer import MiniRacer

import os

dir_path = os.path.dirname(os.path.realpath(__file__))

class Torlus6502Test(CPU6502Spec, TestCase):

    @classmethod
    def setUpClass(cls):
        with open(dir_path + '/../torlus6502.js') as f:
            javascript = f.read()
        cls.ctx = MiniRacer()
        cls.ctx.eval('var mem = Array.apply(null, Array(300)).map(Number.prototype.valueOf,0);')
        cls.ctx.eval(javascript)

    def setUp(self):
        self.ctx.eval('var mem = Array.apply(null, Array(300)).map(Number.prototype.valueOf,0);')
        self.ctx.eval('cpu = new CPU6502()')
        self.ctx.eval('cpu.reset()')

    def tearDown(self):
        pass

    def cpu_pc(self, counter):
        self.ctx.eval('cpu.PC = %s' % counter)

    def memory_set(self, pos, val):
        self.ctx.eval('mem[%s] = %s' % (pos, val))

    def memory_fetch(self, pos):
        return self.ctx.eval('mem[%s]' % pos)

    def execute(self):
        self.ctx.eval('cpu.step()')
        return self.ctx.eval('cpu.cycles'), None

    def cpu_set_register(self, register, value):
        if register == 'SP':
            register = 'S'
        self.ctx.eval('cpu.%s = %s' % (register, value))

    def cpu_register(self, register):
        if register == 'SP':
            register = 'S'
        return self.ctx.eval('cpu.%s' % register)

    def cpu_flag(self, flag):
        return bool(self.ctx.eval('cpu.%s' % flag))

    def cpu_set_flag(self, flag):
        self.ctx.eval('cpu.%s = 1' % flag)

    def cpu_unset_flag(self, flag):
        self.ctx.eval('cpu.%s = 0' % flag)

    def cpu_push_byte(self, byte):
        raise NotImplementedError()

    def cpu_pull_byte(self):
        raise NotImplementedError()

    def cpu_push_word(self, word):
        raise NotImplementedError()

    def cpu_pull_word(self):
        raise NotImplementedError()
