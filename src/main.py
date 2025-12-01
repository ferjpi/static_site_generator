from textnode import TextNode, TextTypes


def main():
    print(TextNode("this is some anchor text", TextTypes.LINK, "https://www.boot.dev"))


if __name__ == "__main__":
    main()
