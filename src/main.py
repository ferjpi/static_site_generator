from textnode import TextNode, TextTypes

from system_management import move_content


def main():
    print(TextNode("this is some anchor text", TextTypes.LINK, "https://www.boot.dev"))
    move_content("static", "public")


if __name__ == "__main__":
    main()
