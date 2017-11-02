from __future__ import print_function

from unittest import TestCase, SkipTest, skip

from py65.devices.mpu6502 import MPU
from wednesday.tests.cpu_6502_spec import CPU6502Spec

from py_mini_racer.py_mini_racer import MiniRacer

import os

dir_path = os.path.dirname(os.path.realpath(__file__))

class Torlus6502Test(CPU6502Spec, TestCase):

    @classmethod
    def setUpClass(cls):
        cls.STACK_PAGE = 0x100
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
        if register == 'P':
            self.ctx.eval('cpu.C = %s' % [0, 1][0 != value & 1])
            self.ctx.eval('cpu.Z = %s' % [0, 1][0 != value & 2])
            self.ctx.eval('cpu.I = %s' % [0, 1][0 != value & 4])
            self.ctx.eval('cpu.D = %s' % [0, 1][0 != value & 8])
            self.ctx.eval('cpu.V = %s' % [0, 1][0 != value & 64])
            self.ctx.eval('cpu.N = %s' % [0, 1][0 != value & 128])
            return
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
        stack_pointer = self.ctx.eval('cpu.S')
        self.ctx.eval('mem[%s] = %s' % (self.STACK_PAGE + stack_pointer, byte))
        self.ctx.eval('cpu.S = %s' % ((stack_pointer - 1) % 0x100))

    def cpu_pull_byte(self):
        stack_pointer = (self.ctx.eval('cpu.S') + 1) % 0x100
        self.ctx.eval('cpu.S = %s' % stack_pointer)
        return self.ctx.eval('mem[%s]' % (self.STACK_PAGE + stack_pointer))

    def cpu_push_word(self, word):
        hi, lo = divmod(word, 0x100)
        self.cpu_push_byte(hi)
        self.cpu_push_byte(lo)

    def cpu_pull_word(self):
        stack_pointer = self.ctx.eval('cpu.S')
        s = self.STACK_PAGE + stack_pointer + 1
        stack_pointer += 2
        raise NotImplementedError()

    def push_byte(self, byte):
        self.write_byte(self.STACK_PAGE + self.stack_pointer, byte)
        self.stack_pointer = (self.stack_pointer - 1) % 0x100

    def pull_byte(self):
        self.stack_pointer = (self.stack_pointer + 1) % 0x100
        return self.read_byte(self.STACK_PAGE + self.stack_pointer)

    def push_word(self, word):
        hi, lo = divmod(word, 0x100)
        self.push_byte(hi)
        self.push_byte(lo)

    def pull_word(self):
        s = self.STACK_PAGE + self.stack_pointer + 1
        self.stack_pointer += 2
        return self.read_word(s)

    @skip('TODO')
    def test_brk(self):
        pass

    @skip('TODO')
    def test_jsr(self):
        pass

    @skip('TODO')
    def test_pla(self):
        pass

    @skip('TODO')
    def test_pla_n_flag_set(self):
        pass

    @skip('TODO')
    def test_pla_z_flag_set(self):
        pass

    @skip('TODO')
    def test_rti(self):
        pass

    @skip('TODO')
    def test_rts(self):
        pass
