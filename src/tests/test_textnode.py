import unittest

from src.textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.ITALIC)
        node4 = TextNode("This is a text node", TextType.BOLD, None)

        self.assertEqual(node, node4)


class TestFunctions(unittest.TestCase):
    def test_text_to_html(self):
        textnode = TextNode("This is a text node", TextType.TEXT)
        boldnode = TextNode("This is a text node", TextType.BOLD)
        italicnode = TextNode("This is a text node", TextType.ITALIC)
        codenode = TextNode("This is a text node", TextType.CODE)
        linknode = TextNode("This is a text node", TextType.LINK, "www.google.com")
        imagenode = TextNode("This is a text node", TextType.IMAGE, "www.imagelink.com")

        html_node = text_node_to_html_node(textnode)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

        html_node = text_node_to_html_node(boldnode)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

        html_node = text_node_to_html_node(italicnode)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

        html_node = text_node_to_html_node(codenode)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")

        html_node = text_node_to_html_node(linknode)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {"href": "www.google.com"})

        html_node = text_node_to_html_node(imagenode)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props, {"src": "www.imagelink.com", "alt": "This is a text node"}
        )


if __name__ == "__main__":
    unittest.main()
