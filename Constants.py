class Constants(object):

    WHITESPACE = " "
    NEWLINE = "\n"
    TAB = "\t"
    FORWARD_SLASH = "/"
    DIGITS = "0123456789"
    EOF = "EOF"
    MEMOP = "MEMOP"
    REG = "REG"
    INTO = "INTO"
    LOADI = "LOADI"
    CONSTANT = "CONSTANT"
    ARITHOP = "ARITHOP"
    COMMA = "COMMA"
    OUTPUT = "OUTPUT"
    NOP = "NOP"
    INVALID = "INVALID"
    MEMOP_PRODUCTION = list([MEMOP, REG, INTO, REG])
    LOADI_PRODUCTION = list([LOADI, CONSTANT, INTO, REG])
    ARITHOP_PRODUCTION = list([ARITHOP, REG, COMMA, REG, INTO, REG])

    OUTPUT_PRODUCTION = list([OUTPUT, CONSTANT])
    NOP_PRODUCTION = list([NOP])
    EMPTY_SLOT = "-"

    # user manual for the -h flag
    USER_MANUAL = "Syntax: /341fe [flags] filename\n\n" \
        "NB: filename is the pathname (absolute or relative) to the input file\n\n" \
        "Flags:\n" \
        "\t-h\t   prints this message\n" \
        "\t-s\t   prints tokens in token stream\n" \
        "\t-p\t   invokes parser and reports on success or failure\n" \
        "\t-r\t   prints human readable version of parser's IR"

    SUPPORTED_FLAGS = {"-h", "-r", "-p", "-s", "-q"}  # flags supported by the front end
    LEXICAL_ERROR_PREFIX = "Lexical error:"
    ERROR_PREFIX = "ERROR:"
    ASCII_ERROR_SUFFIX = "is not a valid ASCII character."
    INVALID_WORD_SUFFIX = "is not a valid word.\n"
    NO_FILENAME_SPECIFIED_ERROR = "No filename specified."
    FILE_NOT_FOUND_ERROR_PREFIX = "Failure to open"
    FILE_NOT_FOUND_ERROR_SUFFIX = "as the input file."
    INVALID_FLAG_ERROR_PREFIX = "Command line argument"
    INVALID_FLAG_ERROR_SUFFIX = "not recognized."
    MULTIPLE_FLAGS_WARNING = "actions specified. Only one allowed."
    SUCCESSFUL_PARSER_MESSAGE_PREFIX = "Parse succeeded, finding"
    SUCCESSFUL_PARSER_MESSAGE_SUFFIX = "ILOC operations."
    INVALID_OPCODE_ERROR = "Operation starts with an invalid opcode:"
    PARSER_FINAL_ERROR_R = "Due to syntax errors, run terminates."


class Node(object):
    def __init__(self, data):
        self.__data = data  

    def __str__(self):
        return str(self.data)  

    def __hash__(self):
        return hash(str(self))  

    def __eq__(self, other):
        return self is other

    @property
    def data(self):
        return self.__data  

    @data.setter
    def data(self, data):
        self.__data = data  


class DoublyLinkedNode(Node, object):
    def __init__(self, data, next_node=None, prev_node=None):
        Node.__init__(self, data)  
        self.__next_node = next_node  
        self.__prev_node = prev_node

    @property
    def next_node(self):
        return self.__next_node  

    @next_node.setter
    def next_node(self, next_node):
        self.__next_node = next_node  

    @property
    def prev_node(self):
        return self.__prev_node  

    @prev_node.setter
    def prev_node(self, prev_node):
        self.__prev_node = prev_node  
