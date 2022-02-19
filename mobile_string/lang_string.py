import os.path


class LangString:
    def __init__(self,
                 module_name: str = "",
                 string_id: str = "",
                 common_path: str = "",
                 lang_dir: str = "",
                 file_name: str = "",
                 content: str = ""
                 ):
        self.module_name = module_name
        self.string_id = string_id
        self.common_path = common_path
        self.lang_dir = lang_dir
        self.file_name = file_name
        self.content = content

    def get_full_path(self) -> str:
        """
        这个字符串相对于项目的全路径,
        :return:
        """
        return self.common_path + os.sep + self.lang_dir + os.sep + self.file_name

    def get_identity_key(self) -> str:
        """
        该字符串的独特 id, 是由 common_path 和 string_id 组成的字符串,
        拥有此 identity_key 的字符串将会被合并到一个共同 mobile_string, 组成一个全语言系列的字符串
        :return:
        """
        identity_key = self.common_path + "#" + self.string_id
        # print("get_identity_key: identity_key = ", identity_key)

        return identity_key

    def __str__(self):
        string = ""
        for key in self.__dict__.keys():
            value = self.__dict__[key]
            if value is None:
                value = ""
            string = string + str(key) + ": " + str(value) + "\n"
        return string
