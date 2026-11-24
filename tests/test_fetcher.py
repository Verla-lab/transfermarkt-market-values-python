import unittest

from transfermarkt_values.fetcher import validate_limits


class LimitTests(unittest.TestCase):
    def test_rejects_short_delay(self):
        with self.assertRaises(ValueError):
            validate_limits(1.5, 1)

    def test_rejects_large_page_budget(self):
        with self.assertRaises(ValueError):
            validate_limits(3, 6)

    def test_accepts_safe_limits(self):
        validate_limits(2, 5)


if __name__ == "__main__":
    unittest.main()
