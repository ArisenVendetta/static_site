import unittest
from textnode import TextNode, TextType
from nodehelper import convert_text_node_to_html_node
from nodehelper import split_text_nodes_by


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode('This is a text node', TextType.BOLD)
        node2 = TextNode('This is a text node', TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode('This is a link node', TextType.LINK)
        node2 = TextNode('This is a link node', TextType.LINK, 'some_link')
        self.assertNotEqual(node, node2)

    def test_neq2(self):
        node = TextNode('This is a text node', TextType.BOLD)
        node2 = TextNode('This is another text node', TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = convert_text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_split_nodes(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_text_nodes_by([node], "`", TextType.CODE)

        check = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, check)


if __name__ == '__main__':
    unittest.main()