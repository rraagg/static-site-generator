import unittest

from block_types import (
    block_to_block_type,
    BLOCK_TYPE_PARAGRAPH,
    BLOCK_TYPE_HEADING,
    BLOCK_TYPE_CODE,
    BLOCK_TYPE_QUOTE,
    BLOCK_TYPE_ORDERED_LIST,
    BLOCK_TYPE_UNORDERED_LIST,
)

from markdown_to_blocks import markdown_to_blocks


class TestBlockTypes(unittest.TestCase):
    def test_headings(self):
        my_heading_block = "### R"
        got_heading = block_to_block_type(my_heading_block)
        self.assertEqual(got_heading, BLOCK_TYPE_HEADING)

        my_paragraph_block = "### "
        got_paragraph = block_to_block_type(my_paragraph_block)
        self.assertEqual(got_paragraph, BLOCK_TYPE_PARAGRAPH)

    def test_code(self):
        my_code_block = "``` Code for you ```"
        got_code = block_to_block_type(my_code_block)
        self.assertEqual(got_code, BLOCK_TYPE_CODE)

        my_paragraph_block = "``` Not a code block"
        got_paragraph = block_to_block_type(my_paragraph_block)
        self.assertEqual(got_paragraph, BLOCK_TYPE_PARAGRAPH)

    def test_quote(self):
        my_quote_block = """
        > This is a quote
        > This is more quote
        > This is the final quote
        """
        stripped = markdown_to_blocks(my_quote_block)

        got_quote = block_to_block_type("\n".join(stripped))
        self.assertEqual(got_quote, BLOCK_TYPE_QUOTE)

    def test_ordered_list(self):
        my_ordered_list = """
        1. One
        2. Two
        3. Three
        """

        stripped = markdown_to_blocks(my_ordered_list)
        got_ordered_list = block_to_block_type("\n".join(stripped))
        self.assertEqual(got_ordered_list, BLOCK_TYPE_ORDERED_LIST)

        my_paragraph_block = """
        1. One
        2. Two
        4. Four
        """

        invalid = markdown_to_blocks(my_paragraph_block)
        got_paragraph = block_to_block_type("\n".join(invalid))
        self.assertEqual(got_paragraph, BLOCK_TYPE_PARAGRAPH)

    def test_unordered_list(self):
        my_asterisk_list = """
        * Human
        * Dog
        * Cat
        """

        asterisk = markdown_to_blocks(my_asterisk_list)
        got_asterisk_unordered_list = block_to_block_type("\n".join(asterisk))
        self.assertEqual(got_asterisk_unordered_list,
                         BLOCK_TYPE_UNORDERED_LIST)

        my_dash_list = """
        - Human
        - Dog
        - Cat
        """

        dash = markdown_to_blocks(my_dash_list)
        got_dash_unordered_list = block_to_block_type("\n".join(dash))
        self.assertEqual(got_dash_unordered_list, BLOCK_TYPE_UNORDERED_LIST)


if __name__ == "__main__":
    unittest.main()
