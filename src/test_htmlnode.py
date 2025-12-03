import unittest

from htmlnode import HtmlNode


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
