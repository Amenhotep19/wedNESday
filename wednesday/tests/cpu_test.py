from unittest import TestCase
from unittest import skip

from wednesday.cpu6502 import *

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

class CPUTest(TestCase):

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
        self.cpu.pull_byte()

    def cpu_push_word(self, word):
        self.cpu.push_word(word)

    def cpu_pull_word(self):
        self.cpu.pull_word()

    def test_lda_imediate(self):
        self.cpu_pc(0x0100)

        self.memory_set(0x0100, 0xa9)
        self.memory_set(0x0101, 0xff)
        self.execute()

        self.assertEquals(self.cpu_register('A'), 0xff)

    def test_lda_zeropage(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xa5)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0xff)
        self.execute()

        self.assertEquals(self.cpu_register('A'), 0xff)

    def test_lda_zero_page_x(self):
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xb5)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0xff)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0xff)

    def test_lda_absolute(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xad)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0084, 0xff)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0xff)

    def test_lda_absolute_x(self):
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xbd)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0085, 0xff)

        cycles, _ = self.execute()

        self.assertEquals(cycles, 4)
        self.assertEquals(self.cpu_register('A'), 0xff)

    @skip('TODO')
    def test_lda_absolute_x_2(self):
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xbd)
        self.memory_set(0x0101, 0xff)
        self.memory_set(0x0102, 0x02)
        self.memory_set(0x0300, 0xff)

        cycles, _ = self.execute()

        self.assertEquals(cycles, 5)

    def test_lda_absolute_y(self):
        self.cpu_set_register('Y', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xb9)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0085, 0xff)

        cycles, _ = self.execute()

        self.assertEquals(cycles, 4)
        self.assertEquals(self.cpu_register('A'), 0xff)

        self.cpu_set_register('Y', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xb9)
        self.memory_set(0x0101, 0xff)
        self.memory_set(0x0102, 0x02)
        self.memory_set(0x0300, 0xff)

        cycles, _ = self.execute()

        # TODO: self.assertEquals(cycles, 5)

    def test_lda_indirect_x(self):
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xa1)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0x87)
        self.memory_set(0x0086, 0x00)
        self.memory_set(0x0087, 0xff)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0xff)

    def test_lda_indirect_y(self):
        self.cpu_set_register('Y', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xb1)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x86)
        self.memory_set(0x0085, 0x00)
        self.memory_set(0x0087, 0xff)

        cycles, _ = self.execute()

        #TODO: self.assertEquals(cycle, 5)
        self.assertEquals(self.cpu_register('A'), 0xff)

        self.cpu_set_register('Y', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xb1)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0xff)
        self.memory_set(0x0085, 0x02)
        self.memory_set(0x0300, 0xff)

        cycles, _ = self.execute()

        #TODO: self.assertEquals(cycle, 6)

    def test_lda_z_flag_set(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xa9)
        self.memory_set(0x0101, 0x00)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_lda_z_flag_unset(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xa9)
        self.memory_set(0x0101, 0x01)

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    def test_lda_n_flag_set(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xa9)
        self.memory_set(0x0101, 0x81)

        self.execute()

        self.assertTrue(self.cpu_flag('N'))

    def test_lda_n_flag_unset(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xa9)
        self.memory_set(0x0101, 0x01)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    # // LDX

    def test_ldx_immediate(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xa2)
        self.memory_set(0x0101, 0xff)

        self.execute()

        self.assertEquals(self.cpu_register('X'), 0xff)

    def test_ldx_zero_page(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xa6)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0xff)

        self.execute()

        self.assertEquals(self.cpu_register('X'), 0xff)

    def test_ldx_zeropage_y(self):
        self.cpu_set_register('Y', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xb6)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0xff)

        self.execute()

        self.assertEquals(self.cpu_register('X'), 0xff)

    def test_ldx_absolute(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xae)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0084, 0xff)

        self.execute()

        self.assertEquals(self.cpu_register('X'), 0xff)

    def test_ldx_absolute_y(self):
        self.cpu_set_register('Y', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xbe)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0085, 0xff)

        self.execute()

        self.assertEquals(self.cpu_register('X'), 0xff)

    def test_ldx_z_flag_set(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xa2)
        self.memory_set(0x0101, 0x00)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_ldx_z_flag_unset(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xa2)
        self.memory_set(0x0101, 0x01)

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    def test_ldx_n_flag_set(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xa2)
        self.memory_set(0x0101, 0x81)

        self.execute()

        self.assertTrue(self.cpu_flag('N'))

    def test_ldx_n_flag_unset(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xa2)
        self.memory_set(0x0101, 0x01)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    # // LDY

    def test_ldy_immediate(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xa0)
        self.memory_set(0x0101, 0xff)

        self.execute()

        self.assertEquals(self.cpu_register('Y'), 0xff)

    def test_ldy_zeropage(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xa4)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0xff)

        self.execute()
        self.assertEquals(self.cpu_register('Y'), 0xff)

    def test_ldy_zeropage_x(self):
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xb4)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0xff)

        self.execute()

        self.assertEquals(self.cpu_register('Y'), 0xff)

    def test_ldy_absolute(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xac)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0084, 0xff)

        self.execute()

        self.assertEquals(self.cpu_register('Y'), 0xff)

    def test_ldy_absolute_x(self):
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xbc)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0085, 0xff)

        self.execute()

        self.assertEquals(self.cpu_register('Y'), 0xff)

    def test_ldy_z_flag_set(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xa0)
        self.memory_set(0x0101, 0x00)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_ldy_z_flag_unset(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xa0)
        self.memory_set(0x0101, 0x01)

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    def test_ldy_n_flag_set(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xa0)
        self.memory_set(0x0101, 0x81)

        self.execute()

        self.assertTrue(self.cpu_flag('N'))

    def test_ldy_n_flag_unset(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xa0)
        self.memory_set(0x0101, 0x01)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    # // STA

    def test_sta_zeropage(self):
        self.cpu_set_register('A', 0xff)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x85)
        self.memory_set(0x0101, 0x84)

        self.execute()

        self.assertEquals(self.memory_fetch(0x0084), 0xff)

    def test_sta_zeropage_x(self):
        self.cpu_set_register('A', 0xff)
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x95)
        self.memory_set(0x0101, 0x84)

        self.execute()

        self.assertEquals(self.memory_fetch(0x0085), 0xff)

    def test_sta_absolute(self):
        self.cpu_set_register('A', 0xff)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x8d)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)

        self.execute()

        self.assertEquals(self.memory_fetch(0x0084), 0xff)

    def test_sta_absolute_x(self):
        self.cpu_set_register('A', 0xff)
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x9d)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)

        self.execute()

        self.assertEquals(self.memory_fetch(0x0085), 0xff)

    def test_sta_absolute_y(self):
        self.cpu_set_register('A', 0xff)
        self.cpu_set_register('Y', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x99)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)

        self.execute()

        self.assertEquals(self.memory_fetch(0x0085), 0xff)

    def test_sta_indirect_x(self):
        self.cpu_set_register('A', 0xff)
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x81)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0x87)
        self.memory_set(0x0086, 0x00)

        self.execute()

        self.assertEquals(self.memory_fetch(0x0087), 0xff)

    def test_sta_indirect_y(self):
        self.cpu_set_register('A', 0xff)
        self.cpu_set_register('Y', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x91)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x86)
        self.memory_set(0x0085, 0x00)

        self.execute()

        self.assertEquals(self.memory_fetch(0x0087), 0xff)

    # // STX

    def test_stx_zeropage(self):
        self.cpu_set_register('X', 0xff)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x86)
        self.memory_set(0x0101, 0x84)

        self.execute()

        self.assertEquals(self.memory_fetch(0x0084), 0xff)

    def test_stx_zeropage_y(self):
        self.cpu_set_register('X', 0xff)
        self.cpu_set_register('Y', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x96)
        self.memory_set(0x0101, 0x84)

        self.execute()

        self.assertEquals(self.memory_fetch(0x0085), 0xff)

    def test_stx_absolute(self):
        self.cpu_set_register('X', 0xff)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x8e)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)

        self.execute()

        self.assertEquals(self.memory_fetch(0x0084), 0xff)

    # // STY

    def test_sty_zeropage(self):
        self.cpu_set_register('Y', 0xff)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x84)
        self.memory_set(0x0101, 0x84)

        self.execute()

        self.assertEquals(self.memory_fetch(0x0084), 0xff)

    def test_sty_zeropage_y(self):
        self.cpu_set_register('Y', 0xff)
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x94)
        self.memory_set(0x0101, 0x84)

        self.execute()

        self.assertEquals(self.memory_fetch(0x0085), 0xff)

    def test_sty_absolute(self):
        self.cpu_set_register('Y', 0xff)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x8c)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)

        self.execute()

        self.assertEquals(self.memory_fetch(0x0084), 0xff)

    # // TAX

    def test_tax(self):
        self.cpu_set_register('A', 0xff)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xaa)

        self.execute()

        self.assertEquals(self.cpu_register('X'), 0xff)

    def test_tax_z_flag_set(self):
        self.cpu_set_register('A', 0x00)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xaa)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_tax_z_flag_unset(self):
        self.cpu_set_register('A', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xaa)

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    def test_tax_n_flag_set(self):
        self.cpu_set_register('A', 0x81)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xaa)

        self.execute()

        self.assertTrue(self.cpu_flag('N'))

    def test_tax_n_flag_unset(self):
        self.cpu_set_register('A', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xaa)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    # // TAY

    def test_tay(self):
        self.cpu_set_register('A', 0xff)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xa8)

        self.execute()

        self.assertEquals(self.cpu_register('Y'), 0xff)

    # // TXA

    def test_txa(self):
        self.cpu_set_register('X', 0xff)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x8a)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0xff)

    # // TYA

    def test_tya(self):
        self.cpu_set_register('Y', 0xff)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x98)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0xff)

    # // TSX

    def test_tsx(self):
        self.cpu_set_register('SP', 0xff)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xba)

        self.execute()

        self.assertEquals(self.cpu_register('X'), 0xff)

    # // TXS

    def test_txs(self):
        self.cpu_set_register('X', 0xff)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x9a)

        self.execute()

        self.assertEquals(self.cpu_register('SP'), 0xff)

    # // PHA

    @skip('TODO')
    def test_pha(self):
        self.cpu_set_register('A', 0xff)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x48)

        self.execute()

        self.assertEquals(self.cpu_pull_byte(), 0xff)

    # // PHP

    @skip('TODO')
    def test_php(self):
        self.cpu_set_register('P', 0xff)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x08)

        self.execute()

        self.assertEquals(self.cpu_pull_byte(), 0xff)

    # // PLA

    def test_pla(self):
        self.cpu_push_byte(0xff)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x68)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0xff)

    def test_pla_z_flag_set(self):
        self.cpu_push_byte(0x00)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x68)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_pla_z_flag_unset(self):
        self.cpu_push_byte(0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x68)

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    def test_pla_n_flag_set(self):
        self.cpu_push_byte(0x81)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x68)

        self.execute()
        self.assertTrue(self.cpu_flag('N'))

    def test_pla_n_flag_unset(self):
        self.cpu_push_byte(0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x68)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))


    # // PLP

    @skip('TODO')
    def test_plp(self):
        self.cpu_push_byte(0xff)
        self.cpu_pc(0x0100)

        self.memory_set(0x0100, 0x28)

        self.execute()

        # TODO: self.assertEquals(self.cpu_register('P'), 0xef)

    # // AND

    def test_and_immediate(self):
        self.cpu_set_register('A', 0xff)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x29)
        self.memory_set(0x0101, 0x0f)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0x0f)

    def test_and_zeropage(self):
        self.cpu_set_register('A', 0xff)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x25)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x0f)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0x0f)

    def test_and_zeropage_x(self):
        self.cpu_set_register('A', 0xff)
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x35)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0x0f)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0x0f)

    def test_and_absolute(self):
        self.cpu_set_register('A', 0xff)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x2d)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0084, 0x0f)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0x0f)

    def test_and_absolute_x(self):
        self.cpu_set_register('A', 0xff)
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x3d)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0085, 0x0f)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0x0f)

    def test_and_absolute_y(self):
        self.cpu_set_register('A', 0xff)
        self.cpu_set_register('Y', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x39)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0085, 0x0f)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0x0f)

    def test_and_indirect_x(self):
        self.cpu_set_register('A', 0xff)
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x21)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0x87)
        self.memory_set(0x0086, 0x00)
        self.memory_set(0x0087, 0x0f)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0x0f)

    def test_and_indirect_y(self):
        self.cpu_set_register('A', 0xff)
        self.cpu_set_register('Y', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x31)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x86)
        self.memory_set(0x0085, 0x00)
        self.memory_set(0x0087, 0x0f)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0x0f)

    def test_and_z_flag_set(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x29)
        self.memory_set(0x0101, 0x00)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_and_z_flag_unset(self):
        self.cpu_set_register('A', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x29)
        self.memory_set(0x0101, 0x01)

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    def test_and_n_flag_set(self):
        self.cpu_set_register('A', 0x81)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x29)
        self.memory_set(0x0101, 0x81)

        self.execute()

        self.assertTrue(self.cpu_flag('N'))

    def test_and_n_flag_unset(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x29)
        self.memory_set(0x0101, 0x01)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    # // EOR

    def test_eor_immediate(self):
        self.cpu_set_register('A', 0xff)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x49)
        self.memory_set(0x0101, 0x0f)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0xf0)

    def test_eor_zeropage(self):
        self.cpu_set_register('A', 0xff)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x45)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x0f)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0xf0)

    def test_eor_zeropage_x(self):
        self.cpu_set_register('A', 0xff)
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x55)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0x0f)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0xf0)

    def test_eor_absolute(self):
        self.cpu_set_register('A', 0xff)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x4d)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0084, 0x0f)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0xf0)

    def test_eor_absolute_x(self):
        self.cpu_set_register('A', 0xff)
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x5d)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0085, 0x0f)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0xf0)

    def test_eor_absolute_y(self):
        self.cpu_set_register('A', 0xff)
        self.cpu_set_register('Y', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x59)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0085, 0x0f)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0xf0)

    def test_eor_indirect_x(self):
        self.cpu_set_register('A', 0xff)
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x41)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0x87)
        self.memory_set(0x0086, 0x00)
        self.memory_set(0x0087, 0x0f)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0xf0)

    def test_eor_indirect_y(self):
        self.cpu_set_register('A', 0xff)
        self.cpu_set_register('Y', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x51)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x86)
        self.memory_set(0x0085, 0x00)
        self.memory_set(0x0087, 0x0f)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0xf0)

    def test_eor_z_flag_set(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x49)
        self.memory_set(0x0101, 0x00)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_eor_z_flag_unset(self):
        self.cpu_set_register('A', 0x00)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x49)
        self.memory_set(0x0101, 0x01)

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    def test_eor_n_flag_set(self):
        self.cpu_set_register('A', 0x00)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x49)
        self.memory_set(0x0101, 0x81)

        self.execute()

        self.assertTrue(self.cpu_flag('N'))

    def test_eor_n_flag_unset(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x49)
        self.memory_set(0x0101, 0x01)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    # // ORA

    def test_ora_immediate(self):
        self.cpu_set_register('A', 0xf0)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x09)
        self.memory_set(0x0101, 0x0f)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0xff)

    def test_ora_zeropage(self):
        self.cpu_set_register('A', 0xf0)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x05)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x0f)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0xff)

    def test_ora_zeropage_x(self):
        self.cpu_set_register('A', 0xf0)
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x15)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0x0f)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0xff)

    def test_ora_absolute(self):
        self.cpu_set_register('A', 0xf0)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x0d)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0084, 0x0f)
        self.execute()

        self.assertEquals(self.cpu_register('A'), 0xff)

    def test_ora_absolute_x(self):
        self.cpu_set_register('A', 0xf0)
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x1d)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0085, 0x0f)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0xff)

    def test_ora_absolute_y(self):
        self.cpu_set_register('A', 0xf0)
        self.cpu_set_register('Y', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x19)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0085, 0x0f)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0xff)

    def test_ora_indirect_x(self):
        self.cpu_set_register('A', 0xf0)
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x01)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0x87)
        self.memory_set(0x0086, 0x00)
        self.memory_set(0x0087, 0x0f)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0xff)

    def test_ora_indirect_y(self):
        self.cpu_set_register('A', 0xf0)
        self.cpu_set_register('Y', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x11)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x86)
        self.memory_set(0x0085, 0x00)
        self.memory_set(0x0087, 0x0f)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0xff)

    def test_ora_z_flag_set(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x09)
        self.memory_set(0x0101, 0x00)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_ora_z_flag_unset(self):
        self.cpu_set_register('A', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x09)
        self.memory_set(0x0101, 0x00)

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    def test_ora_n_flag_set(self):
        self.cpu_set_register('A', 0x81)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x09)
        self.memory_set(0x0101, 0x00)

        self.execute()

        self.assertTrue(self.cpu_flag('N'))

    def test_ora_n_flag_unset(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x09)
        self.memory_set(0x0101, 0x01)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    # // BIT

    def test_bit_zeropage(self):
        self.cpu_set_register('A', 0xff)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x24)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x7f)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    def test_bit_absolute(self):
        self.cpu_set_register('A', 0xff)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x2c)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0084, 0x7f)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    def test_bit_n_flag_set(self):
        self.cpu_set_register('A', 0xff)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x24)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0xff)

        self.execute()

        self.assertTrue(self.cpu_flag('N'))

    def test_bit_n_flag_unset(self):
        self.cpu_set_register('A', 0xff)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x24)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x7f)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    def test_bit_v_flag_set(self):
        self.cpu_set_register('A', 0xff)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x24)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0xff)

        self.execute()

        self.assertTrue(self.cpu_flag('V'))

    def test_bit_v_flag_unset(self):
        self.cpu_set_register('A', 0xff)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x24)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x3f)

        self.execute()

        self.assertFalse(self.cpu_flag('V'))

    def test_bit_z_flag_set(self):
        self.cpu_set_register('A', 0x00)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x24)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0xff)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_bit_z_flag_unset(self):
        self.cpu_set_register('A', 0xff)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x24)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x3f)

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    # // ADC

    def test_adc_immediate(self):

        self.cpu_set_register('A', 0x01)
        self.cpu_pc(0x0100)

        self.memory_set(0x0100, 0x69)
        self.memory_set(0x0101, 0x02)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0x03)

        return
        # TODO
        self.cpu_set_flag('D')
        self.cpu_set_register('A', 0x29) # BCD
        self.cpu_pc(0x0100)

        self.memory_set(0x0100, 0x69)
        self.memory_set(0x0101, 0x11) # BCD

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0x40)

        self.cpu_set_flag('D')
        self.cpu_set_register('A', 0x29) | uint8(N) # BCD
        self.cpu_pc(0x0100)

        self.memory_set(0x0100, 0x69)
        self.memory_set(0x0101, 0x29) # BCD

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0x38)

        self.cpu_set_flag('D')
        self.cpu_set_flag('C')
        self.cpu_set_register('A', 0x58) // BCD
        self.cpu_pc(0x0100)

        self.memory_set(0x0100, 0x69)
        self.memory_set(0x0101, 0x46) // BCD

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0x05)

    def test_adc_zeropage(self):
        self.cpu_set_register('A', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x65)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x02)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0x03)

    def test_adc_zeropage_x(self):
        self.cpu_set_register('A', 0x01)
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x75)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0x02)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0x03)

    def test_adc_absolute(self):
        self.cpu_set_register('A', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x6d)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0084, 0x02)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0x03)

    def test_adc_absolute_x(self):
        self.cpu_set_register('A', 0x01)
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x7d)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0085, 0x02)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0x03)

    def test_adc_absolute_y(self):
        self.cpu_set_register('A', 0x01)
        self.cpu_set_register('Y', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x79)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0085, 0x02)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0x03)

    def test_adc_indirect_x(self):
        self.cpu_set_register('A', 0x01)
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x61)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0x87)
        self.memory_set(0x0086, 0x00)
        self.memory_set(0x0087, 0x02)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0x03)


    def test_adc_indirect_y(self):
        self.cpu_set_register('A', 0x01)
        self.cpu_set_register('Y', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x71)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x86)
        self.memory_set(0x0085, 0x00)
        self.memory_set(0x0087, 0x02)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0x03)

    def test_adc_c_flag_set(self):
        self.cpu_set_register('A', 0xff) # -1
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x69)
        self.memory_set(0x0101, 0x01) # +1

        self.execute()

        self.assertTrue(self.cpu_flag('C'))

        self.cpu_set_flag('C')
        self.cpu_set_register('A', 0xff) # -1
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x69)
        self.memory_set(0x0101, 0x00) # +0

        self.execute()

        self.assertTrue(self.cpu_flag('C'))

    def test_adc_c_flag_unset(self):
        self.cpu_set_register('A', 0x00) # +0
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x69)
        self.memory_set(0x0101, 0x01) # +1

        self.execute()

        self.assertFalse(self.cpu_flag('C'))

        self.cpu_unset_flag('C')
        self.cpu_set_register('A', 0xff) # -1
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x69)
        self.memory_set(0x0101, 0x00) # +0

        self.execute()

        self.assertFalse(self.cpu_flag('C'))

    def test_adc_z_flag_set(self):
        self.cpu_set_register('A', 0x00) # +0
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x69)
        self.memory_set(0x0101, 0x00) # +0

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

        self.cpu_set_flag('C')
        self.cpu_set_register('A', 0xfe) # -2
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x69)
        self.memory_set(0x0101, 0x01) # +1

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_adc_z_flag_unset(self):
        self.cpu_set_register('A', 0x00) # +0
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x69)
        self.memory_set(0x0101, 0xff) # -1

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

        self.cpu_set_register('A', 0xfe) # -2
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x69)
        self.memory_set(0x0101, 0x01) # +1

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    def test_adc_v_flag_set(self):
        self.cpu_set_register('A', 0x7f) # +127
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x69)
        self.memory_set(0x0101, 0x01) # +1

        self.execute()

        self.assertTrue(self.cpu_flag('V'))

    def test_adc_v_flag_unset(self):
        self.cpu_set_register('A', 0x01) # +1
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x69)
        self.memory_set(0x0101, 0x01) # +1

        self.execute()

        self.assertFalse(self.cpu_flag('V'))

    def test_adc_n_flag_set(self):
        self.cpu_set_register('A', 0x01) # +1
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x69)
        self.memory_set(0x0101, 0xfe) # -2

        self.execute()

        self.assertTrue(self.cpu_flag('N'))

    def test_adc_n_flag_unset(self):
        self.cpu_set_register('A', 0x01) # +1
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x69)
        self.memory_set(0x0101, 0x01) # +1

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    # // SBC

    def test_sbc_immediate(self):
        self.cpu_set_flag('C')
        self.cpu_set_register('A', 0x02)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xe9)
        self.memory_set(0x0101, 0x01)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0x01)

        return
        # TODO
        self.cpu_set_flag('D')
        self.cpu_set_register('A', 0x29) # BCD
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xe9)
        self.memory_set(0x0101, 0x11) # BCD

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0x18)

    def test_sbc_zeroPage(self):
        self.cpu_set_flag('C')
        self.cpu_set_register('A', 0x02)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xe5)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x01)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0x01)

    def test_sbc_zeropage_x(self):
        self.cpu_set_flag('C')
        self.cpu_set_register('A', 0x02)
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xf5)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0x01)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0x01)

    def test_sbc_absolute(self):
        self.cpu_set_flag('C')
        self.cpu_set_register('A', 0x02)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xed)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0084, 0x01)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0x01)

    def test_sbc_absolute_x(self):
        self.cpu_set_flag('C')
        self.cpu_set_register('A', 0x02)
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xfd)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0085, 0x01)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0x01)

    def test_sbc_absolute_y(self):
        self.cpu_set_flag('C')
        self.cpu_set_register('A', 0x02)
        self.cpu_set_register('Y', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xf9)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0085, 0x01)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0x01)

    def test_sbc_indirect_x(self):
        self.cpu_set_flag('C')
        self.cpu_set_register('A', 0x02)
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)

        self.memory_set(0x0100, 0xe1)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0x87)
        self.memory_set(0x0086, 0x00)
        self.memory_set(0x0087, 0x01)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0x01)

    def test_sbc_indirect_y(self):
        self.cpu_set_flag('C')
        self.cpu_set_register('A', 0x02)
        self.cpu_set_register('Y', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xf1)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x86)
        self.memory_set(0x0085, 0x00)
        self.memory_set(0x0087, 0x01)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0x01)

    def test_sbc_c_flag_set(self):
        self.cpu_set_register('A', 0xc4) # -60
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xe9)
        self.memory_set(0x0101, 0x3c) # +60

        self.execute()

        self.assertTrue(self.cpu_flag('C'))

    def test_sbc_c_flag_unset(self):
        self.cpu_set_register('A', 0x02) # +2
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xe9)
        self.memory_set(0x0101, 0x04) # +4

        self.execute()

        self.assertFalse(self.cpu_flag('C'))

    def test_sbc_z_flag_set(self):
        self.cpu_set_register('A', 0x02) # +2
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xe9)
        self.memory_set(0x0101, 0x01) # +1

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_sbc_z_flag_unset(self):
        self.cpu_set_register('A', 0x02) # +2
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xe9)
        self.memory_set(0x0101, 0x02) # +2

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    def test_sbc_v_flag_set(self):
        self.cpu_set_register('A', 0x80) # -128
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xe9)
        self.memory_set(0x0101, 0x01) # +1

        self.execute()

        self.assertTrue(self.cpu_flag('V'))

    def test_sbc_v_flag_unset(self):
        self.cpu_set_register('A', 0x01) # +1
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xe9)
        self.memory_set(0x0101, 0x01) # +1

        self.execute()

        self.assertFalse(self.cpu_flag('V'))

    def test_sbc_n_flag_set(self):
        self.cpu_set_register('A', 0xfd) # -3
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xe9)
        self.memory_set(0x0101, 0x01) # +1

        self.execute()

        self.assertTrue(self.cpu_flag('N'))

    def test_sbc_n_flag_unset(self):
        self.cpu_set_register('A', 0x02) # +2
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xe9)
        self.memory_set(0x0101, 0x01) # +1

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    # // CMP

    def test_cmp_immediate(self):
        self.cpu_set_register('A', 0xff)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xc9)
        self.memory_set(0x0101, 0xff)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_cmp_zeropage(self):
        self.cpu_set_register('A', 0xff)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xc5)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0xff)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_cmp_zeropage_x(self):
        self.cpu_set_register('A', 0xff)
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xd5)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0xff)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_cmp_absolute(self):
        self.cpu_set_register('A', 0xff)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xcd)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0084, 0xff)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_cmp_absolute_x(self):
        self.cpu_set_register('A', 0xff)
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xdd)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0085, 0xff)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_cmp_absolute_y(self):
        self.cpu_set_register('A', 0xff)
        self.cpu_set_register('Y', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xd9)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0085, 0xff)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_cmp_indirect_x(self):
        self.cpu_set_register('A', 0xff)
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xc1)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0x87)
        self.memory_set(0x0086, 0x00)
        self.memory_set(0x0087, 0xff)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_cmp_indirect_y(self):
        self.cpu_set_register('A', 0xff)
        self.cpu_set_register('Y', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xd1)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x86)
        self.memory_set(0x0085, 0x00)
        self.memory_set(0x0087, 0xff)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_cmp_n_flag_set(self):
        self.cpu_set_register('A', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xc9)
        self.memory_set(0x0101, 0x02)

        self.execute()

        self.assertTrue(self.cpu_flag('N'))

    def test_Cmp_n_flag_unset(self):
        self.cpu_set_register('A', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xc9)
        self.memory_set(0x0101, 0x01)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    def test_cmp_z_flag_set(self):
        self.cpu_set_register('A', 0x02)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xc9)
        self.memory_set(0x0101, 0x02)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

        self.cpu_set_register('A', 0xfe) # -2
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xc9)
        self.memory_set(0x0101, 0xfe) # -2

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_cmp_z_flag_unset(self):
        self.cpu_set_register('A', 0x02)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xc9)
        self.memory_set(0x0101, 0x01)

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

        self.cpu_set_register('A', 0xfe) # -2
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xc9)
        self.memory_set(0x0101, 0xff) # -1

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    def test_cmp_c_flag_set(self):
        self.cpu_set_register('A', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xc9)
        self.memory_set(0x0101, 0x01)

        self.execute()

        self.assertTrue(self.cpu_flag('C'))

        self.cpu_set_register('A', 0x02)
        self.cpu_pc(0x0100)

        self.memory_set(0x0100, 0xc9)
        self.memory_set(0x0101, 0x01)

        self.execute()

        self.assertTrue(self.cpu_flag('C'))

        self.cpu_set_register('A', 0xfe) # -2
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xc9)
        self.memory_set(0x0101, 0xfd) #s -3

        self.execute()

        self.assertTrue(self.cpu_flag('C'))

    def test_cmp_c_flag_unset(self):
        self.cpu_set_register('A', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xc9)
        self.memory_set(0x0101, 0x02)

        self.execute()

        self.assertFalse(self.cpu_flag('C'))

        self.cpu_set_register('A', 0xfd) # -3
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xc9)
        self.memory_set(0x0101, 0xfe) # -2

        self.execute()

        self.assertFalse(self.cpu_flag('C'))

    # // CPX

    def test_cpx_immediate(self):
        self.cpu_set_register('X', 0xff)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xe0)
        self.memory_set(0x0101, 0xff)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_cpx_zeropage(self):
        self.cpu_set_register('X', 0xff)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xe4)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0xff)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_cpx_absolute(self):
        self.cpu_set_register('X', 0xff)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xec)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0084, 0xff)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_cpx_n_flag_set(self):
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xe0)
        self.memory_set(0x0101, 0x02)

        self.execute()

        self.assertTrue(self.cpu_flag('N'))

    def test_cpx_n_flag_unset(self):
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xe0)
        self.memory_set(0x0101, 0x01)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    def test_cpx_z_flag_set(self):
        self.cpu_set_register('X', 0x02)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xe0)
        self.memory_set(0x0101, 0x02)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_cpx_z_flag_unset(self):
        self.cpu_set_register('X', 0x02)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xe0)
        self.memory_set(0x0101, 0x01)

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    def test_cpx_c_flag_set(self):
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xe0)
        self.memory_set(0x0101, 0x01)

        self.execute()

        self.assertTrue(self.cpu_flag('C'))

    def test_cpx_C_flag_unset(self):
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xe0)
        self.memory_set(0x0101, 0x02)

        self.execute()

        self.assertFalse(self.cpu_flag('C'))

    # // CPY

    def test_cpy_immediate(self):
        self.cpu_set_register('Y', 0xff)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xc0)
        self.memory_set(0x0101, 0xff)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_cpy_zeroPage(self):
        self.cpu_set_register('Y', 0xff)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xc4)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0xff)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_cpy_absolute(self):
        self.cpu_set_register('Y', 0xff)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xcc)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0084, 0xff)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_cpy_n_flag_set(self):
        self.cpu_set_register('Y', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xc0)
        self.memory_set(0x0101, 0x02)

        self.execute()

        self.assertTrue(self.cpu_flag('N'))

    def test_cpy_n_flag_unset(self):
        self.cpu_set_register('Y', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xc0)
        self.memory_set(0x0101, 0x01)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    def test_cpy_z_flag_set(self):
        self.cpu_set_register('Y', 0x02)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xc0)
        self.memory_set(0x0101, 0x02)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_Cpy_z_flag_unset(self):
        self.cpu_set_register('Y', 0x02)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xc0)
        self.memory_set(0x0101, 0x01)

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    def test_cpy_c_flag_set(self):
        self.cpu_set_register('Y', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xc0)
        self.memory_set(0x0101, 0x01)

        self.execute()

        self.assertTrue(self.cpu_flag('C'))

    def test_cpy_c_flag_unset(self):
        self.cpu_set_register('Y', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xc0)
        self.memory_set(0x0101, 0x02)

        self.execute()

        self.assertFalse(self.cpu_flag('C'))

    # // INC

    def test_inc_zeroPage(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xe6)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0xfe)

        self.execute()

        self.assertEquals(self.memory_fetch(0x0084), 0xff)

    def test_inc_zeropage_x(self):
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xf6)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0xfe)

        self.execute()

        self.assertEquals(self.memory_fetch(0x0085), 0xff)

    def test_inc_absolute(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xee)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0084, 0xfe)

        self.execute()

        self.assertEquals(self.memory_fetch(0x0084), 0xff)

    def test_inc_absolute_x(self):
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xfe)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0085, 0xfe)

        self.execute()

        self.assertEquals(self.memory_fetch(0x0085), 0xff)

    def test_inc_z_flag_set(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xe6)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0xff) # -1

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_inc_z_flag_unset(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xe6)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x00)

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    def test_inc_n_flag_set(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xe6)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0xfe) # -2

        self.execute()

        self.assertTrue(self.cpu_flag('N'))

    def test_inc_n_flag_unset(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xe6)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x00)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    # // INX

    def test_inx(self):
        self.cpu_set_register('X', 0xfe)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xe8)

        self.execute()

        self.assertEquals(self.cpu_register('X'), 0xff)

    def test_inx_z_flag_set(self):
        self.cpu_set_register('X', 0xff) # -1
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xe8)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_inx_z_flag_unset(self):
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xe8)

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    def test_inx_n_flag_set(self):
        self.cpu_set_register('X', 0xfe) # -2
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xe8)

        self.execute()

        self.assertTrue(self.cpu_flag('N'))

    def test_inx_n_flag_unset(self):
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xe8)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))


    # // INY

    def test_iny(self):
        self.cpu_set_register('Y', 0xfe) # -2
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xc8)

        self.execute()

        self.assertEquals(self.cpu_register('Y'), 0xff)

    def test_iny_z_flag_set(self):
        self.cpu_set_register('Y', 0xff) # -1
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xc8)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_iny_z_flag_unset(self):
        self.cpu_set_register('Y', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xc8)

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    def test_iny_n_flag_set(self):
        self.cpu_set_register('Y', 0xfe) # -2
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xc8)

        self.execute()

        self.assertTrue(self.cpu_flag('N'))

    def test_iny_n_flag_unset(self):
        self.cpu_set_register('Y', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xc8)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    # // DEC

    def test_dec_zeroPage(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xc6)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x02)

        self.execute()

        self.assertEquals(self.memory_fetch(0x0084), 0x01)

    def test_dec_zeropage_x(self):
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xd6)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0x02)

        self.execute()

        self.assertEquals(self.memory_fetch(0x0085), 0x01)

    def test_dec_absolute(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xce)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0084, 0x02)

        self.execute()

        self.assertEquals(self.memory_fetch(0x0084), 0x01)

    def test_dec_absolute_x(self):
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xde)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0085, 0x02)

        self.execute()

        self.assertEquals(self.memory_fetch(0x0085), 0x01)

    def test_dec_z_flag_set(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xc6)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x01)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_dec_z_flag_unset(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xc6)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x02)

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    def test_dec_n_flag_set(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xc6)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x00)

        self.execute()

        self.assertTrue(self.cpu_flag('N'))

    def test_Dec_n_flag_unset(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xc6)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x01)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    # // DEX

    def test_dex(self):
        self.cpu_set_register('X', 0x02)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xca)

        self.execute()

        self.assertEquals(self.cpu_register('X'), 0x01)

    def test_dex_z_flag_set(self):
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xca)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_dex_z_flag_unset(self):
        self.cpu_set_register('X', 0x02)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xca)

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    def test_dex_n_flag_set(self):
        self.cpu_set_register('X', 0x00)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xca)

        self.execute()

        self.assertTrue(self.cpu_flag('N'))

    def test_dex_n_flag_unset(self):
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xca)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    # // DEY

    def test_dey(self):
        self.cpu_set_register('Y', 0x02)
        self.cpu_pc(0x0100)

        self.memory_set(0x0100, 0x88)

        self.execute()

        self.assertEquals(self.cpu_register('Y'), 0x01)

    def test_dey_z_flag_set(self):
        self.cpu_set_register('Y', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x88)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_dey_z_flag_unset(self):
        self.cpu_set_register('Y', 0x02)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x88)

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    def test_dey_n_flag_set(self):
        self.cpu_set_register('Y', 0x00)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x88)

        self.execute()

        self.assertTrue(self.cpu_flag('N'))

    def test_dey_n_flag_unset(self):
        self.cpu_set_register('Y', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x88)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    # // ASL

    def test_asl_accumulator(self):
        self.cpu_set_register('A', 0x02)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x0a)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0x04)

    def test_asl_zeroPage(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x06)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x02)

        self.execute()

        self.assertEquals(self.memory_fetch(0x0084), 0x04)

    def test_asl_zeropage_x(self):
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x16)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0x02)

        self.execute()

        self.assertEquals(self.memory_fetch(0x0085), 0x04)


    def test_asl_absolute(self):

        self.cpu_pc(0x0100)

        self.memory_set(0x0100, 0x0e)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0084, 0x02)

        self.execute()

        self.assertEquals(self.memory_fetch(0x0084), 0x04)


    def test_asl_absoluteX(self):
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)

        self.memory_set(0x0100, 0x1e)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0085, 0x02)

        self.execute()

        self.assertEquals(self.memory_fetch(0x0085), 0x04)

    def test_asl_c_flag_set(self):
        self.cpu_set_register('A', 0xff)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x0a)

        self.execute()

        self.assertTrue(self.cpu_flag('C'))

    def test_asl_c_flag_unset(self):
        self.cpu_set_register('A', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x0a)

        self.execute()

        self.assertFalse(self.cpu_flag('C'))

    def test_asl_z_flag_set(self):
        self.cpu_set_register('A', 0x00)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x0a)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_asl_z_flag_unset(self):
        self.cpu_set_register('A', 0x02)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x0a)

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    def test_asl_n_flag_set(self):
        self.cpu_set_register('A', 0xfe)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x0a)

        self.execute()

        self.assertTrue(self.cpu_flag('N'))

    def test_asl_n_flag_unset(self):
        self.cpu_set_register('A', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x0a)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    # // LSR

    def test_lsr_accumulator(self):
        self.cpu_set_register('A', 0x2)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x4a)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0x01)

    def test_lsr_zeroPage(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x46)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x02)

        self.execute()

        self.assertEquals(self.memory_fetch(0x0084), 0x01)

    def test_lsr_zeropage_x(self):
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x56)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0x02)

        self.execute()

        self.assertEquals(self.memory_fetch(0x0085), 0x01)

    def test_lsr_absolute(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x4e)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0084, 0x02)

        self.execute()

        self.assertEquals(self.memory_fetch(0x0084), 0x01)

    def test_lsr_absolute_x(self):
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x5e)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0085, 0x02)

        self.execute()

        self.assertEquals(self.memory_fetch(0x0085), 0x01)

    def test_lsr_c_flag_set(self):
        self.cpu_set_register('A', 0xff)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x4a)

        self.execute()

        self.assertTrue(self.cpu_flag('C'))

    def test_lsr_c_flag_unset(self):
        self.cpu_set_register('A', 0x10)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x4a)

        self.execute()

        self.assertFalse(self.cpu_flag('C'))

    def test_lsr_z_flag_set(self):
        self.cpu_set_register('A', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x4a)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_lsr_z_flag_unset(self):
        self.cpu_set_register('A', 0x02)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x4a)

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))


    # TODO: def test_lsr_n_flag_set(self): }
    # TODO: not tested, N bit always set to 0

    def test_lsr_n_flag_unset(self):
        self.cpu_set_register('A', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x4a)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))


    # // ROL

    def test_rol_Accumulator(self):

        self.cpu_set_flag('C')
        self.cpu_set_register('A', 0x2)
        self.cpu_pc(0x0100)

        self.memory_set(0x0100, 0x2a)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0x05)


    def test_rol_ZeroPage(self):

        self.cpu_set_flag('C')
        self.cpu_pc(0x0100)

        self.memory_set(0x0100, 0x26)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x02)

        self.execute()

        self.assertEquals(self.memory_fetch(0x0084), 0x05)


    def test_rol_ZeroPageX(self):

        self.cpu_set_flag('C')
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)

        self.memory_set(0x0100, 0x36)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0x02)

        self.execute()

        self.assertEquals(self.memory_fetch(0x0085), 0x05)


    def test_rol_Absolute(self):

        self.cpu_set_flag('C')
        self.cpu_pc(0x0100)

        self.memory_set(0x0100, 0x2e)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0084, 0x02)

        self.execute()

        self.assertEquals(self.memory_fetch(0x0084), 0x05)


    def test_rol_AbsoluteX(self):

        self.cpu_set_flag('C')
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)

        self.memory_set(0x0100, 0x3e)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0085, 0x02)

        self.execute()

        self.assertEquals(self.memory_fetch(0x0085), 0x05)


    def test_rol_c_flag_set(self):
        self.cpu_set_register('A', 0x80)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x2a)

        self.execute()

        self.assertTrue(self.cpu_flag('C'))

    def test_rol_c_flag_unset(self):
        self.cpu_set_register('A', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x2a)

        self.execute()

        self.assertFalse(self.cpu_flag('C'))


    def test_rol_z_flag_set(self):
        self.cpu_set_register('A', 0x00)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x2a)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))


    def test_rol_z_flag_unset(self):
        self.cpu_set_register('A', 0x02)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x2a)

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    def test_rol_n_flag_set(self):
        self.cpu_set_register('A', 0xfe)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x2a)

        self.execute()

        self.assertTrue(self.cpu_flag('N'))

    def test_rol_n_flag_unset(self):
        self.cpu_set_register('A', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x2a)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))


    # // ROR

    def test_ror_accumulator(self):
        self.cpu_set_flag('C')
        self.cpu_set_register('A', 0x08)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x6a)

        self.execute()

        self.assertEquals(self.cpu_register('A'), 0x84)

    def test_ror_zeropage(self):
        self.cpu_set_flag('C')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x66)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x08)

        self.execute()

        self.assertEquals(self.memory_fetch(0x0084), 0x84)

    def test_ror_zeropage_x(self):
        self.cpu_set_flag('C')
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x76)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0x08)

        self.execute()

        self.assertEquals(self.memory_fetch(0x0085), 0x84)

    def test_ror_absolute(self):
        self.cpu_set_flag('C')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x6e)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0084, 0x08)

        self.execute()

        self.assertEquals(self.memory_fetch(0x0084), 0x84)

    def test_ror_absolute_x(self):
        self.cpu_set_flag('C')
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x7e)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0085, 0x08)

        self.execute()

        self.assertEquals(self.memory_fetch(0x0085), 0x84)

    def test_ror_c_flag_set(self):
        self.cpu_set_register('A', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x6a)

        self.execute()

        self.assertTrue(self.cpu_flag('C'))

    def test_ror_c_flag_unset(self):
        self.cpu_set_register('A', 0x10)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x6a)

        self.execute()

        self.assertFalse(self.cpu_flag('C'))

    def test_ror_z_flag_set(self):
        self.cpu_set_register('A', 0x00)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x6a)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_ror_z_flag_unset(self):
        self.cpu_set_register('A', 0x02)
        self.cpu_pc(0x0100)

        self.memory_set(0x0100, 0x6a)

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    def test_ror_n_flag_set(self):
        self.cpu_set_flag('C')
        self.cpu_set_register('A', 0xfe)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x6a)

        self.execute()

        self.assertTrue(self.cpu_flag('N'))

    def test_ror_n_flag_unset(self):
        self.cpu_unset_flag('C')
        self.cpu_set_register('A', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x6a)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))


    # // JMP

    def test_jmp_absolute(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x4c)
        self.memory_set(0x0101, 0xff)
        self.memory_set(0x0102, 0x01)

        self.execute()

        self.assertEquals(self.cpu_register('PC'), 0x01ff)

    def test_jmp_indirect(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x6c)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x01)
        self.memory_set(0x0184, 0xff)
        self.memory_set(0x0185, 0xff)

        self.execute()

        self.assertEquals(self.cpu_register('PC'), 0xffff)

    # // JSR

    def test_jsr(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x20)
        self.memory_set(0x0101, 0xff)
        self.memory_set(0x0102, 0x01)

        self.execute()

        self.assertEquals(self.cpu_register('PC'), 0x01ff)
        #TODO: self.assertEquals(self.memory_fetch(0x01fd), 0x01)
        #TODO: self.assertEquals(self.memory_fetch(0x01fc), 0x02)

        self.cpu_pc(0x0100)

        self.memory_set(0x0100, 0x20) # JSR
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0084, 0x60) # RTS

        self.execute()
        self.execute()

        self.assertEquals(self.cpu_register('PC'), 0x0103)
        self.assertEquals(self.cpu_register('SP'), 0xfd)

        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x20) # JSR $0084
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0103, 0xa9) # LDA #$ff
        self.memory_set(0x0104, 0xff)
        self.memory_set(0x0105, 0x02) # illegal opcode
        self.memory_set(0x0084, 0x60) # RTS

        # TODO:    cpu.Run()
        # self.execute()
        # self.assertEquals(self.cpu_register('A'), 0xff)

    # // RTS

    def test_rts(self):
        self.cpu_pc(0x0100)
        self.cpu_push_word(0x0102)
        self.memory_set(0x0100, 0x60)

        self.execute()

        self.assertEquals(self.cpu_register('PC'), 0x0103)


    # // BCC

    def test_bcc(self):
        self.cpu_set_flag('C')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x90)

        cycles, _ = self.execute()

        self.assertEquals(cycles, 2)
        self.assertEquals(self.cpu_register('PC'), 0x0102)

        self.cpu_unset_flag('C')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x90)
        self.memory_set(0x0101, 0x02) # +2

        cycles, _ = self.execute()

        # TODO: self.assertEquals(cycles, 3)
        self.assertEquals(self.cpu_register('PC'), 0x0104)

        self.cpu_unset_flag('C')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x90)
        self.memory_set(0x0101, 0xfd) # -3

        cycles, _ = self.execute()

        # TODO: self.assertEquals(cycles, 4)
        self.assertEquals(self.cpu_register('PC'), 0x00ff)

    # // BCS

    def test_bcs(self):
        self.cpu_set_flag('C')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xb0)
        self.memory_set(0x0101, 0x02) # +2

        self.execute()

        self.assertEquals(self.cpu_register('PC'), 0x0104)
        self.cpu_set_flag('C')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xb0)
        self.memory_set(0x0101, 0xfe) # -2

        self.execute()

        self.assertEquals(self.cpu_register('PC'), 0x0100)

    # // BEQ

    def test_beq(self):
        self.cpu_set_flag('Z')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xf0)
        self.memory_set(0x0101, 0x02) # +2

        self.execute()

        self.assertEquals(self.cpu_register('PC'), 0x0104)

        self.cpu_set_flag('Z')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xf0)
        self.memory_set(0x0101, 0xfe) # -2

        self.execute()

        self.assertEquals(self.cpu_register('PC'), 0x0100)

    # // BMI

    def test_bmi(self):
        self.cpu_set_flag('N')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x30)
        self.memory_set(0x0101, 0x02) # +2

        self.execute()

        self.assertEquals(self.cpu_register('PC'), 0x0104)

        self.cpu_set_flag('N')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x30)
        self.memory_set(0x0101, 0xfe) # -2

        self.execute()

        self.assertEquals(self.cpu_register('PC'), 0x0100)

    # // BNE

    def test_bne(self):
        self.cpu_unset_flag('Z')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xd0)
        self.memory_set(0x0101, 0x02) # +2

        self.execute()

        self.assertEquals(self.cpu_register('PC'), 0x0104)

        self.cpu_unset_flag('Z')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xd0)
        self.memory_set(0x0101, 0xfe) # -2

        self.execute()

        self.assertEquals(self.cpu_register('PC'), 0x0100)

    # // BPL

    def test_bpl(self):

        self.cpu_unset_flag('N')
        self.cpu_pc(0x0100)

        self.memory_set(0x0100, 0x10)
        self.memory_set(0x0101, 0x02) # +2

        self.execute()

        self.assertEquals(self.cpu_register('PC'), 0x0104)

        self.cpu_unset_flag('N')
        self.cpu_pc(0x0100)

        self.memory_set(0x0100, 0x10)
        self.memory_set(0x0101, 0xfe) # -2

        self.execute()

        self.assertEquals(self.cpu_register('PC'), 0x0100)

    # // BVC

    def test_bvc(self):
        self.cpu_unset_flag('V')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x50)
        self.memory_set(0x0101, 0x02) # +2

        self.execute()

        self.assertEquals(self.cpu_register('PC'), 0x0104)
        self.cpu_unset_flag('V')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x50)
        self.memory_set(0x0101, 0xfe) # -2

        self.execute()

        self.assertEquals(self.cpu_register('PC'), 0x0100)

    # // BVS

    def test_bvs(self):
        self.cpu_set_flag('V')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x70)
        self.memory_set(0x0101, 0x02) # +2

        self.execute()

        self.assertEquals(self.cpu_register('PC'), 0x0104)

        self.cpu_set_flag('V')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x70)
        self.memory_set(0x0101, 0xfe) # -2

        self.execute()

        self.assertEquals(self.cpu_register('PC'), 0x0100)

    # // CLC

    def test_clc(self):
        self.cpu_unset_flag('C')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x18)

        self.execute()

        self.assertFalse(self.cpu_flag('C'))

        self.cpu_set_flag('C')
        self.cpu_pc(0x0100)

        self.memory_set(0x0100, 0x18)

        self.execute()

        self.assertFalse(self.cpu_flag('C'))

    # // CLD

    def test_Cld(self):
        self.cpu_unset_flag('D')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xd8)

        self.execute()

        self.assertFalse(self.cpu_flag('D'))

        return # TODO
        self.cpu_set_flag('D')
        self.cpu_pc(0x0100)

        self.memory_set(0x0100, 0xd8)

        self.execute()

        self.assertFalse(self.cpu_flag('D'))

    # // CLI

    def test_cli(self):
        self.cpu_unset_flag('I')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x58)

        self.execute()

        self.assertFalse(self.cpu_flag('I'))

        self.cpu_set_flag('I')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x58)

        self.execute()

        self.assertFalse(self.cpu_flag('I'))


    # // CLV

    def test_clv(self):
        self.cpu_unset_flag('V')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xb8)

        self.execute()

        self.assertFalse(self.cpu_flag('V'))

        self.cpu_set_flag('V')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xb8)

        self.execute()

        self.assertFalse(self.cpu_flag('V'))

    # // SEC

    def test_sec(self):
        self.cpu_unset_flag('C')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x38)

        self.execute()

        self.assertTrue(self.cpu_flag('C'))

        self.cpu_set_flag('C')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x38)

        self.execute()

        self.assertTrue(self.cpu_flag('C'))

    # // SED

    def test_sed(self):
        self.cpu_unset_flag('D')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xf8)

        self.execute()

        self.assertTrue(self.cpu_flag('D'))

        self.cpu_set_flag('D')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xf8)

        self.execute()

        self.assertTrue(self.cpu_flag('D'))

    # // SEI

    def test_sei(self):
        self.cpu_unset_flag('I')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x78)

        self.execute()

        self.assertTrue(self.cpu_flag('I'))

        self.cpu_set_flag('I')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x78)

        self.execute()

        self.assertTrue(self.cpu_flag('I'))


    # // BRK

    @skip('TODO')
    def test_brk(self):
        self.cpu_set_register('P', 0xff) # & (^B)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x00)
        self.memory_set(0xfffe, 0xff)
        self.memory_set(0xffff, 0x01)

        self.execute()

        self.assertEquals(self.cpu_pull_byte(), 0xff)

        self.assertEquals(self.cpu_pull_word(), 0x0102)

        self.assertEquals(self.cpu_register('PC'), 0x01ff)


    # // RTI

    @skip('TODO')
    def test_rti(self):
        self.cpu_pc(0x0100)
        self.cpu_push_word(0x0102)
        self.cpu_push_byte(0x03)
        self.memory_set(0x0100, 0x40)

        self.execute()

        self.assertEquals(self.cpu_register('P'), 0x23)
        self.assertEquals(self.cpu_register('PC'), 0x0102)


