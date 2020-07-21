 #!/usr/bin/python 
import sys
import os.path

from Parser import Parser
from Scanner import Scanner
from Constants import Constants, DoublyLinkedNode


def determine_invalid_flags(input_flags):
    invalid_input_flags = list()
    for flag in input_flags:
        if flag not in Constants.SUPPORTED_FLAGS:
            invalid_input_flags.append(flag)
    return invalid_input_flags


def compute_num_flags(input_flags):
    return sum(list(["-" in flag for flag in input_flags]))


args = list(sys.argv)

flags = args[1:]

num_flags = compute_num_flags(flags)

if not num_flags and not len(flags):
    print(Constants.WHITESPACE.join(
        list([
            Constants.ERROR_PREFIX,
            Constants.NO_FILENAME_SPECIFIED_ERROR
        ])
    ))

    print(Constants.USER_MANUAL)
else:
    if num_flags > 1:
        print(Constants.WHITESPACE.join(
            list([
                str(num_flags),
                Constants.MULTIPLE_FLAGS_WARNING
            ])
        ))

    if "-h" in flags:
        print(Constants.USER_MANUAL)
    else:
        filepath = flags.pop()

        if not os.path.isfile(filepath):
            print(Constants.WHITESPACE.join(
                list([
                    Constants.ERROR_PREFIX,
                    Constants.FILE_NOT_FOUND_ERROR_PREFIX,
                    "\'" + filepath + "\'",
                    Constants.FILE_NOT_FOUND_ERROR_SUFFIX
                ])
            ))

            print(Constants.USER_MANUAL)
        else:
            invalid_flags = determine_invalid_flags(flags)
            if invalid_flags:
                print(Constants.WHITESPACE.join(
                    list([
                        Constants.ERROR_PREFIX,
                        Constants.INVALID_FLAG_ERROR_PREFIX,
                        "\'" + invalid_flags[0].lstrip("-") + "\'",
                        Constants.INVALID_FLAG_ERROR_SUFFIX
                    ])
                ))

                print(Constants.USER_MANUAL)
            else:
                iloc_scanner = Scanner(filepath)

                iloc_parser = Parser(iloc_scanner)

                if "-r" in flags:
                    ir, printable_ir = iloc_parser.run()
                    if iloc_parser.error_count:
                        print(Constants.WHITESPACE.join(
                            list([
                                Constants.ERROR_PREFIX,
                                Constants.PARSER_FINAL_ERROR_R
                            ])
                        ))
                    else:
                        print("No errors whilst parsing. Run smoothly.")
                elif "-p" in flags or not len(flags):
                    ir, printable_ir = iloc_parser.run()

                    if iloc_parser.error_count:
                        print(Constants.WHITESPACE.join(
                            list([
                                "Parser found",
                                str(iloc_parser.error_count),
                                "syntax errors in",
                                str(iloc_scanner.line_id),
                                "lines of input."
                            ])
                        ))
                    else:
                        print(Constants.WHITESPACE.join(
                            list([
                                Constants.SUCCESSFUL_PARSER_MESSAGE_PREFIX,
                                str(iloc_parser.operation_count),
                                Constants.SUCCESSFUL_PARSER_MESSAGE_SUFFIX
                            ])
                        ))

                elif "-s" in flags:
                    iloc_scanner.print_tokens()

                elif "-q" in flags:
                    sys.exit()


