class IOS_String(object):
    def __init__(self, module_name, string_id, value):
        self.module_name = module_name
        self.string_id = string_id
        self.value = value

    def __str__(self):
        string = ""
        for key in self.__dict__.keys():
            value = self.__dict__[key]
            if value is None:
                value = ""
            string = string + str(key) + " == " + str(value) + "\n"
        return string
