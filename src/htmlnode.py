class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props


    def __eq__(self, other):
        return (self.tag == other.tag
                and self.value == other.value
                and self.children == other.children
                and self.props == other.props)


    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


    def to_html(self):
        raise NotImplemented("Not implemented")


    def props_to_html(self):
        if self.props:
            html_string = ""
            for key, value in self.props.items():
                html_string = f"{html_string} {key}=\"{value}\""
            return html_string


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)


    def to_html(self):
        if not self.value:
            raise ValueError("All leaf nodes require a value")
        if not self.tag:
            return self.value
        if self.props:
            props_string = self.props_to_html()
            print(f"Props String: {props_string}")
            return f"<{self.tag}{props_string}>{self.value}</{self.tag}>" 
        return f"<{self.tag}>{self.value}</{self.tag}>"
