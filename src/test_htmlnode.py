import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    test_node = HTMLNode(tag='a', props={'href': 'www.link.net', 'target': '_blank'})

    def test_prop_leading_space(self):
        props = self.test_node.props_to_html()
        self.assertEqual(props[0], ' ')

    def test_prop_format(self):
        formatted_props = self.test_node.props_to_html()
        self.assertEqual(len(formatted_props.lstrip().split(' ')), len(self.test_node.props))

    def test_missing_quotes(self):
        self.assertEqual(self.test_node.props_to_html().count('"'), len(self.test_node.props) * 2)


class TestLeafNode(unittest.TestCase):
    test_node = LeafNode(tag=None, value='This is just raw text')
    test_node2 = LeafNode('p', "What's that over there?", props={'div': '#center'})

    def test_leaf_raw_text(self):
        self.assertEqual(self.test_node.to_html(), self.test_node.value)

    def test_leaf_eq(self):
        self.assertNotEqual(self.test_node, self.test_node2)

    def test_leaf_to_html(self):
        self.assertEqual(self.test_node2.to_html(), '<p div="#center">What\'s that over there?</p>')


class TestParentNode(unittest.TestCase):
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

if __name__ == '__main__':
    unittest.main()