import threading
import time
import unittest

from collections import namedtuple

from fawnlog import flashlib
from fawnlog.flash_unit import FlashUnit
from fawnlog import utils

from test import config


Measure = namedtuple("Measure", ["timestamp"])
OffsetMessage = namedtuple("OffsetMessage", ["measure", "is_full", "offset"])


data = "abc"
data_id = "id_1"
offset = 1
measure = Measure(utils.nanotime())
msg = OffsetMessage(measure, is_full=False, offset=1)
full_msg = OffsetMessage(None, is_full=True, offset=-1)


class TestFlashUnit(unittest.TestCase):

    def setUp(self):
        self.flash_unit = FlashUnit(0, config)
        self.flash_unit.reset()

    def tearDown(self):
        self.flash_unit.close()

    def test_write_offset_write(self):
        self.flash_unit.write_offset(data_id, msg)
        self._write_and_assert()

    def test_write_write_offset(self):
        threading.Timer(.1, self._write_offset).start()
        self._write_and_assert()

    def test_write_is_full(self):
        self.flash_unit.write_offset(data_id, full_msg)
        self.assertRaises(flashlib.ErrorNoCapacity,
                self.flash_unit.write, data_id, data)

    def test_read_hole_timeout(self):
        measure = Measure(utils.nanotime())
        msg = OffsetMessage(measure, is_full=False, offset=1)
        self.flash_unit.write_offset(data_id, msg)
        time.sleep(config.FLASH_HOLE_DELAY_THRESHOLD)
        self.assertRaises(flashlib.ErrorFilledHole, self.flash_unit.read,
                offset)
        self.assertRaises(flashlib.ErrorFilledHole, self.flash_unit.write,
                data_id, data)

    def _write_offset(self):
        self.flash_unit.write_offset(data_id, msg)

    def _write_and_assert(self):
        test_measure = self.flash_unit.write(data_id, data)
        self.assertEqual(measure, test_measure)
        test_data = self.flash_unit.read(offset)
        self.assertEqual(data, test_data)


if __name__ == "__main__":
    unittest.main()
