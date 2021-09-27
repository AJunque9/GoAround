from io import SEEK_CUR
import helpers.config
import random


class Obfuscation:
    obfuscation_methods = helpers.config.ObfuscationMethods

    def __init__(self) -> None:
        pass

    def execute_obfuscation_file(self, obfuscation_type, input, output):
        code = ""
        try:
            input_file = open(input, "r")
            for line in input_file:
                code = code + line
            input_file.close()
            self.select_ofuscation(obfuscation_type, code, output)
        except IOError:
            print(
                "File not found: " + input)

    def execute_ofuscation_code(self, obfuscation_type, code, output):
        self.select_ofuscation(obfuscation_type, code, output)

    def select_ofuscation(self, obfuscation_type, code, output):
        """ Function for selecting the function to make the obfuscation """
        if (obfuscation_type == self.obfuscation_methods.mayus):
            self.execute_mayus_obfuscation(code, output)
        elif (obfuscation_type == self.obfuscation_methods.concatenation):
            self.execute_concatenation_obfuscation(code, output)
        elif (obfuscation_type == self.obfuscation_methods.insertion):
            self.execute_insertion_obfuscation(code, output)
        elif (obfuscation_type == None):
            self.write_file(code, output)
        else:
            raise SystemExit("Not supported obfuscation type")

    def execute_mayus_obfuscation(self, code, output):
        """ Function for executing the obfuscation of random uppercase and lowercase letters.
        It only obfuscates the code that is neither strings nor variables """
        choices = ["lower", "upper"]
        activate_double = False
        activate_simple = False
        word = ""
        is_string = False
        code_to_write = ""
        is_variable = False

        for line in code:
            for character in line:
                if character == '"':
                    code_to_write = code_to_write + character
                    if not is_string:
                        is_string = True
                        activate_double = True
                    else:
                        if activate_double:  # If the string had begun with double quotes
                            # String has ended
                            is_string = False
                            activate_double = False
                elif character == "'":
                    code_to_write = code_to_write + character
                    if not is_string:
                        is_string = True
                        activate_simple = True
                    else:
                        if activate_simple:  # If the string had begun with simple quotes
                            # String has ended
                            is_string = False
                            activate_simple = False
                elif character == '$':  # Beginning of a variable
                    code_to_write = code_to_write + character
                    if not is_string:
                        is_variable = True
                elif character == '\n' and is_variable:  # End of the variable
                    code_to_write = code_to_write + character
                    is_variable = False
                else:  # Other characters
                    if is_string or is_variable:  # Do not change it
                        code_to_write = code_to_write + character
                    else:
                        choice = random.choice(choices)
                        s = ""
                        if (choice == "lower"):
                            s = character.lower()
                        else:
                            s = character.upper()
                        code_to_write = code_to_write + s

        self.write_file(code_to_write, output)

    def execute_concatenation_obfuscation(self, code, output):
        """ Function for executing the obfuscation of variables concatenation """
        activate_double = False
        activate_simple = False
        word = ""
        is_string = False
        ignore_quote = False
        code_to_write = ""

        for line in code:
            for character in line:
                if character == '"':
                    if is_string == False and ignore_quote == False:
                        is_string = True
                        activate_double = True
                    elif is_string and activate_double:  # If the string had begun with double quotes
                        # Make concatenation
                        new_strings = self.make_concatenation(word, True)
                        code_to_write = code_to_write + new_strings
                        is_string = False
                        activate_double = False
                        word = ""
                    else:
                        if ignore_quote:
                            code_to_write = code_to_write + character
                        else:
                            # Quote is inside another string
                            word = word + character

                elif character == "'":
                    if is_string == False and ignore_quote == False:
                        is_string = True
                        activate_simple = True
                    elif is_string and activate_simple:  # If the string had begun with simple quotes
                        # Make concatenation
                        new_strings = self.make_concatenation(word, False)
                        code_to_write = code_to_write + new_strings
                        is_string = False
                        activate_simple = False
                        word = ""
                    else:
                        if ignore_quote:
                            code_to_write = code_to_write + character
                        else:
                            # Quote is inside another string
                            word = word + character
                elif character == '@' and is_string == False:
                    if ignore_quote == False:
                        ignore_quote = True
                    else:
                        ignore_quote = False
                    code_to_write = code_to_write + character
                else:
                    if (is_string == False):
                        code_to_write = code_to_write + character
                    else:
                        word = word + character

        self.write_file(code_to_write, output)

    def execute_insertion_obfuscation(self, code, output):
        """ Function for executing the obfuscation of variables insertion """
        activate_double = False
        activate_simple = False
        word = ""
        is_string = False
        code_insertion = ""
        code_variables = ""
        variables = 0
        ignore_quote = False

        for line in code:
            for character in line:
                if character == '"':
                    if is_string == False and ignore_quote == False:
                        is_string = True
                        activate_double = True
                    elif is_string and activate_double:  # If the string had begun with double quotes
                        # Make insertion
                        result = self.make_insertion(
                            word, variables, True)
                        new_strings = result[0]
                        code_insertion = code_insertion + new_strings
                        if '$' not in word:
                            variables = variables + 1
                            code_variables = code_variables + result[1]
                        is_string = False
                        activate_double = False
                        word = ""
                    else:
                        if ignore_quote:
                            code_insertion = code_insertion + character
                        else:
                            # Quote is inside another string
                            word = word + character

                elif character == "'":
                    if is_string == False and ignore_quote == False:
                        is_string = True
                        activate_simple = True
                    elif is_string and activate_simple:  # If the string had begun with simple quotes
                        # Make insertion
                        result = self.make_insertion(
                            word, variables, False)
                        new_strings = result[0]
                        code_insertion = code_insertion + new_strings
                        if '$' not in word:
                            variables = variables + 1
                            code_variables = code_variables + result[1]
                        is_string = False
                        activate_simple = False
                        word = ""
                    else:
                        if ignore_quote:
                            code_insertion = code_insertion + character
                        else:
                            # Quote is inside another string
                            word = word + character
                elif character == '@' and is_string == False:
                    if ignore_quote == False:
                        ignore_quote = True
                    else:
                        ignore_quote = False
                    code_insertion = code_insertion + character
                else:
                    if (is_string == False):
                        code_insertion = code_insertion + character
                    else:
                        word = word + character

        self.write_file(code_variables + code_insertion, output)

    def make_concatenation(self, word, is_double):
        """ Function that makes the new string, made of concatenation of several strings """
        # Number of strings that will be created
        number_of_concats = 1
        new_strings = ''
        if is_double:
            quote = '"'
        else:
            quote = "'"

        if (len(word) > 4):
            number_of_concats = random.randint(1, 4)
        else:
            if (len(word) <= 1):
                return quote + word + quote
            else:
                number_of_concats = random.randint(1, len(word))

        step = int(len(word)/number_of_concats)
        start = 0
        end = start + step

        if '$' in word:
            # Do not concatenate if there are variables in the string
            return quote + word + quote
        else:
            for i in range(number_of_concats):
                if (i == 0):
                    # First concatenation, without + symbol
                    new_strings = quote + word[start:end] + quote
                elif i == number_of_concats - 1:
                    # Last iteration, step could be grater
                    new_strings = new_strings + \
                        ' + ' + quote + word[start:] + quote
                else:
                    new_strings = new_strings + ' + ' + \
                        quote + word[start:end] + quote
                start = end
                end = start + step

        return new_strings

    def make_insertion(self, word, variables, is_double):
        """ Function that returns the code of the declaration of the new 
        variabels and the new strings with the variables inserted"""
        new_strings = ""
        result = []
        quote = ""
        step = 2

        if is_double:
            quote = '"'
        else:
            quote = "'"

        if (len(word) > 4):
            rand_number = random.randint(2, 4)
            step = int(len(word)/rand_number)
        else:
            if (len(word) <= 1):
                result.append(quote + word + quote)
                result.append("")
                return result
            else:
                step = int(len(word)/2)

        if '$' in word:
            # Do not insert if there are variables in the string
            result.append(quote + word + quote)
            result.append("")
            return result
        else:
            new_strings = quote + word[0:step] + \
                "$var_tfm" + str(variables) + quote
            code_variables = "$var_tfm" + \
                str(variables) + ' = ' + quote + word[step:] + quote + '\n'

        result.append(new_strings)
        result.append(code_variables)
        return result

    def write_file(self, code, output):
        """ Function for writing the given code to the file 'output'"""
        try:
            output_file = open(output, "w")
            output_file.write(code)
            output_file.close()
        except IOError:
            print(
                "An error was found. Could not create file " + output)
