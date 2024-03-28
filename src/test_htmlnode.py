import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p")
        node2 = HTMLNode("p")
        self.assertEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode(
            "p",
            "A paragraph",
            [],
            {"href": "https://www.google.com", "target": "_blank"},
        )
        html_string = node.props_to_html()
        want = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(html_string, want)


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})

        got = node.to_html()
        got2 = node2.to_html()

        want = "<p>This is a paragraph of text.</p>"
        want2 = '<a href="https://www.google.com">Click me!</a>'

        self.assertEqual(got, want)
        self.assertEqual(got2, want2)


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        got = node.to_html()
        want = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(got, want)

    def test_to_html_nested(self):
        node = ParentNode(
            "p",
            [
                ParentNode(
                    "div",
                    [
                        LeafNode(
                            "b",
                            "Bold text",
                        ),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ],
                    {"class": "my-div"},
                )
            ],
        )

        got = node.to_html()
        want = '<p><div class="my-div"><b>Bold text</b>Normal text<i>italic text</i>Normal text</div></p>'
        self.assertEqual(got, want)
