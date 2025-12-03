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
