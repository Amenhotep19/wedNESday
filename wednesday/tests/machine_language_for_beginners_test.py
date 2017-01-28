from unittest import TestCase
from unittest import skip

from nesasm.compiler import lexical, semantic, syntax, Cartridge
from wednesday.tests.py65_cpu_test import Py65CPUBridge
from py65.devices.mpu6502 import MPU


# snippets from book Machine language for beginners

class TheFundamentalsTest(Py65CPUBridge, TestCase):
    # chapter 2

    def setUp(self):
        self.cpu = MPU()

    def assembly(self, source, start_addr=0):
        cart = Cartridge()
        if start_addr != 0:
          cart.set_org(start_addr)
        return semantic(syntax(lexical(source)), False, cart)

    def load_program(self, code):
        start_addr = 0x0100
        opcodes = self.assembly(code, start_addr)
        self.cpu_pc(start_addr)
        for addr, val in enumerate(opcodes, start=start_addr):
            self.memory_set(addr, val)
        self.stop_addr = addr

    def run_program(self):
        b = 0
        while self.cpu.pc < self.stop_addr:
            self.execute()
            if b > 1000:
                raise Exception('dammit')
                break
            b += 1


    def test_program_2_8(self):
        code = '''
            LDA #$02
            ADC #$05
            STA $0FA0
            RTS
        '''

        self.load_program(code)
        self.run_program()

        self.assertEquals(self.cpu_register('A'), 7)
        self.assertEquals(7, self.memory_fetch(0x0fa0))

