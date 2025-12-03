from textnode import TextTypes


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


def text_node_to_html_node(text_node):
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
                "img", None, props={"src": text_node.url, "alt": text_node.text}
            )
