import configparser

config = configparser.ConfigParser()
config.read('config.ini')
print(config.get('project', 'android_strings_files'))


def get_android_strings_files() -> list:
    return config.get('project', 'android_strings_files').split(",")


def get_ios_strings_files() -> list:
    return config.get('project', 'ios_strings_files').split(",")


def get_ios_project_path() -> str:
    return config.get('project', 'ios_project_path').strip("\n")


def get_android_project_path() -> str:
    return config.get('project', 'android_project_path').strip("\n")


def get_target_language() -> str:
    return config.get('project', 'target_language').strip("\n")


def get_generate_excel_file_name() -> str:
    return config.get('project', 'generate_excel_file_name').strip("\n")