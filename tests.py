import unittest
from validator import Validator


class ValidatorTests(unittest.TestCase):
    def test_camel_case_split(self):
        self.assertListEqual(Validator.camel_case_split('aaaBbbCcc123'), ['aaa', 'Bbb', 'Ccc', '123'])
        self.assertListEqual(Validator.camel_case_split('faceId1'), ['face', 'Id', '1'])


if __name__ == '__main__':
    unittest.main()
