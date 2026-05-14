import unittest

from src.htmlnode import *


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode(
            "a",
            "Click me!",
            {"class": "greeting", "href": "https://google.com"},
        )
        node2 = LeafNode(
            "p",
            "This is a paragraph of text.",
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://google.com"',
        )
        self.assertEqual(
            node.to_html(),
            '<a class="greeting" href="https://google.com">Click me!</a>',
        )
        self.assertEqual(
            node2.to_html(),
            "<p>This is a paragraph of text.</p>",
        )

    def test_values(self):
        node = LeafNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = LeafNode(
            "p",
            "What a strange world",
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "LeafNode(p, What a strange world, {'class': 'primary'})",
        )


if __name__ == "__main__":
    unittest.main()
