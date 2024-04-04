import unittest

from textnode import (
    TextNode,
    split_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_images,
    split_nodes_links,
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

    def test_split_delimiter_bold(self):
        node = TextNode("This is text with a **bolded** word", TEXT_TYPE_TEXT)

        want = [
            TextNode("This is text with a ", TEXT_TYPE_TEXT),
            TextNode("bolded", TEXT_TYPE_BOLD),
            TextNode(" word", TEXT_TYPE_TEXT),
        ]

        node2 = TextNode(
            "This is text with two **bolded** words, my **friend**", TEXT_TYPE_TEXT
        )

        want2 = [
            TextNode("This is text with two ", TEXT_TYPE_TEXT),
            TextNode("bolded", TEXT_TYPE_BOLD),
            TextNode(" words, my ", TEXT_TYPE_TEXT),
            TextNode("friend", TEXT_TYPE_BOLD),
        ]
        node3 = TextNode(
            "**This is text** with three **bolded** words, my **friend**",
            TEXT_TYPE_TEXT,
        )

        want3 = [
            TextNode("This is text", TEXT_TYPE_BOLD),
            TextNode(" with three ", TEXT_TYPE_TEXT),
            TextNode("bolded", TEXT_TYPE_BOLD),
            TextNode(" words, my ", TEXT_TYPE_TEXT),
            TextNode("friend", TEXT_TYPE_BOLD),
        ]
        delimiter = "**"
        got = split_delimiter([node], delimiter, TEXT_TYPE_BOLD)
        got2 = split_delimiter([node2], delimiter, TEXT_TYPE_BOLD)
        got3 = split_delimiter([node3], delimiter, TEXT_TYPE_BOLD)
        self.assertListEqual(got, want)
        self.assertListEqual(got2, want2)
        self.assertListEqual(got3, want3)

    def test_split_delimiter_code(self):
        node = TextNode("This is text with a `code` word", TEXT_TYPE_TEXT)

        want = [
            TextNode("This is text with a ", TEXT_TYPE_TEXT),
            TextNode("code", TEXT_TYPE_CODE),
            TextNode(" word", TEXT_TYPE_TEXT),
        ]

        node2 = TextNode(
            "This is text with two `code` words, my `friend`", TEXT_TYPE_TEXT
        )

        want2 = [
            TextNode("This is text with two ", TEXT_TYPE_TEXT),
            TextNode("code", TEXT_TYPE_CODE),
            TextNode(" words, my ", TEXT_TYPE_TEXT),
            TextNode("friend", TEXT_TYPE_CODE),
        ]
        delimiter = "`"

        got = split_delimiter([node], delimiter, TEXT_TYPE_CODE)
        got2 = split_delimiter([node2], delimiter, TEXT_TYPE_CODE)

        self.assertListEqual(got, want)
        self.assertListEqual(got2, want2)

    def test_split_delimiter_italic(self):
        node = TextNode("This is text with a *italic* word", TEXT_TYPE_TEXT)

        want = [
            TextNode("This is text with a ", TEXT_TYPE_TEXT),
            TextNode("italic", TEXT_TYPE_ITALIC),
            TextNode(" word", TEXT_TYPE_TEXT),
        ]

        node2 = TextNode(
            "This is text with two *italic* words, my *friend*", TEXT_TYPE_TEXT
        )

        want2 = [
            TextNode("This is text with two ", TEXT_TYPE_TEXT),
            TextNode("italic", TEXT_TYPE_ITALIC),
            TextNode(" words, my ", TEXT_TYPE_TEXT),
            TextNode("friend", TEXT_TYPE_ITALIC),
        ]
        delimiter = "*"

        got = split_delimiter([node], delimiter, TEXT_TYPE_ITALIC)
        got2 = split_delimiter([node2], delimiter, TEXT_TYPE_ITALIC)

        self.assertListEqual(got, want)
        self.assertListEqual(got2, want2)

    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfsdkjfd.png)"

        want = [
            ("image", "https://i.imgur.com/zjjcJKZ.png"),
            ("another", "https://i.imgur.com/dfsdkjfd.png"),
        ]

        got = extract_markdown_images(text)
        self.assertListEqual(got, want)

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        want = [
            ("link", "https://www.example.com"),
            ("another", "https://www.example.com/another"),
        ]

        got = extract_markdown_links(text)
        self.assertListEqual(got, want)

    def test_split_nodes_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TEXT_TYPE_TEXT,
        )

        node2 = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) with text that follows.",
            TEXT_TYPE_TEXT,
        )
        want = [
            TextNode("This is text with an ", TEXT_TYPE_TEXT),
            TextNode("image", TEXT_TYPE_IMAGE,
                     "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TEXT_TYPE_TEXT),
            TextNode(
                "second image", TEXT_TYPE_IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ]
        want2 = [
            TextNode("This is text with an ", TEXT_TYPE_TEXT),
            TextNode("image", TEXT_TYPE_IMAGE,
                     "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TEXT_TYPE_TEXT),
            TextNode(
                "second image", TEXT_TYPE_IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
            TextNode(" with text that follows.", TEXT_TYPE_TEXT),
        ]
        nodes = [node]
        nodes2 = [node2]

        got = split_nodes_images(nodes)
        self.assertListEqual(got, want)
        got2 = split_nodes_images(nodes2)
        self.assertListEqual(got2, want2)

    def test_split_nodes_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another) with text that follows."
        text2 = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        node = TextNode(
            text,
            TEXT_TYPE_TEXT,
        )

        node2 = TextNode(
            text2,
            TEXT_TYPE_TEXT,
        )
        want = [
            TextNode("This is text with a ", TEXT_TYPE_TEXT),
            TextNode("link", TEXT_TYPE_LINK, "https://www.example.com"),
            TextNode(" and ", TEXT_TYPE_TEXT),
            TextNode("another", TEXT_TYPE_LINK,
                     "https://www.example.com/another"),
            TextNode(" with text that follows.", TEXT_TYPE_TEXT),
        ]
        want2 = [
            TextNode("This is text with a ", TEXT_TYPE_TEXT),
            TextNode("link", TEXT_TYPE_LINK, "https://www.example.com"),
            TextNode(" and ", TEXT_TYPE_TEXT),
            TextNode("another", TEXT_TYPE_LINK,
                     "https://www.example.com/another"),
        ]
        nodes = [node]
        nodes2 = [node2]

        got = split_nodes_links(nodes)
        got2 = split_nodes_links(nodes2)
        self.assertListEqual(got, want)
        self.assertListEqual(got2, want2)


if __name__ == "__main__":
    unittest.main()
