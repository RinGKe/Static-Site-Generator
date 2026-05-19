import unittest

from src.inline_markdown import *
from src.textnode import *


class TestInlineMarkdown(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        textnode = TextNode("This is just text", TextType.TEXT)
        errornode = TextNode(
            "This is and **non-error** but this is a *error** delimiter",
            TextType.TEXT,
        )
        boldnode = TextNode("This is text with a **bold** word", TextType.TEXT)
        multibold = TextNode(
            "This is text with a **bold** word and another **bolder** word too",
            TextType.TEXT,
        )
        italicnode = TextNode("This is text with a __italic__ word", TextType.TEXT)
        multiitalic = TextNode(
            "This is text with a __italic__ word and another __italicer__ word too",
            TextType.TEXT,
        )
        bothnode = TextNode(
            "This is text with a __italic__ word and a **bold** word too",
            TextType.TEXT,
        )

        new_boldnodes = split_nodes_delimiter(
            [textnode, boldnode, multibold, bothnode], "**", TextType.BOLD
        )
        self.assertEqual(
            new_boldnodes,
            [
                TextNode("This is just text", TextType.TEXT, None),
                TextNode("This is text with a ", TextType.TEXT, None),
                TextNode("bold", TextType.BOLD, None),
                TextNode(" word", TextType.TEXT, None),
                TextNode("This is text with a ", TextType.TEXT, None),
                TextNode("bold", TextType.BOLD, None),
                TextNode(" word and another ", TextType.TEXT, None),
                TextNode("bolder", TextType.BOLD, None),
                TextNode(" word too", TextType.TEXT, None),
                TextNode(
                    "This is text with a __italic__ word and a ", TextType.TEXT, None
                ),
                TextNode("bold", TextType.BOLD, None),
                TextNode(" word too", TextType.TEXT, None),
            ],
        )

        new_italicnodes = split_nodes_delimiter(
            [textnode, italicnode, multiitalic, bothnode], "__", TextType.ITALIC
        )
        self.assertEqual(
            new_italicnodes,
            [
                TextNode("This is just text", TextType.TEXT, None),
                TextNode("This is text with a ", TextType.TEXT, None),
                TextNode("italic", TextType.ITALIC, None),
                TextNode(" word", TextType.TEXT, None),
                TextNode("This is text with a ", TextType.TEXT, None),
                TextNode("italic", TextType.ITALIC, None),
                TextNode(" word and another ", TextType.TEXT, None),
                TextNode("italicer", TextType.ITALIC, None),
                TextNode(" word too", TextType.TEXT, None),
                TextNode("This is text with a ", TextType.TEXT, None),
                TextNode("italic", TextType.ITALIC, None),
                TextNode(" word and a **bold** word too", TextType.TEXT, None),
            ],
        )

        with self.assertRaises(Exception):
            new_errors = split_nodes_delimiter([errornode], "**", TextType.BOLD)

    def test_extract_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

        matches2 = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a second ![image2](https://i.imgur.com/zjjcJKZ2.png)"
        )
        self.assertListEqual(
            [
                ("image", "https://i.imgur.com/zjjcJKZ.png"),
                ("image2", "https://i.imgur.com/zjjcJKZ2.png"),
            ],
            matches2,
        )

    def test_extract_links(self):
        matches = extract_markdown_links(
            "This is text with a [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

        matches2 = extract_markdown_links(
            "This is text with a [to boot dev](https://www.boot.dev) and another [to google](https://www.google.com)"
        )
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to google", "https://www.google.com"),
            ],
            matches2,
        )
