import re

from typing import List, Tuple
from block import BlockType, block_to_block_type
from textnode import TextNode, TextTypes


# it serves as an abstract class
class HtmlNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""
        return " ".join([f" {k}='{v}'" for k, v in self.props.items()])

    def __repr__(self):
        return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"


class LeafNode(HtmlNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")

        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HtmlNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("tag is required")

        if self.children is None:
            raise ValueError("children is required")

        children_html = []
        for child in self.children:
            children_html.append(child.to_html())

        content = "".join(children_html)

        props_str = self.props_to_html()
        return f"<{self.tag}{props_str}>{content}</{self.tag}>"


def text_node_to_html_node(text_node: TextNode):
    if text_node.text_type not in TextTypes:
        raise Exception("wrong text type")

    match text_node.text_type:
        case TextTypes.TEXT:
            return LeafNode(None, text_node.text)
        case TextTypes.BOLD:
            return LeafNode("b", text_node.text)
        case TextTypes.ITALIC:
            return LeafNode("i", text_node.text)
        case TextTypes.CODE:
            return LeafNode("code", text_node.text)
        case TextTypes.LINK:
            return LeafNode("a", text_node.text, props={"href": text_node.url})
        case TextTypes.IMAGE:
            return LeafNode(
                "img", "", props={"src": text_node.url, "alt": text_node.text}
            )


def split_nodes_delimiter(
    old_nodes: List[TextNode], delimiter: str, text_type: TextTypes
):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextTypes.TEXT:
            new_nodes.append(node)
        elif delimiter in node.text:
            split_values = node.text.split(delimiter)
            new_nodes.append(TextNode(split_values[0], TextTypes.TEXT))
            new_nodes.extend(TextNode(value, text_type) for value in split_values[1:-1])
            new_nodes.append(TextNode(split_values[-1], TextTypes.TEXT))
        else:
            new_nodes.append(node)

    return new_nodes


def extract_markdown_images(text: str) -> List[Tuple[str, str]]:
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_links(text: str) -> List[Tuple[str, str]]:
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches


def split_nodes_image(old_nodes: List[TextNode]) -> List[TextNode]:
    split_nodes = []

    for node in old_nodes:
        splitted_text = re.split(r"(!\[(?:.*?)\]\((?:.*?)\))", node.text)

        for text in splitted_text:
            if text == "":
                continue
            elif re.match(r"!\[.*?\]\(.*?\)", text):
                t, url = extract_markdown_images(text)[0]
                split_nodes.append(TextNode(t, TextTypes.IMAGE, url))
            else:
                split_nodes.append(TextNode(text, node.text_type, node.url))
    return split_nodes


def split_nodes_link(old_nodes: List[TextNode]) -> List[TextNode]:
    split_nodes = []

    for node in old_nodes:
        if node.text_type != TextTypes.TEXT:
            split_nodes.append(node)
            continue

        splitted_text = re.split(r"((?<!!)\[(?:.*?)\]\((?:.*?)\))", node.text)

        for text in splitted_text:
            if text == "" or not text:
                continue

            if text.startswith("!"):
                split_nodes.append(TextNode(text, TextTypes.TEXT))

            elif text.startswith("[") and text.endswith(")"):
                t, url = extract_markdown_links(text)[0]
                split_nodes.append(TextNode(t, TextTypes.LINK, url))
            else:
                split_nodes.append(TextNode(text, node.text_type, node.url))
    return split_nodes


def text_to_textnodes(text: str) -> List[TextNode]:
    node = TextNode(text, TextTypes.TEXT)
    nodes = [node]

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    nodes = split_nodes_delimiter(nodes, "`", TextTypes.CODE)
    nodes = split_nodes_delimiter(nodes, "_", TextTypes.ITALIC)
    nodes = split_nodes_delimiter(nodes, "**", TextTypes.BOLD)

    return nodes


def markdown_to_blocks(markdowns: str) -> List[str]:
    inlines = markdowns.split("\n\n")

    new_blocks = []

    for line in inlines:
        if not line:
            continue
        else:
            new_blocks.append(line.strip())

    return new_blocks


def text_to_textchildren(text: str) -> List[TextNode]:
    """
    Converts a text string to a list of TextNode objects
    """

    text_nodes = text_to_textnodes(text)

    children = []
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))

    return children


def block_to_html_node(block: str, block_type: BlockType) -> HtmlNode:
    """
    Converts a block of text to a HtmlNode object
    """
    if block_type == BlockType.PARAGRAPH:
        children = text_to_textchildren(block)
        return ParentNode("p", children)

    if block_type == BlockType.HEADING:
        level = block.count("#")
        text = block.lstrip("#").strip()
        children = text_to_textchildren(text)
        return ParentNode(f"h{level}", children)

    if block_type == BlockType.CODE:
        code_text = block.strip("`").strip()
        code_node = LeafNode("code", code_text)
        return ParentNode("pre", [code_node])

    if block_type == BlockType.QUOTE:
        text = block.lstrip(">").strip()
        children = text_to_textchildren(text)
        return ParentNode("blockquote", children)

    if block_type == BlockType.UNORDERED_LIST:
        list_items_text = block.split("\n")
        list_items = []
        for item in list_items_text:
            text = item.lstrip("-").strip()
            children = text_to_textchildren(text)
            list_items.append(ParentNode("li", children))
        return ParentNode("ul", list_items)

    if block_type == BlockType.ORDERED_LIST:
        list_items_text = block.split("\n")
        list_items = []
        for item in list_items_text:
            text = re.sub(r"^\d+\.\s*", "", item).strip()
            children = text_to_textchildren(text)
            list_items.append(ParentNode("li", children))
        return ParentNode("ol", list_items)

    raise ValueError(f"Unknown block type: {block_type}")


def markdown_to_html_node(markdowns: str) -> ParentNode:
    blocks = markdown_to_blocks(markdowns)
    block_nodes = []

    for block in blocks:
        if not block:
            continue
        type = block_to_block_type(block)
        html_node = block_to_html_node(block, type)
        block_nodes.append(html_node)

    return ParentNode("div", block_nodes)


def extract_title(markdowns: str) -> str:
    if not markdowns.startswith("# "):
        raise Exception("Markdown title must start with a title")

    return markdowns[2:].strip()
