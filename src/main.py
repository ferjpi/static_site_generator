import sys
from system_management import move_content
from utils import generate_pages_recursive


def main():
    base_path = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] is not None else "/"
    move_content("static", "docs")
    generate_pages_recursive(base_path, "content", "template.html", "docs")


if __name__ == "__main__":
    main()
