class MobileString:
    def __init__(self,
                 module_name: str,
                 zh_cn="",
                 zh_cn_file="",
                 string_id="",

                 english_us="",
                 english_us_file="",

                 isStringArray=False,
                 is_android_string=False, is_ios_string=False,
                 default_lang="",

                 zh_tw="",
                 zh_tw_file="",

                 spanish="",
                 spanish_file="",

                 french="",
                 french_file="",

                 russia="",
                 russia_file="",

                 korean="",
                 korean_file="",

                 japan="",
                 japan_file="",

                 germany="",
                 germany_file="",

                 ):
        self.module_name = module_name
        self.string_id = string_id
        self.isStringArray = isStringArray

        self.default_lang = default_lang

        self.is_android_string = is_android_string
        self.is_ios_string = is_ios_string

        self.zh_cn = zh_cn
        self.zh_cn_file = zh_cn_file

        self.zh_tw = zh_tw
        self.zh_tw_file = zh_tw_file

        self.english_us = english_us
        self.english_us_file = english_us_file

        self.spanish = spanish
        self.spanish_file = spanish_file

        self.germany = germany
        self.germany_file = germany_file

        self.french = french
        self.french_file = french_file

        self.russia = russia
        self.russia_file = russia_file

        self.korean = korean
        self.korean_file = korean_file

        self.japan = japan
        self.japan_file = japan_file

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
