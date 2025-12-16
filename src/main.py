from system_management import move_content
from utils import generate_page, generate_pages_recursive


def main():
    move_content("static", "public")
    # generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()
