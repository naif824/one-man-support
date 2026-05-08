import json
import tempfile
import unittest
from pathlib import Path

import bot


class OneManSupportTests(unittest.TestCase):
    def test_save_json_writes_readable_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"
            bot.save_json(path, {"hello": "world"})
            self.assertEqual(json.loads(path.read_text()), {"hello": "world"})

    def test_markdown_escape_handles_user_text(self):
        escaped = bot.md("hello _user_ [link](x)!")
        self.assertIn("\\_user\\_", escaped)
        self.assertIn("\\[link\\]", escaped)

    def test_admin_header_escapes_user_fields(self):
        class User:
            id = 12345
            first_name = "A_b"
            username = "user[name]"

        header = bot.build_admin_header({"name": "My_App", "emoji": "📱"}, User())
        self.assertIn("My\\_App", header)
        self.assertIn("A\\_b", header)
        self.assertIn("@user\\[name\\]", header)

    def test_app_label_has_defaults(self):
        self.assertEqual(bot.app_label({"name": "Support"}), "💬 Support")


if __name__ == "__main__":
    unittest.main()
