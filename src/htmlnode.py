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
            return ''
        return ' ' + ' '.join([f'{k}="{v}"' for k, v in self.props.items()])
    
    def __repr__(self):
        child_string = '' if self.children is None else self.children
        value_string = '' if self.value is None else self.value
        tag_string = '' if self.tag is None else self.tag
        return f'tag: {tag_string}, value: {value_string}, children: {child_string}, props: {self.props_to_html()}'


class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict[str, str] = None):
        super().__init__(tag, value, None, props)

        if self.value is None or len(self.value) < 1:
            print(self)
            raise ValueError('all leaf nodes must have a value')


    def to_html(self):
        if self.value is None or len(self.value) < 1:
            print(self)
            raise ValueError('all leaf nodes must have a value')
        if self.tag is None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    
class ImageNode(HTMLNode):
    def __init__(self, src: str, alt_text: str = None, props: dict[str, str] = None):
        super().__init__('img', None, None, props)
        self.source = src
        self.alt_text = alt_text
        if self.props is None:
            self.props = {}
        self.props['src'] = self.source
        self.props['alt'] = self.alt_text

    def to_html(self):
        if self.source is None or len(self.source) < 1:
            raise ValueError('all image nodes must have a src')
        return f'<{self.tag}{self.props_to_html()}>'
    

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list['HTMLNode'], props: dict[str, str] = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None or len(self.tag) < 1:
            raise ValueError('all parent nodes must have a tag')
        if self.children is None or len(self.children) < 1:
            raise ValueError('a parent node must have some children')
        
        return f'<{self.tag}{self.props_to_html()}>{''.join([child.to_html() for child in self.children])}</{self.tag}>'