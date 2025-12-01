import unittest

from textnode import TextNode, TextTypes


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextTypes.BOLD)
        node2 = TextNode("This is a text node", TextTypes.BOLD)
        self.assertEqual(node, node2)

    def test_ne(self):
        node = TextNode("This is a text node", TextTypes.LINK, "https://www.google.com")
        node2 = TextNode("This is a text node", TextTypes.BOLD)
        self.assertNotEqual(node, node2)

    def test_ne_links(self):
        node = TextNode("This is a text node", TextTypes.LINK, "https://www.google.com")
        node2 = TextNode("This is a text node", TextTypes.LINK, "http://www.google.com")
        self.assertNotEqual(node, node2)

    def test_link_without_link(self):
        node = TextNode("This is a text node", TextTypes.LINK)
        self.assertEqual(node.url, None)


if __name__ == "__main__":
    unittest.main()
