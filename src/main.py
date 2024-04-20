import os
import shutil


def main():
    copy_src_to_public("static", "public")


def copy_src_to_public(from_directory, to_directory):
    current_from_directory = os.path.join("./", from_directory)
    current_to_directory = os.path.join("./", to_directory)
    if os.path.exists(current_to_directory):
        shutil.rmtree(current_to_directory)
    more_directories = []
    if os.path.exists(current_from_directory):
        contents = os.listdir(current_from_directory)
        for item in contents:
            if os.path.isfile(os.path.join(current_from_directory, item)):
                if os.path.exists(current_to_directory):
                    shutil.copy(
                        os.path.join(current_from_directory, item),
                        os.path.join(current_to_directory, item),
                    )
                else:
                    os.mkdir(current_to_directory)
                    shutil.copy(
                        os.path.join(current_from_directory, item),
                        os.path.join(current_to_directory, item),
                    )
            else:
                more_directories.append(item)
        for directory in more_directories:
            return copy_src_to_public(
                os.path.join(current_from_directory.lstrip("./"), directory),
                os.path.join(current_to_directory.lstrip("./"), directory),
            )


if __name__ == "__main__":
    main()
