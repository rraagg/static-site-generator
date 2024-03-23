import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p")
        node2 = HTMLNode("p")
        self.assertEqual(node, node2)


    def test_props_to_html(self):
        node = HTMLNode("p", "A paragraph", [], {"href": "https://www.google.com", "target": "_blank"})
        html_string = node.props_to_html()
        want = " href=\"https://www.google.com\" target=\"_blank\""
        self.assertEqual(html_string, want)
        

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})

        got = node.to_html()
        got2 = node2.to_html()

        want = "<p>This is a paragraph of text.</p>"
        want2 = "<a href=\"https://www.google.com\">Click me!</a>"

        self.assertEqual(got, want)
        self.assertEqual(got2, want2)

