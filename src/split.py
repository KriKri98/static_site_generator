from textnode import TextType, TextNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

            
        text_blocks = node.text.split(delimiter)
        if len(text_blocks) % 2 == 0:
            raise Exception("Delimiter not correct in given Text")
        for i in range(0, len(text_blocks)):
            if text_blocks[i] == "":
                continue           
            text = True
            if i % 2 == 1:
                text = False
            
            if text == True:
                new_nodes.append(TextNode(text_blocks[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(text_blocks[i], text_type))


    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue        
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
        text_blocks = []
        for i in range(0, len(images)):
            if text_blocks == []:
                text_blocks = node.text.split(f"![{images[i][0]}]({images[i][1]})", 1)
            else:
                temp = text_blocks[-1].split(f"![{images[i][0]}]({images[i][1]})", 1)
                del text_blocks[-1]
                text_blocks.extend(temp)
        for i in range(0, len(text_blocks)):
            if text_blocks[i] != "":
                new_nodes.append(TextNode(text_blocks[i], TextType.TEXT))
            if i < len(images):
                new_nodes.append(TextNode(images[i][0], TextType.IMAGE, images[i][1]))
    return new_nodes



        


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
        text_blocks = []
        for i in range(0, len(links)):
            if text_blocks == []:
                text_blocks = node.text.split(f"[{links[i][0]}]({links[i][1]})", 1)
            else:
                temp = text_blocks[-1].split(f"[{links[i][0]}]({links[i][1]})", 1)
                del text_blocks[-1]
                text_blocks.extend(temp)
        for i in range(0, len(text_blocks)):
            if text_blocks[i] != "":
                new_nodes.append(TextNode(text_blocks[i], TextType.TEXT))
            if i < len(links):
                new_nodes.append(TextNode(links[i][0], TextType.LINK, links[i][1]))
    return new_nodes


def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    block = []
    for i in range(0, len(blocks)):
        block.append(blocks[i].strip())
        if block[i] == "":
            del block[-1]
    return block