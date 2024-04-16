import unittest

from block_to_html import markdown_to_html_node

from htmlnode import ParentNode, LeafNode


class TestBlockToHtml(unittest.TestCase):
    def test_paragraph_to_html(self):
        my_paragraph = """
        This is my paragraph.
        It has two lines.
        """

        got_paragraph = markdown_to_html_node(my_paragraph)

        want = ParentNode(
            "div", [LeafNode("p", "This is my paragraph.\nIt has two lines.")]
        )

        self.assertEqual(got_paragraph.to_html(), want.to_html())

    def test_quote_to_html(self):
        my_quote = """
        > Quote me on this.
        > Quote me on this.
        > Quote me on this.
        """

        got_quote = markdown_to_html_node(my_quote)

        want = ParentNode(
            "div",
            [
                LeafNode(
                    "blockquote",
                    "Quote me on this.\nQuote me on this.\nQuote me on this.",
                )
            ],
        )

        self.assertEqual(got_quote.to_html(), want.to_html())

    def test_code_to_html(self):
        my_code = """
        ```
        x = 2
        print(x)
        ```
        """

        got_code = markdown_to_html_node(my_code)

        want = ParentNode(
            "div", [ParentNode(
                "pre", [LeafNode("code", "\nx = 2\nprint(x)\n")])]
        )

        self.assertEqual(got_code.to_html(), want.to_html())

    def test_ordered_list_to_html(self):
        my_ordered_list = """
        1. One
        2. Two
        3. Three
        """

        got_ordered_list = markdown_to_html_node(my_ordered_list)

        want = ParentNode(
            "div",
            [
                ParentNode(
                    "ol",
                    [
                        LeafNode("li", "One"),
                        LeafNode("li", "Two"),
                        LeafNode("li", "Three"),
                    ],
                )
            ],
        )

        self.assertEqual(got_ordered_list.to_html(), want.to_html())

    def test_unordered_list_to_html(self):
        my_unordered_list = """
        * One
        * Two
        * Three
        """

        got_unordered_list = markdown_to_html_node(my_unordered_list)

        want = ParentNode(
            "div",
            [
                ParentNode(
                    "ul",
                    [
                        LeafNode("li", "One"),
                        LeafNode("li", "Two"),
                        LeafNode("li", "Three"),
                    ],
                )
            ],
        )

        self.assertEqual(got_unordered_list.to_html(), want.to_html())


if __name__ == "__main__":
    unittest.main()
