import sys
from collections import deque


class Scanner(object):

    DEFAULT_BUFFER_SIZE = 100000  # default maximum number of tokens present in the token stream

    CATEGORY_STR_SIZE = 9  # number of characters in the formatted category string of a token

    def __init__(self, filepath, buffer_size=DEFAULT_BUFFER_SIZE, verbose=False):
        self.__filepath = filepath  # initialize all fields

        self.__buffer_size = buffer_size
        self.__token_buffer = deque()

        self.__input_pos = 0
        self.__input_stream = ""

        self.__line_id = 1
        self.__num_bytes = 0

        self.__verbose = verbose

    def print_tokens(self):
        self.__verbose = True  # set the verbose flag True
        while True:  # enter an infinite loop - check below for termination criteria
            current_token = self.next_token()  # extract the next token
            if "EOF" in current_token:  # if the end of file has not been reached
                break  # exit infinite loop
        self.__verbose = False  # reset the verbose flag to False

    def next_token(self):
        if not len(self.token_buffer):  # if the token stream is empty
            self.__populate_buffer()  # extract and load more tokens
        return self.token_buffer.popleft()  # return the next token

    def __populate_buffer(self):
        file_reader = open(self.filepath)  # obtain a file reader object
        file_reader.seek(self.num_bytes)  # move the file pointer appropriately

        # as long as the maximum buffer size has not been reached
        while len(self.token_buffer) <= self.buffer_size:
            if self.input_pos >= len(self.input_stream):  # if the current line has been entirely scanned

                current_line = Scanner.__readline(file_reader)  # read the next line in the file

                if not len(current_line):  # if the next line is empty
                    current_token = "< " + "EOF" + ", " + " (" + str(self.line_id) + ") >"
                    if self.verbose:  # if verbose mode is on
                        print(Scanner.__construct_token_str(current_token))  # print the next token
                    # append the EOF token along with the line number to the token stream
                    self.token_buffer.append(current_token)
                    break  # exit the while loop

                self.__initialize(current_line)  # otherwise re-initialize the scanner with the next line

            current_token = self.__run()  # extract the next token

            if "EOF" in current_token:  # handle this edge case for end of line
                continue

            # if verbose mode is on and the token is not invalid
            if self.verbose and "INVALID" not in current_token:
                print(Scanner.__construct_token_str(current_token))  # print the next token

            # append the next token along with the line number to the token stream
            self.token_buffer.append(current_token)

        self.num_bytes = file_reader.tell()  # record the number of bytes read so far
        file_reader.close()  # close the file reader object

    def __run(self):
        while True:  # enter an infinite loop
            if self.input_pos >= len(self.input_stream):  # if the current line has been entirely scanned
                # return the EOF token
                return "< " + "EOF" + ", " + " (" + str(self.line_id) + ") >"
            elif not 0 <= ord(self.input_stream[self.input_pos]) <= 127:  # if the input character is not ASCII
                sys.stderr.write(
                    " ".join(
                        list([
                            "Lexical error:",
                            str(self.line_id) + ":",
                            "\"" + self.input_stream[self.input_pos] + "\"",
                            "is not a valid ASCII character."
                        ])
                    )
                )  # print an appropriate error
                self.input_pos += 1  # advance the file pointer
                continue
            # if the current character is a whitespace
            elif self.input_stream[self.input_pos] == " ":
                self.input_pos += 1  # advance the file pointer
                continue
            # if the current character is a newline
            elif self.input_stream[self.input_pos] == "\t":
                self.input_pos += 1  # advance the file pointer
                continue
            # if the current character is a newline
            elif self.input_stream[self.input_pos] == "\n":
                self.input_pos += 1  # advance the file pointer
                self.line_id += 1  # update line id counter
                continue
            # if the current line is a comment
            elif self.input_stream[self.input_pos] == "/" and \
                    self.input_stream[self.input_pos + 1] == "/":
                self.__ignore_comment()  # skip the current line
                continue

            break

        lexeme = ""
        update_current_lexeme = self.__update_current_lexeme
        if self.input_stream[self.input_pos] == "s":
            lexeme = update_current_lexeme(lexeme)
            if self.input_stream[self.input_pos] == "t":
                lexeme = update_current_lexeme(lexeme)
                if self.input_stream[self.input_pos] == "o":
                    lexeme = update_current_lexeme(lexeme)
                    if self.input_stream[self.input_pos] == "r":
                        lexeme = update_current_lexeme(lexeme)
                        if self.input_stream[self.input_pos] == "e":  # "store" lexeme recognized
                            lexeme = update_current_lexeme(lexeme)
                            return "< " + "MEMOP" + ", " + lexeme + " (" + str(self.line_id) + ") >"
                        else:
                            lexeme = update_current_lexeme(lexeme)
                            token = "< " + "INVALID" + ", " + lexeme + " (" + str(self.line_id) + ") >"
                            self.__print_error(lexeme)
                            return token
                    else:
                        lexeme = update_current_lexeme(lexeme)
                        token = "< " + "INVALID" + ", " + lexeme + " (" + str(self.line_id) + ") >"
                        self.__print_error(lexeme)
                        return token
                else:
                    lexeme = update_current_lexeme(lexeme)
                    token = "< " + "INVALID" + ", " + lexeme + " (" + str(self.line_id) + ") >"
                    self.__print_error(lexeme)
                    return token
            elif self.input_stream[self.input_pos] == "u":
                lexeme = update_current_lexeme(lexeme)
                if self.input_stream[self.input_pos] == "b":  # "sub" lexeme recognized
                    lexeme = update_current_lexeme(lexeme)
                    return "< " + "ARITHOP" + ", " + lexeme + " (" + str(self.line_id) + ") >"
                else:
                    lexeme = update_current_lexeme(lexeme)
                    token = "< " + "INVALID" + ", " + lexeme + " (" + str(self.line_id) + ") >"
                    self.__print_error(lexeme)
                    return token
            else:
                lexeme = update_current_lexeme(lexeme)
                token = "< " + "INVALID" + ", " + lexeme + " (" + str(self.line_id) + ") >"
                self.__print_error(lexeme)
                return token
        elif self.input_stream[self.input_pos] == "l":
            lexeme = update_current_lexeme(lexeme)
            if self.input_stream[self.input_pos] == "o":
                lexeme = update_current_lexeme(lexeme)
                if self.input_stream[self.input_pos] == "a":
                    lexeme = update_current_lexeme(lexeme)
                    # "load" lexeme recognized
                    if self.input_stream[self.input_pos] == "d" and self.input_stream[self.input_pos + 1] != "I":
                        lexeme = update_current_lexeme(lexeme)
                        return "< " + "MEMOP" + ", " + lexeme + " (" + str(self.line_id) + ") >"
                    # "loadI" lexeme recognized
                    elif self.input_stream[self.input_pos] == "d" and self.input_stream[self.input_pos + 1] == "I":
                        lexeme = update_current_lexeme(lexeme)
                        lexeme = update_current_lexeme(lexeme)
                        return "< " + "LOADI" + ", " + lexeme + " (" + str(self.line_id) + ") >"
                    else:
                        lexeme = update_current_lexeme(lexeme)
                        token = "< " + "INVALID" + ", " + lexeme + " (" + str(self.line_id) + ") >"
                        self.__print_error(lexeme)
                        return token
                else:
                    lexeme = update_current_lexeme(lexeme)
                    token = "< " + "INVALID" + ", " + lexeme + " (" + str(self.line_id) + ") >"
                    self.__print_error(lexeme)
                    return token
            elif self.input_stream[self.input_pos] == "s":
                lexeme = update_current_lexeme(lexeme)
                if self.input_stream[self.input_pos] == "h":
                    lexeme = update_current_lexeme(lexeme)
                    if self.input_stream[self.input_pos] == "i":
                        lexeme = update_current_lexeme(lexeme)
                        if self.input_stream[self.input_pos] == "f":
                            lexeme = update_current_lexeme(lexeme)
                            if self.input_stream[self.input_pos] == "t":  # "lshift" lexeme recognized
                                lexeme = update_current_lexeme(lexeme)
                                return "< " + "ARITHOP" + ", " + lexeme + " (" + str(self.line_id) + ") >"
                            else:
                                lexeme = update_current_lexeme(lexeme)
                                token = "< " + "INVALID" + ", " + lexeme + " (" + str(self.line_id) + ") >"
                                self.__print_error(lexeme)
                                return token
                        else:
                            lexeme = update_current_lexeme(lexeme)
                            token = "< " + "INVALID" + ", " + lexeme + " (" + str(self.line_id) + ") >"
                            self.__print_error(lexeme)
                            return token
                    else:
                        lexeme = update_current_lexeme(lexeme)
                        token = "< " + "INVALID" + ", " + lexeme + " (" + str(self.line_id) + ") >"
                        self.__print_error(lexeme)
                        return token
                else:
                    lexeme = update_current_lexeme(lexeme)
                    token = "< " + "INVALID" + ", " + lexeme + " (" + str(self.line_id) + ") >"
                    self.__print_error(lexeme)
                    return token
            else:
                lexeme = update_current_lexeme(lexeme)
                token = "< " + "INVALID" + ", " + lexeme + " (" + str(self.line_id) + ") >"
                self.__print_error(lexeme)
                return token
        elif self.input_stream[self.input_pos] == "r":
            lexeme = update_current_lexeme(lexeme)
            if self.input_stream[self.input_pos] == "s":
                lexeme = update_current_lexeme(lexeme)
                if self.input_stream[self.input_pos] == "h":
                    lexeme = update_current_lexeme(lexeme)
                    if self.input_stream[self.input_pos] == "i":
                        lexeme = update_current_lexeme(lexeme)
                        if self.input_stream[self.input_pos] == "f":
                            lexeme = update_current_lexeme(lexeme)
                            if self.input_stream[self.input_pos] == "t":  # "rshift" lexeme recognized
                                lexeme = update_current_lexeme(lexeme)
                                return "< " + "ARITHOP" + ", " + lexeme + " (" + str(self.line_id) + ") >"
                            else:
                                lexeme = update_current_lexeme(lexeme)
                                token = "< " + "INVALID" + ", " + lexeme + " (" + str(self.line_id) + ") >"
                                self.__print_error(lexeme)
                                return token
                        else:
                            lexeme = update_current_lexeme(lexeme)
                            token = "< " + "INVALID" + ", " + lexeme + " (" + str(self.line_id) + ") >"
                            self.__print_error(lexeme)
                            return token
                    else:
                        lexeme = update_current_lexeme(lexeme)
                        token = "< " + "INVALID" + ", " + lexeme + " (" + str(self.line_id) + ") >"
                        self.__print_error(lexeme)
                        return token
                else:
                    lexeme = update_current_lexeme(lexeme)
                    token = "< " + "INVALID" + ", " + lexeme + " (" + str(self.line_id) + ") >"
                    self.__print_error(lexeme)
                    return token
            elif self.input_stream[self.input_pos] in "0123456789":  # register lexeme recognized
                lexeme = update_current_lexeme(lexeme)
                while self.input_stream[self.input_pos] in "0123456789":
                    lexeme = update_current_lexeme(lexeme)
                return "< " + "REG" + ", " + lexeme + " (" + str(self.line_id) + ") >"
            else:
                lexeme = update_current_lexeme(lexeme)
                token = "< " + "INVALID" + ", " + lexeme + " (" + str(self.line_id) + ") >"
                self.__print_error(lexeme)
                return token
        elif self.input_stream[self.input_pos] == "m":
            lexeme = update_current_lexeme(lexeme)
            if self.input_stream[self.input_pos] == "u":
                lexeme = update_current_lexeme(lexeme)
                if self.input_stream[self.input_pos] == "l":
                    lexeme = update_current_lexeme(lexeme)
                    if self.input_stream[self.input_pos] == "t":  # "mult" lexeme recognized
                        lexeme = update_current_lexeme(lexeme)
                        return "< " + "ARITHOP" + ", " + lexeme + " (" + str(self.line_id) + ") >"
                    else:
                        lexeme = update_current_lexeme(lexeme)
                        token = "< " + "INVALID" + ", " + lexeme + " (" + str(self.line_id) + ") >"
                        self.__print_error(lexeme)
                        return token
                else:
                    lexeme = update_current_lexeme(lexeme)
                    token = "< " + "INVALID" + ", " + lexeme + " (" + str(self.line_id) + ") >"
                    self.__print_error(lexeme)
                    return token
            else:
                lexeme = update_current_lexeme(lexeme)
                token = "< " + "INVALID" + ", " + lexeme + " (" + str(self.line_id) + ") >"
                self.__print_error(lexeme)
                return token
        elif self.input_stream[self.input_pos] == "a":
            lexeme = update_current_lexeme(lexeme)
            if self.input_stream[self.input_pos] == "d":
                lexeme = update_current_lexeme(lexeme)
                if self.input_stream[self.input_pos] == "d":  # "add" lexeme recognized
                    lexeme = update_current_lexeme(lexeme)
                    return "< " + "ARITHOP" + ", " + lexeme + " (" + str(self.line_id) + ") >"
                else:
                    lexeme = update_current_lexeme(lexeme)
                    token = "< " + "INVALID" + ", " + lexeme + " (" + str(self.line_id) + ") >"
                    self.__print_error(lexeme)
                    return token
            else:
                lexeme = update_current_lexeme(lexeme)
                token = "< " + "INVALID" + ", " + lexeme + " (" + str(self.line_id) + ") >"
                self.__print_error(lexeme)
                return token
        elif self.input_stream[self.input_pos] == "n":
            lexeme = update_current_lexeme(lexeme)
            if self.input_stream[self.input_pos] == "o":
                lexeme = update_current_lexeme(lexeme)
                if self.input_stream[self.input_pos] == "p":  # "nop" lexeme recognized
                    lexeme = update_current_lexeme(lexeme)
                    return "< " + "NOP" + ", " + lexeme + " (" + str(self.line_id) + ") >"
                else:
                    lexeme = update_current_lexeme(lexeme)
                    token = "< " + "INVALID" + ", " + lexeme + " (" + str(self.line_id) + ") >"
                    self.__print_error(lexeme)
                    return token
            else:
                lexeme = update_current_lexeme(lexeme)
                token = "< " + "INVALID" + ", " + lexeme + " (" + str(self.line_id) + ") >"
                self.__print_error(lexeme)
                return token
        elif self.input_stream[self.input_pos] == "o":
            lexeme = update_current_lexeme(lexeme)
            if self.input_stream[self.input_pos] == "u":
                lexeme = update_current_lexeme(lexeme)
                if self.input_stream[self.input_pos] == "t":
                    lexeme = update_current_lexeme(lexeme)
                    if self.input_stream[self.input_pos] == "p":
                        lexeme = update_current_lexeme(lexeme)
                        if self.input_stream[self.input_pos] == "u":
                            lexeme = update_current_lexeme(lexeme)
                            if self.input_stream[self.input_pos] == "t":  # "output" lexeme recognized
                                lexeme = update_current_lexeme(lexeme)
                                return "< " + "OUTPUT" + ", " + lexeme + " (" + str(self.line_id) + ") >"
                            else:
                                lexeme = update_current_lexeme(lexeme)
                                token = "< " + "INVALID" + ", " + lexeme + " (" + str(self.line_id) + ") >"
                                self.__print_error(lexeme)
                                return token
                        else:
                            lexeme = update_current_lexeme(lexeme)
                            token = "< " + "INVALID" + ", " + lexeme + " (" + str(self.line_id) + ") >"
                            self.__print_error(lexeme)
                            return token
                    else:
                        lexeme = update_current_lexeme(lexeme)
                        token = "< " + "INVALID" + ", " + lexeme + " (" + str(self.line_id) + ") >"
                        self.__print_error(lexeme)
                        return token
                else:
                    lexeme = update_current_lexeme(lexeme)
                    token = "< " + "INVALID" + ", " + lexeme + " (" + str(self.line_id) + ") >"
                    self.__print_error(lexeme)
                    return token
            else:
                lexeme = update_current_lexeme(lexeme)
                token = "< " + "INVALID" + ", " + lexeme + " (" + str(self.line_id) + ") >"
                self.__print_error(lexeme)
                return token
        elif self.input_stream[self.input_pos] in "0123456789":  # constant lexeme recognized
            lexeme = update_current_lexeme(lexeme)
            while self.input_stream[self.input_pos] in "0123456789":
                lexeme = update_current_lexeme(lexeme)
            return "< " + "CONSTANT" + ", " + lexeme + " (" + str(self.line_id) + ") >"
        elif self.input_stream[self.input_pos] == "=":
            lexeme = update_current_lexeme(lexeme)
            if self.input_stream[self.input_pos] == ">":  # "=>" lexeme recognized
                lexeme = update_current_lexeme(lexeme)
                return "< " + "INTO" + ", " + lexeme + " (" + str(self.line_id) + ") >"
            else:
                lexeme = update_current_lexeme(lexeme)
                token = "< " + "INVALID" + ", " + lexeme + " (" + str(self.line_id) + ") >"
                self.__print_error(lexeme)
                return token
        elif self.input_stream[self.input_pos] == ",":  # "," lexeme recognized
            lexeme = update_current_lexeme(lexeme)
            return "< " + "COMMA" + ", " + lexeme + " (" + str(self.line_id) + ") >"
        else:
            lexeme = update_current_lexeme(lexeme)
            token = "< " + "INVALID" + ", " + lexeme + " (" + str(self.line_id) + ") >"
            self.__print_error(lexeme)
            return token

    def __update_current_lexeme(self, lexeme):
        self.input_pos += 1  # advance the file pointer
        return lexeme + self.input_stream[self.input_pos - 1]  # return the updated lexeme

    def __initialize(self, input_stream):
        self.input_pos = 0
        self.input_stream = input_stream

    def __ignore_comment(self):
        while not self.input_stream[self.input_pos] == "\n" and \
                self.input_pos < len(self.input_stream):
            self.input_pos += 1  # skip the current character

    @staticmethod
    def __readline(file_reader):
        next_line = ""
        while True:
            next_char = file_reader.read(1)
            next_line += next_char
            if next_char == "\n" or next_char == "":
                break
        return next_line

    @staticmethod
    def process_token(token):
        processed_token = token.lstrip("< ").rstrip(" >")  # strip off the outer substrings

        # extract the line number
        line_number = processed_token.split()[-1].lstrip("(").rstrip(")")

        # if the token signifies the EOF, handle the special case
        if "EOF" in processed_token:
            return line_number, "EOF", str()
        else:  # otherwise
            syntactic_category, lexeme = processed_token.split(", ", 1)
            lexeme = lexeme.split()[0]
            return line_number, syntactic_category, lexeme  # return the post-processed constituents

    @staticmethod
    def __construct_token_str(token):
        line_number, syntactic_category, lexeme = Scanner.process_token(token)
        while len(syntactic_category) < Scanner.CATEGORY_STR_SIZE:
            syntactic_category += " " 
        return line_number + ": < " + syntactic_category + ", \"" + lexeme + "\" >"

    def __print_error(self, lexeme):
        sys.stderr.write(
            " ".join(
                list([
                    "Lexical error:",
                    str(self.line_id) + ":",
                    "\"" + lexeme + "\"",
                    "is not a valid word.\n"
                ])
            )
        )  # print the error message to stderr
        self.line_id += 1  # skip to the next line
        self.input_pos = len(self.input_stream)

    @property
    def filepath(self):
        return self.__filepath  # return the file path

    @filepath.setter
    def filepath(self, filepath):
        self.__filepath = filepath  # set the current file path to the input file path

    @property
    def buffer_size(self):
        return self.__buffer_size  # return the maximum size of the token buffer

    @buffer_size.setter
    def buffer_size(self, buffer_size):
        self.__buffer_size = buffer_size  # set the current buffer size to the input buffer size

    @property
    def token_buffer(self):
        return self.__token_buffer  # return the token stream

    @token_buffer.setter
    def token_buffer(self, token_buffer):
        self.__token_buffer = deque(iterable=token_buffer)

    @property
    def input_pos(self):
        return self.__input_pos  # return the input position

    @input_pos.setter
    def input_pos(self, input_pos):
        self.__input_pos = input_pos  # set the current input position to the input input position

    @property
    def input_stream(self):
        return self.__input_stream  # return the input stream

    @input_stream.setter
    def input_stream(self, input_stream):
        self.__input_stream = input_stream  # set the current input stream to the input input stream

    @property
    def line_id(self):
        return self.__line_id  # return the number of lines scanned

    @line_id.setter
    def line_id(self, line_id):
        self.__line_id = line_id  # set the current number of lines to the input number of lines

    @property
    def num_bytes(self):
        return self.__num_bytes  # return the number of bytes

    @num_bytes.setter
    def num_bytes(self, num_bytes):
        self.__num_bytes = num_bytes  # set the current number of bytes to the input number of bytes

    @property
    def verbose(self):
        return self.__verbose  # return the verbose flag

    @verbose.setter
    def verbose(self, verbose):
        self.__verbose = verbose  # set the current verbose flag to the input verbose flag
