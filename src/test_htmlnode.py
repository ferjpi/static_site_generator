import unittest

from htmlnode import (
    HtmlNode,
    LeafNode,
    ParentNode,
    markdown_to_blocks,
    markdown_to_html_node,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_node_to_html_node,
    extract_markdown_images,
    extract_markdown_links,
    text_to_textnodes,
)
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
        if html_node is None:
            self.fail("html_node is not a LeafNode")

        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_split_text_nodes(self):
        node = TextNode("This is a text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is a text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_keeping_other_nodes(self):
        node = TextNode(
            "This is a **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",
            TextType.TEXT,
        )

        new_nodes = [node]

        new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)

        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(
                    " and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",
                    TextType.TEXT,
                ),
            ],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

        matched_images = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![alt text](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [
                ("image", "https://i.imgur.com/zjjcJKZ.png"),
                ("alt text", "https://i.imgur.com/zjjcJKZ.png"),
            ],
            matched_images,
        )

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.google.com)"
        )

        self.assertListEqual([("link", "https://www.google.com")], matches)

    def test_split_nodes_link(self):
        node = TextNode(
            "This is a text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("This is a text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_link_keeping_other_nodes(self):
        node = TextNode(
            "This is a text with a link [to boot dev](https://www.boot.dev) and ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("This is a text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(
                    " and ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_image(self):
        node = TextNode(
            "This is a text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![second image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("This is a text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_image_keeping_other_nodes(self):
        node = TextNode(
            "This is a text with an ![image](https://i.imgur.com/zjjcJKZ.png) and [link](https://google.com)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("This is a text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and [link](https://google.com)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        list_node = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )

        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            list_node,
        )

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

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph text in a p tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain the **same** even with inline stuff</code></pre></div>",
        )

    # def test_paragraphs(self):
    #     md = """
    # This is **bolded** paragraph
    # text in a p
    # tag here
    #
    # This is another paragraph with _italic_ text and `code` here
    #
    # """
    #
    #     node = markdown_to_html_node(md)
    #     html = node.to_html()
    #     self.assertEqual(
    #         html,
    #         "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    #     )
    #
    # def test_codeblock(self):
    #     md = """
    # ```
    # This is text that _should_ remain
    # the **same** even with inline stuff
    # ```
    # """
    #
    #     node = markdown_to_html_node(md)
    #     html = node.to_html()
    #     self.assertEqual(
    #         html,
    #         "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    #     )
