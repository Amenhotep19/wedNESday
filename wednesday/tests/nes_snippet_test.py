from unittest import TestCase
from unittest import skip

from nesasm.compiler import lexical, semantic, syntax, Cartridge
from wednesday.tests.py65_cpu_test import Py65CPUBridge
from py65.devices.mpu6502 import MPU


class NesSnippetsTest(Py65CPUBridge, TestCase):

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

    def test_wait_vblank(self):
        code = '''
            WAITVBLANK:
              BIT $2002
              BPL WAITVBLANK
              RTS
        '''

        self.load_program(code)

        self.execute()
        self.assertEquals(0x103, self.cpu.pc)
        self.execute()
        self.assertEquals(0x100, self.cpu.pc)
        self.execute()
        self.assertEquals(0x103, self.cpu.pc)
        # self.memory_set(0x2002, 0b11111111)
        # print self.memory_fetch(0x2002)
        self.cpu_set_flag('N') # WaitVBlank
        self.execute()
        self.assertEquals(0x105, self.cpu.pc)

    def test_reset(self):
        code = '''
            RESET:
              SEI
              CLD
              LDX #$40
              STX $4017
              LDX #$FF
              TXS
              INX
              STX $2000
              STX $2001
              STX $4010
        '''
        self.load_program(code)
        self.run_program()

        self.assertEquals(0x40, self.memory_fetch(0x4017))
        # self.assertEquals(0xff, self.cpu_pull_byte())

        self.assertEquals(self.cpu_register('X'), self.memory_fetch(0x2000))
        self.assertEquals(self.cpu_register('X'), self.memory_fetch(0x2001))
        self.assertEquals(self.cpu_register('X'), self.memory_fetch(0x4010))


    def test_clearmem(self):
        code = '''
            CLEARMEM:
              LDA #$00
              STA $0000, x
              STA $0100, x
              STA $0200, x
              STA $0400, x
              STA $0500, x
              STA $0600, x
              STA $0700, x
              LDA #$FE
              STA $0300, x
              INX
              BNE CLEARMEM
        '''

        self.load_program(code)
        # TODO self.run_program()

    def test_load_palettes(self):
        code = '''
            LoadPalettes:
              LDA $2002             ; Reset PPU, start writing
              LDA #$3F
              STA $2006             ; High byte = $3F00
              LDA #$00
              STA $2006             ; Low byte = $3F00
              LDX #$00
            LoadPalettesIntoPPU:
              LDA palette, x
              STA $2007
              INX
              CPX #32
              BNE LoadPalettesIntoPPU
            JMP done

            palette:
              .db $0F,$01,$02,$03,$04,$05,$06,$07,$08,$09,$0A,$0B,$0C,$0D,$0E,$0F
              .db $0F,$30,$31,$32,$33,$35,$36,$37,$38,$39,$3A,$3B,$3C,$3D,$3E,$0F

            done:
              RTS
        '''

        self.load_program(code)
        self.run_program()

        self.assertEquals(0x00, self.memory_fetch(0x2006))
        self.assertEquals(self.cpu_register('X'), 32)
        self.assertEquals(0x0f, self.memory_fetch(0x2007))

    def test_load_sprites(self):
        code = '''
            LoadSprites:
              LDX #$00
            LoadSpritesIntoPPU:
              LDA sprites, x
              STA $0200, x
              INX
              CPX #4                  ; Hex 20 = 32 decimal
              BNE LoadSpritesIntoPPU
            JMP done

            sprites:
              .db $80, $00, $03, $80; Y pos, tile id, attributes, X pos

            done:
              RTS
        '''

        self.load_program(code)
        self.run_program()

        self.assertEquals(self.cpu_register('A'), 0x80)
        self.assertEquals(self.cpu_register('X'), 4)
        self.assertEquals(0x80, self.memory_fetch(0x0200))
        self.assertEquals(0x00, self.memory_fetch(0x0201))
        self.assertEquals(0x03, self.memory_fetch(0x0202))
        self.assertEquals(0x80, self.memory_fetch(0x0203))
