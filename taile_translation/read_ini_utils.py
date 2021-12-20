import configparser

config = configparser.ConfigParser()
config.read('config.ini')
print(config.get('project', 'android_strings_files'))


def get_android_strings_files() -> list:
    return config.get('project', 'android_strings_files').split(",")


def get_ios_strings_files() -> list:
    return config.get('project', 'ios_strings_files').split(",")


