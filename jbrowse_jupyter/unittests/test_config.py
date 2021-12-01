import unittest
from jbrowse_jupyter import JBrowseConfig

class TestConfig(unittest.TestCase):

    def __init__(self, config_obj):
        self.config_obj = config_obj

    def test_config(self):
        print('hi')
        # self.assertAlmostEqual(,8)
        # self.assertAlmostEqual(cuboid_volume(1),1)
        # self.assertAlmostEqual(cuboid_volume(0),0)
        # self.assertAlmostEqual(cuboid_volume(5.5),166.375)
    # def test_session(self):
    # def test_assembly(self):
    # def test_location(self):

if __name__ == "__main__":
    config_obj = JBrowseConfig()
    test = TestConfig(config_obj)
    test.test_config()
    # test.test_session()
    # test.test_assembly()
    # test.test_location()
        
