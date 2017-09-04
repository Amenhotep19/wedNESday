from __future__ import print_function

from unittest import TestCase
from unittest import SkipTest

from py65.devices.mpu6502 import MPU
from wednesday.bridge import Py65CPUBridge
from wednesday.tests.cpu_6502_spec import CPU6502Spec


class Py65CPUTest(Py65CPUBridge, CPU6502Spec, TestCase):

    def setUp(self):
        self.cpu = MPU()
        print(self.cpu)

    def tearDown(self):
        print(self.cpu)
