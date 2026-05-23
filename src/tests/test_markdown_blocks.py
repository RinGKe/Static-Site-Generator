import unittest

from src.markdown_blocks import *


class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "####### heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "~~~\ncode\n~~~"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "~~~\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "```\ncode```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "```code```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "> quote\nmore quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "- list\n-items"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "1. list\n2.items"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "1. list\n3. items"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
