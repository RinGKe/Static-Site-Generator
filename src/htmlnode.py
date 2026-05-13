class HTMLNode:
    def __init__(
        self,
        tag: str = None,
        value: str = None,
        children: [] = None,
        props: {} = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        result = ""
        if not self.props:
            return result
        for p in self.props:
            result += f' {p}="{self.props[p]}"'
        return result

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
