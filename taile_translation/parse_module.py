import os

# settings_gradle_file = "/Volumes/Mathew/code/mxchip/develop_deye_android/settings.gradle"
project_path = "/Volumes/Mathew/code/mxchip/mxapp_smartplus_android/"


def parse_app_modules(project_settings_path):
    with open(project_settings_path) as f:
        settings_gradle_text = f.readlines()
    module_list = []
    for line in settings_gradle_text:
        if line.startswith("include"):
            """
            一个include 行包含多个模块名称, 或者一个模块
            """
            if line.__contains__(","):
                module_name_group = line.split(",")
                for name in module_name_group:
                    if name.__contains__("include"):
                        trimmed_name = name.split(":")[1].replace("\'", "").strip()
                        module_list.append(trimmed_name)
                    else:
                        trimmed_name = name.replace("\'", "").replace(":", "").replace("\"", "").strip()
                        module_list.append(trimmed_name)

            else:
                module_name = line.split(":")[1]
                module_name = module_name.replace("'", "").strip(" ").replace("\n", "")
                module_list.append(module_name)

    print("get the app all module in settings.gradle file, " + str(module_list))
    return module_list


def get_app_project_module():
    settings_gradle_file = project_path + "settings.gradle"
    module_list = parse_app_modules(settings_gradle_file)
    module_path_list = []
    for file_name in os.listdir(project_path):
        for module_name in module_list:
            if file_name.__eq__(module_name):
                module_path_list.append(module_name)
    print("get all the module the locate in this project path: " + str(module_path_list))
    return module_path_list


get_app_project_module()
