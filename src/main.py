from textnode import TextNode, TextType

def main():
    link = TextType.LINK
    new_node = TextNode("this is a test", link, "https://www.boot.dev")
    print(new_node)

main()