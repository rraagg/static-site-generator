from textnode import TextNode


def main():
   my_text_node = TextNode("This is a text node", "bold", "https://www.boot.dev")
   print(repr(my_text_node))

if __name__ == "__main__":
    main()
