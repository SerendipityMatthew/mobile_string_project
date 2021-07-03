class TaileString:
    def __init__(self, module_name: str,
                 simplified_chinese: str, english_us: str,
                 page_start="", isStringArray=False, android_src_path="", ios_module="",
                 android_id="", function_desc="",
                 default_lang="", ios_id="",
                 spanish="", french="", russia="",
                 korean="", japan="", germany=""):
        self.module_name = module_name
        self.ios_module = ios_module
        self.android_src_path = android_src_path
        self.page_start = page_start
        self.function_desc = function_desc
        self.isStringArray = isStringArray
        self.android_id = android_id
        self.ios_id = ios_id
        self.simplified_chinese = simplified_chinese
        self.default_lang = default_lang
        self.english_us = english_us
        self.spanish = spanish
        self.germany = germany
        self.french = french
        self.russia = russia
        self.korean = korean
        self.japan = japan

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
            if self.page_start is None:
                return False
            if self.page_start < other.page_start:
                return True
            return False
