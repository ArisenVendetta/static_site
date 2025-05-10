class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list['HTMLNode'] = None, props: dict[str, str] = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props is None:
            return ""
        return ' ' + ' '.join([f'{k}="{v}"' for k, v in self.props.items()])
    
    def __repr__(self):
        print(f'tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props_to_html()}')


class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict[str, str] = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None or len(self.value) < 1:
            raise ValueError('all leaf nodes must have a value')
        if self.tag is None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list['HTMLNode'], props: dict[str, str] = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None or len(self.tag) < 1:
            raise ValueError('all parent nodes must have a tag')
        if self.children is None or len(self.children) < 1:
            raise ValueError('a parent node must have some children')
        
        return f'<{self.tag}{self.props_to_html()}>{''.join([child.to_html() for child in self.children])}</{self.tag}>'