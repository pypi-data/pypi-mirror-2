from khan.utils.testing import *

class TestDictTester(DictTester, TestCase):
    
    def setUp(self):
        self.store = dict(map(lambda x: (str(x), str(x)), range(100)))
        super(TestDictTester, self).setUp()

if __name__ == "__main__":
    unittest.main()

