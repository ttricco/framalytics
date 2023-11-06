import unittest
from framalytics.visualize import visualize_network
from framalytics.xfmv_parser import parse_xfmv

class TestVisualize(unittest.TestCase):
    def test_visualization(self):
        # Setup your environment for testing (if needed)
        # Ensure that the visualization function works with given data
        data = parse_xfmv('FRAM model-Stroke care system.xfmv')
        fig, ax = visualize_network(data['function'], data['aspect'])
        self.assertIsNotNone(fig)
        self.assertIsNotNone(ax)

if __name__ == '__main__':
    unittest.main()
