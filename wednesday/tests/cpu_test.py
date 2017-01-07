from unittest import TestCase
from unittest import skip

from wednesday.cpu6502 import *
from wednesday.tests.cpu_6502_spec import CPU6502Spec

REGISTERS = {
    'A': 'accumulator',
    'X': 'x_index',
    'Y': 'y_index',
    'SP': 'stack_pointer',
    'PC': 'program_counter',
}

FLAGS = {
    'C': 'carry_flag',
    'Z': 'zero_flag',
    'I': 'interrupt_disable_flag',
    'D': 'decimal_mode_flag',
    'B': 'break_flag',
    'V': 'overflow_flag',
    'N': 'sign_flag',
}


class CPUTest(CPU6502Spec, TestCase):

    def setUp(self):
        class Options():

            def __init__(self):
                self.rom = None
                self.ram = None
                self.bus = None
                self.pc = 0xFFFA

        self.memory = BasicMemory()
        self.options = Options()
        self.cpu = CPU(self.options, self.memory)

        self.executor = self.cpu.run()

    def tearDown(self):
        pass

    def cpu_pc(self, counter):
        self.cpu.program_counter = counter

    def memory_set(self, pos, val):
        self.memory._mem[pos] = val

    def memory_fetch(self, pos):
        return self.memory._mem[pos]

    def execute(self):
        cycle, _ = self.executor.next()
        return cycle, _

    def cpu_set_register(self, register, value):
        name = REGISTERS[register]
        setattr(self.cpu, name, value)

    def cpu_register(self, register):
        name = REGISTERS[register]
        return getattr(self.cpu, name)

    def cpu_flag(self, flag):
        name = FLAGS[flag]
        return not not getattr(self.cpu, name)

    def cpu_set_flag(self, flag):
        name = FLAGS[flag]
        setattr(self.cpu, name, True)

    def cpu_unset_flag(self, flag):
        name = FLAGS[flag]
        setattr(self.cpu, name, False)

    def cpu_push_byte(self, byte):
        self.cpu.push_byte(byte)

    def cpu_pull_byte(self):
        return self.cpu.pull_byte()

    def cpu_push_word(self, word):
        self.cpu.push_word(word)

    def cpu_pull_word(self):
        return self.cpu.pull_word()
