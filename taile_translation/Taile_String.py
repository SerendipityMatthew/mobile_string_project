class TaileString:
    def __init__(self, module_name, android_id,
                 default_lang, ios_id,
                 simplified_chinese, english_us,
                 spanish, french, russia,
                 korean, japan, germany):
        self.module_name = module_name
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
            string = string +  key + " == " + self.__dict__[key] + "\n"
        return string
