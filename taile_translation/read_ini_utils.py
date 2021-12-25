import configparser

config = configparser.ConfigParser()
config.read('config.ini')
print(config.get('project', 'android_strings_files'))


def get_common_string_files(properties: str):
    file_list = config.get('project', properties).split(",")
    wanted_file_list = []
    for file in file_list:
        if file is not None and file.strip("\n") != "":
            wanted_file_list.append(file)
    return wanted_file_list


def get_android_strings_files() -> list:
    return get_common_string_files("android_strings_files")


def get_ios_strings_files() -> list:
    return get_common_string_files("ios_strings_files")


def get_ios_project_path() -> str:
    return config.get('project', 'ios_project_path').strip("\n")


def get_android_project_path() -> str:
    return config.get('project', 'android_project_path').strip("\n")


def get_target_language() -> str:
    return config.get('project', 'target_language').strip("\n")


def get_generate_excel_file_name() -> str:
    return config.get('project', 'generate_excel_file_name').strip("\n")


if __name__ == "__main__":
    print("get_android_strings_files() ", get_android_strings_files())
    print("get_ios_strings_files() ", get_ios_strings_files())