# // Rom

# def test_Rom(self):

#     cpu.DisableDecimalMode()

#     self.cpu_set_register('P', 0x24)
#     cpu.Registers.SP = 0xfd
#     cpu.Registers.PC = 0xc000

#     cpu.Memory.(*BasicMemory).load("test-roms/nestest/nestest.nes")

#     self.memory_set(0x4004, 0xff)
#     self.memory_set(0x4005, 0xff)
#     self.memory_set(0x4006, 0xff)
#     self.memory_set(0x4007, 0xff)
#     self.memory_set(0x4015, 0xff)

#     err := cpu.Run()

#     if err != nil {
#         switch err.(type) {
#         case BrkOpCodeError:
#         default:
#             t.Error("Error during Run\n")
#         }
#     }

#     self.assertEquals(self.memory_fetch(0x0002), 0x00)

#     self.assertEquals(self.memory_fetch(0x0003), 0x00)


    # // Irq

    @skip('TODO')
    def test_irq(self):
        self.cpu_set_register('P', 0xfb)
        self.cpu_pc(0x0100)
        cpu.Interrupt(Irq, true)
        self.memory_set(0xfffe, 0x40)
        self.memory_set(0xffff, 0x01)

        cpu.PerformInterrupts()

        # if cpu.pull() != 0xfb {
        #     t.Error("Memory is not 0xfb")
        # }

        # if cpu.pull16() != 0x0100 {
        #     t.Error("Memory is not 0x0100")
        # }

        self.assertEquals(self.cpu_register('PC'), 0x0140)

        # if cpu.GetInterrupt(Irq) {
        #     t.Error("Interrupt is set")
        # }


    # // Nmi

    @skip('TODO')
    def test_nmi(self):
        self.cpu_set_register('P', 0xff)
        self.cpu_pc(0x0100)
        cpu.Interrupt(Nmi, true)
        self.memory_set(0xfffa, 0x40)
        self.memory_set(0xfffb, 0x01)

        cpu.PerformInterrupts()

        # if cpu.pull() != 0xff {
        #     t.Error("Memory is not 0xff")
        # }

        # if cpu.pull16() != 0x0100 {
        #     t.Error("Memory is not 0x0100")
        # }

        self.assertEquals(self.cpu_register('PC'), 0x0140)

        # if cpu.GetInterrupt(Nmi) {
        #     t.Error("Interrupt is set")
        # }


    # // Rst

    @skip('TODO')
    def test_rst(self):

        self.cpu_pc(0x0100)

        cpu.Interrupt(Rst, true)
        self.memory_set(0xfffc, 0x40)
        self.memory_set(0xfffd, 0x01)

        # cpu.PerformInterrupts()

        self.assertEquals(self.cpu_register('PC'), 0x0140)

        # if cpu.GetInterrupt(Rst) {
        #     t.Error("Interrupt is set")
        # }
