import unittest
from framalytics import read_xfmv

class TestReadXFMV(unittest.TestCase):
    def test_file_loading(self):
        # Test to ensure that files load without errors
        self.assertIsNotNone(read_xfmv('FRAM model-Stroke care system.xfmv'))

if __name__ == '__main__':
    unittest.main()