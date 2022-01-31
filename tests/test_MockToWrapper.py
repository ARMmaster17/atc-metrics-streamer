import unittest
from traffic_ops import MockToWrapper


class MockToWrapperTestCase(unittest.TestCase):
    def test_object_initalizes(self):
        mock = MockToWrapper.MockToWrapper()
        self.assertIsNotNone(mock, None)

    def test_wrapper_connects(self):
        mock = MockToWrapper.MockToWrapper()
        monitors = mock.get_traffic_monitors()


if __name__ == '__main__':
    unittest.main()
