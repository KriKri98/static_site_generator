import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "this is a test", ["child1", "child2"], {"href": "https://www.google.com"})
        node2 = HTMLNode("p", "this is a test", ["child1", "child2"], {"href": "https://www.google.com"})
        self.assertEqual(node.tag, node2.tag)

    def test_eq2(self):
        node = HTMLNode("p")
        node2 = HTMLNode("p")
        self.assertEqual(node.value, node2.value)

    def test_neq(self):
        node = HTMLNode("p", "this is a test", ["child1", "child2"], {"href": "https://www.google.com"})
        node2 = HTMLNode("p", "this is a test", props={"href": "https://www.google.com"})
        self.assertNotEqual(node, node2)

    def test_neq2(self):
        node = HTMLNode("p", "this is a test", ["child1", "child2"], {"href": "https://www.google.com"})
        node2 = HTMLNode("p", "This is a test", ["child1", "child2"], {"href": "https://www.google.com"})
        self.assertNotEqual(node, node2)

    def test_eq3(self):
        node = HTMLNode("p", "this is a test", ["child1", "child2"], {"href": "https://www.google.com", "target": "_blank"})
        
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")    

    def test_leaf_to_html_p2(self):
        node = LeafNode("a", "Hello, world!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Hello, world!</a>')

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


if __name__ == "__main__":
    unittest.main()