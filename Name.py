class Name:
    def __init__(self, name_input, is_person):
        if is_person:
            try:
                self.first_name = self.extract_first_name(name_input)
            except:
                self.first_name = 'ERROR'
            try:
                self.middle_name = self.extract_middle_name(name_input)
            except:
                self.middle_name = 'ERROR'
            try:
                self.last_name = self.extract_last_name(name_input)
            except:
                self.last_name = 'ERROR'
            self.org_name = ''
        else:
            self.first_name = ''
            self.middle_name = ''
            self.last_name = ''
            self.org_name = name_input

    @staticmethod
    def extract_first_name(full_name):
        name_array = full_name.split()
        return name_array[0]

    @staticmethod
    def extract_middle_name(full_name):
        middle_name_string = ''
        name_array = full_name.split()
        x = len(name_array)
        if x == 2 or x < 2:
            return ''
        if x == 3:
            return name_array[1]
        if x > 3:
            for i in name_array:
                value_index = name_array.index(i)
                if value_index != 0 and value_index != x - 1:
                    middle_name_string = middle_name_string + ' ' + i
            return middle_name_string

    @staticmethod
    def extract_last_name(full_name):
        name_array = full_name.split()
        x = len(name_array)
        return name_array[x - 1]