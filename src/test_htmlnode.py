import unittest

from htmlnode import HtmlNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextTypes as TextType


class TestHtmlNode(unittest.TestCase):
    def test_to_html(self):
        node = HtmlNode(tag="div", value="hello")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html(self):
        node = HtmlNode(tag="div", value="hello", props={"class": "foo"})

        self.assertEqual(node.props_to_html(), " class='foo'")

    def test_without_prosp(self):
        node = HtmlNode(tag="div", value="hello")

        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        node = HtmlNode(tag="div", value="hello", props={"class": "foo"})

        self.assertEqual(repr(node), "<div  class='foo'>hello</div>")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node2.to_html(), "<a href='https://www.google.com'>Click me!</a>"
        )

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
