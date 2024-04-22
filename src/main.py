import os
import shutil
from generate_page import generate_page, generate_pages_recursive
from copystatic import copy_files_recursive


dir_path_static = "./static"
dir_path_public = "./public"
md_content_path = "./content/index.md"
template_path = "template.html"
destination_path = "./public/index.html"


def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)
    # generate_page(md_content_path, template_path, destination_path)
    generate_pages_recursive("./content", template_path, "./public")



if __name__ == "__main__":
    main()
