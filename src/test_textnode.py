import unittest

from textnode import (
    TextNode,
    TEXT_TYPE_TEXT,
    TEXT_TYPE_BOLD,
    TEXT_TYPE_ITALIC,
    TEXT_TYPE_CODE,
    TEXT_TYPE_IMAGE,
    TEXT_TYPE_LINK,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TEXT_TYPE_TEXT)
        node2 = TextNode("This is a text node", TEXT_TYPE_TEXT)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", TEXT_TYPE_TEXT)
        node2 = TextNode("This is a text node", TEXT_TYPE_BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", TEXT_TYPE_TEXT)
        node2 = TextNode("This is a text node2", TEXT_TYPE_TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node",
                        TEXT_TYPE_ITALIC, "https://www.boot.dev")
        node2 = TextNode(
            "This is a text node", TEXT_TYPE_ITALIC, "https://www.boot.dev"
        )
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TEXT_TYPE_TEXT,
                        "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )


if __name__ == "__main__":
    unittest.main()
