from lang_string import LangString


class MobileString:
    def __init__(self,
                 module_name: str,
                 string_id: str,
                 zh_cn: LangString = None,
                 english_us: LangString = None,

                 isStringArray=False,
                 is_android_string=False, is_ios_string=False,
                 default_lang="",
                 zh_tw: LangString = None,
                 spanish: LangString = None,
                 french: LangString = None,
                 russia: LangString = None,
                 korean: LangString = None,
                 japan: LangString = None,
                 germany: LangString = None,

                 ):
        self.module_name = module_name
        self.string_id = string_id
        self.isStringArray = isStringArray

        self.default_lang = default_lang

        self.is_android_string = is_android_string
        self.is_ios_string = is_ios_string

        self.zh_cn = zh_cn

        self.zh_tw = zh_tw

        self.english_us = english_us

        self.spanish = spanish

        self.germany = germany

        self.french = french

        self.russia = russia

        self.korean = korean

        self.japan = japan

    def get_identity_key(self) -> str:
        """
        该字符串的独特 id, 是由 common_path 和 string_id 组成的字符串,
        拥有此 identity_key 的字符串将会被合并到一个共同 mobile_string, 组成一个全语言系列的字符串
        :return:
        """
        mobile_string_identity_key = ""
        if self.zh_cn is not None and self.zh_cn.get_identity_key() is not None and self.zh_cn.get_identity_key() != "":
            mobile_string_identity_key = self.zh_cn.get_identity_key()
        elif self.english_us is not None and self.english_us.get_identity_key() is not None and self.english_us.get_identity_key() != "":
            mobile_string_identity_key = self.english_us.get_identity_key()
        elif self.korean is not None and self.korean is not None and self.korean.get_identity_key() is not None and self.korean.get_identity_key() != "":
            mobile_string_identity_key = self.korean.get_identity_key()
        elif self.japan is not None and self.japan is not None and self.japan.get_identity_key() is not None and self.japan.get_identity_key() != "":
            mobile_string_identity_key = self.japan.get_identity_key()
        elif self.germany is not None and self.germany is not None and self.germany.get_identity_key() is not None and self.germany.get_identity_key() != "":
            mobile_string_identity_key = self.germany.get_identity_key()
        elif self.spanish is not None and self.spanish is not None and self.spanish.get_identity_key() is not None and self.spanish.get_identity_key() != "":
            mobile_string_identity_key = self.spanish.get_identity_key()
        elif self.russia is not None and self.russia is not None and self.russia.get_identity_key() is not None and self.russia.get_identity_key() != "":
            mobile_string_identity_key = self.russia.get_identity_key()
        elif self.french is not None and self.french is not None and self.french.get_identity_key() is not None and self.french.get_identity_key() != "":
            mobile_string_identity_key = self.french.get_identity_key()
        return mobile_string_identity_key


def __str__(self):
    string = ""
    for key in self.__dict__.keys():
        value = self.__dict__[key]
        if value is None:
            value = ""
        string = string + str(key) + ": " + str(value) + "\n"
    return string
