import unittest
from framalytics.xfmv_parser import parse_xfmv

class TestParseXFMV(unittest.TestCase):
    def test_parse(self):
        # Assuming parse_xfmv returns a dictionary of dataframes
        result = parse_xfmv('FRAM model-Stroke care system.xfmv')
        self.assertIn('function', result)
        self.assertIn('input', result)
        self.assertIn('aspect', result)

        # Check the type of data returned
        for key, df in result.items():
            self.assertIsInstance(df, pd.DataFrame)

if __name__ == '__main__':
    unittest.main()
