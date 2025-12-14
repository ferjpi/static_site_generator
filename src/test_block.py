import unittest

from block import BlockType, block_to_block_type


class TestBlock(unittest.TestCase):
    def test_block_to_block_type(self):
        self.assertEqual(block_to_block_type("# heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("> quoting"), BlockType.QUOTE)
        self.assertEqual(
            block_to_block_type("- first elemetn"), BlockType.UNORDERED_LIST
        )
        self.assertEqual(
            block_to_block_type("1. first elemetn"), BlockType.ORDERED_LIST
        )
        self.assertEqual(block_to_block_type("```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("`"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("```python"), BlockType.CODE)
        self.assertEqual(
            block_to_block_type("This is a paragraph"), BlockType.PARAGRAPH
        )
