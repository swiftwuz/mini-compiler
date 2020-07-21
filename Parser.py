from Scanner import Scanner
from InstructionsList import DoublyLinkedNode, InstructionsList


class Parser(object):
    PRINTABLE_OP_STR_SIZE = 8  # operation string size - useful for formatting

    def __init__(self, iloc_scanner):
        self.__iloc_scanner = iloc_scanner

        self.__operation_count = 0

        self.__error_count = 0

        self.__current_sentence = list()

    def run(self):
        next_token = self.iloc_scanner.next_token

        printable_ir = str()
        internal_representation = InstructionsList()

        line_number, syntactic_category, lexeme = Scanner.process_token(next_token())

        self.__current_sentence.append(lexeme)

        while not syntactic_category == "EOF":

            if syntactic_category == "MEMOP":
                success = self.construct_sentence(["MEMOP", "REG", "INTO", "REG"])

                if success:
                    ir_list_row, printable_ir_row = self.construct_memop_record()

                    internal_representation.append(DoublyLinkedNode(ir_list_row))

                    printable_ir += str(printable_ir_row)

            elif syntactic_category.__eq__("LOADI"):
                success = self.construct_sentence(["LOADI", "CONSTANT", "INTO", "REG"])

                if success:
                    ir_list_row, printable_ir_row = self.construct_loadi_record()

                    internal_representation.append(DoublyLinkedNode(ir_list_row))

                    printable_ir += str(printable_ir_row)

            elif syntactic_category.__eq__("ARITHOP"):
                success = self.construct_sentence(["ARITHOP", "REG", "COMMA", "REG", "INTO", "REG"])

                if success:
                    ir_list_row, printable_ir_row = self.construct_arithop_record()

                    internal_representation.append(DoublyLinkedNode(ir_list_row))

                    printable_ir += str(printable_ir_row)

            elif syntactic_category.__eq__("OUTPUT"):
                success = self.construct_sentence(["OUTPUT", "CONSTANT"])

                if success:
                    ir_list_row, printable_ir_row = self.construct_output_record()

                    internal_representation.append(DoublyLinkedNode(ir_list_row))

                    printable_ir += str(printable_ir_row)

            elif syntactic_category.__eq__("NOP"):
                success = self.construct_sentence(["NOP"])

                if success:
                    ir_list_row, printable_ir_row = self.construct_nop_record()

                    internal_representation.append(DoublyLinkedNode(ir_list_row))

                    printable_ir += str(printable_ir_row)

            else:
                print(" ".join(
                    list([
                        "ERROR:",
                        line_number + ":",
                        "Operation starts with an invalid opcode:",
                        "\'" + lexeme + "\'"
                    ])
                ))

                self.error_count += 1

            self.operation_count += 1

            line_number, syntactic_category, lexeme = Scanner.process_token(next_token())

            self.__current_sentence = list([lexeme])

        return internal_representation, str(printable_ir)

    def construct_sentence(self, production):
        next_token_fn = self.iloc_scanner.next_token
        process_token_fn = Scanner.process_token
        for expected_category in production[1:]:
            token = next_token_fn()
            line_number, actual_category, lexeme = process_token_fn(token)
            if not actual_category == expected_category:
                print(" ".join(
                    list([
                        "ERROR:",
                        line_number + ":",
                        "Expected a(n)",
                        Parser.__return_full_name(expected_category) + ",",
                        "got a(n)",
                        Parser.__return_full_name(actual_category) + ":",
                        "\'" + lexeme + "\'"
                    ])
                ))
                self.error_count += 1
                return False

            self.__current_sentence.append(lexeme)
        return True

    def construct_memop_record(self):
        ir_py_list = \
            list([
                self.__construct_operation_str(self.current_sentence[0]),
                Parser.__extract_register_number(self.current_sentence[1]),
                "-",
                "-",
                "-",
                "-",
                "-",
                "-",
                "-",
                Parser.__extract_register_number(self.current_sentence[3]),
                "-",
                "-",
                "-"
            ])

        printable_ir_str = \
            Parser.__construct_printable_op_str(Parser.__extract_first_lexeme(ir_py_list[0])) + \
            "[ " + "sr" + str(ir_py_list[1]) + " ], " + \
            "[ ], " + \
            "[ " + "sr" + str(ir_py_list[9]) + " ]\n"

        return ir_py_list, printable_ir_str

    def construct_loadi_record(self):
        ir_py_list = \
            list([
                self.__construct_operation_str(self.current_sentence[0]),
                Parser.__to_int(self.current_sentence[1]),
                "-",
                "-",
                "-",
                "-",
                "-",
                "-",
                "-",
                Parser.__extract_register_number(self.current_sentence[3]),
                "-",
                "-",
                "-"
            ])

        printable_ir_str = \
            Parser.__construct_printable_op_str(Parser.__extract_first_lexeme(ir_py_list[0])) + \
            "[ " + "val " + str(ir_py_list[1]) + " ], " + \
            "[ ], " + \
            "[ " + "sr" + str(ir_py_list[9]) + " ]\n"

        return ir_py_list, printable_ir_str

    def construct_arithop_record(self):
        ir_py_list = \
            list([
                self.__construct_operation_str(self.current_sentence[0]),
                Parser.__extract_register_number(self.current_sentence[1]),
                "-",
                "-",
                "-",
                Parser.__extract_register_number(self.current_sentence[3]),
                "-",
                "-",
                "-",
                Parser.__extract_register_number(self.current_sentence[5]),
                "-",
                "-",
                "-",
            ])

        printable_ir_str = \
            Parser.__construct_printable_op_str(Parser.__extract_first_lexeme(ir_py_list[0])) + \
            "[ " + "sr" + str(ir_py_list[1]) + " ], " + \
            "[ " + "sr" + str(ir_py_list[5]) + " ], " + \
            "[ " + "sr" + str(ir_py_list[9]) + " ]\n"

        return ir_py_list, printable_ir_str

    def construct_output_record(self):
        ir_py_list = \
            list([
                self.__construct_operation_str(self.current_sentence[0]),
                Parser.__to_int(self.current_sentence[1]),
                "-",
                "-",
                "-",
                "-",
                "-",
                "-",
                "-",
                "-",
                "-",
                "-",
                "-",
            ])

        printable_ir_str = \
            Parser.__construct_printable_op_str(Parser.__extract_first_lexeme(ir_py_list[0])) + \
            "[ " + "val " + str(ir_py_list[1]) + " ], " + \
            "[ ]," + \
            "[ ]\n"

        return ir_py_list, printable_ir_str

    def construct_nop_record(self):
        ir_py_list = \
            list([
                self.__construct_operation_str(self.current_sentence[0]),
                "-",
                "-",
                "-",
                "-",
                "-",
                "-",
                "-",
                "-",
                "-",
                "-",
                "-",
                "-",
            ])

        printable_ir_str = \
            Parser.__construct_printable_op_str(Parser.__extract_first_lexeme(ir_py_list[0])) + \
            "[ ]," + \
            "[ ]," + \
            "[ ]\n"

        return ir_py_list, printable_ir_str

    @staticmethod
    def __extract_first_lexeme(string):
        lexeme = str()
        for character in string:
            if character != " ":
                lexeme += character
            else:
                return lexeme

    @staticmethod
    def __construct_printable_op_str(raw_op_str):
        return str(raw_op_str + (Parser.PRINTABLE_OP_STR_SIZE - len(raw_op_str)) * " ")

    def __construct_operation_str(self, op_str):
        return " ".join(list([op_str, "(" + str(self.iloc_scanner.line_id) + ")"]))

    @staticmethod
    def __extract_register_number(reg_str):
        return Parser.__to_int(reg_str.lstrip("r"))

    @staticmethod
    def __return_full_name(category):
        if category == "MEMOP":
            return "Memory Operation"
        elif category == "REG":
            return "Register"
        elif category == "INTO":
            return "Into"
        elif category == "LOADI":
            return "LoadI"
        elif category == "CONSTANT":
            return "Constant"
        elif category == "ARITHOP":
            return "Arithmetic Operation"
        elif category == "COMMA":
            return "Comma"
        elif category == "OUTPUT":
            return "Output"
        elif category == "NOP":
            return "Nop"
        else:
            return "Invalid Category"

    @staticmethod
    def __to_int(string):
        return \
            sum(
                list([
                    (ord(string[index]) - ord("0")) * (10 ** (len(string) - index - 1))
                    for index in range(len(string))
                ])
            )

    @property
    def iloc_scanner(self):
        return self.__iloc_scanner

    @iloc_scanner.setter
    def iloc_scanner(self, iloc_scanner):
        self.__iloc_scanner = iloc_scanner

    @property
    def operation_count(self):
        return self.__operation_count

    @operation_count.setter
    def operation_count(self, operation_count):
        self.__operation_count = operation_count

    @property
    def error_count(self):
        return self.__error_count

    @error_count.setter
    def error_count(self, error_count):
        self.__error_count = error_count

    @property
    def current_sentence(self):
        return self.__current_sentence

    @current_sentence.setter
    def current_sentence(self, current_sentence):
        self.__current_sentence = current_sentence
