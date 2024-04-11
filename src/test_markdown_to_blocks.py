import unittest

from markdown_to_blocks import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        document = """
        This is **bolded** paragraph

        This is another paragraph with *italic* text and `code` here
        This is the same paragraph on a new line

        * This is a list
        * with items
        """
        want = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items",
        ]

        document2 = "This is one line"
        want2 = ["This is one line"]

        document3 = "This is two lines\n** I'm line two"
        want3 = ["This is two lines\n** I'm line two"]

        document4 = """
        
        This is on the second line.
        This is on the third line.

        This is on the fifth line.

        """

        want4 = [
            "This is on the second line.\nThis is on the third line.",
            "This is on the fifth line.",
        ]

        got = markdown_to_blocks(document)
        self.assertListEqual(got, want)
        got2 = markdown_to_blocks(document2)
        self.assertListEqual(got2, want2)
        got3 = markdown_to_blocks(document3)
        self.assertListEqual(got3, want3)
        got4 = markdown_to_blocks(document4)
        self.assertListEqual(got4, want4)


if __name__ == "__main__":
    unittest.main()
