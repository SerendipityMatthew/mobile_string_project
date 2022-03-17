class TaileString:
    def __init__(self, module_name: str,
                 simplified_chinese: str, string_type=str,
                 android_src_path="",
                 string_id="",
                 default_lang="",
                 **languages):
        self.module_name = module_name
        self.android_src_path = android_src_path
        self.string_id = string_id
        #  字符串的类型，Android，或者是 iOS 字符串，
        self.string_type = string_type
        self.simplified_chinese = simplified_chinese
        self.default_lang = default_lang
        self.__dict__.update(languages)

    def __str__(self):
        string = ""
        for key in self.__dict__.keys():
            value = self.__dict__[key]
            if value is None:
                value = ""
            string = string + str(key) + " == " + str(value) + "\n"
        return string

    """
     先 根据 module_name 排序, 然后再根据 page_start 字段排序
    """

    def __lt__(self, other):
        if self.module_name < other.module_name:
            return True
        if self.module_name == other.module_name:
            if self.ios_id is None:
                return False
            if self.ios_id < other.ios_id:
                return True
            return False
