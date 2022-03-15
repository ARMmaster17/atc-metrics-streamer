import unittest

from steps.BuildTOConnectionInfoStep import BuildTOConnectionInfoStep


class BuildTOConnectionInfoStepTests(unittest.TestCase):
    def test_step_initializes(self):
        step = BuildTOConnectionInfoStep(skip_connection=True)


if __name__ == '__main__':
    unittest.main()
