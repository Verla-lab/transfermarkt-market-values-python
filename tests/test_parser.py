from pathlib import Path
import unittest

from transfermarkt_values.parser import classify_access, parse_players

FIXTURES = Path(__file__).parents[1] / "fixtures"


class ParserTests(unittest.TestCase):
    def test_parses_two_players(self):
        html = (FIXTURES / "player-values.html").read_text(encoding="utf-8")
        players = parse_players(html)
        self.assertEqual(len(players), 2)
        self.assertEqual(players[0].player_id, "DEMO-PLAYER-1")
        self.assertEqual(players[0].market_value, "€18.00m")
        self.assertEqual(players[1].position, "Right Winger")
        self.assertEqual(players[0].age, 24)

    def test_normalizes_relative_url(self):
        html = (FIXTURES / "player-values.html").read_text(encoding="utf-8")
        player = parse_players(html)[0]
        self.assertEqual(player.url, "https://www.transfermarkt.com/demo-player-1/profil/spieler/1001")

    def test_optional_fields_can_be_missing(self):
        html = (
            '<table><tr data-player-id="DEMO-X">'
            '<td data-field="name">Name only</td></tr></table>'
        )
        player = parse_players(html)[0]
        self.assertIsNone(player.club)
        self.assertIsNone(player.age)
        self.assertIsNone(player.market_value)

    def test_detects_verification_page(self):
        html = (FIXTURES / "verification.html").read_text(encoding="utf-8")
        access = classify_access(html)
        self.assertEqual(access.status, "verification_required")
        self.assertTrue(access.manual_action_required)
        self.assertEqual(parse_players(html), [])


if __name__ == "__main__":
    unittest.main()
