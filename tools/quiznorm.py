#!/usr/bin/env python3

from nbnorm import replace_file_with_string


def normalize_quiz(filename):
    normalized = ""
    # False = outside, True = inside
    in_out = False
    with open(filename) as input:
        for line in input:
            if '[explanation]' in line:
                in_out = not in_out
            elif in_out:
                line = line.replace('[', '&#91;').replace(']', '&#93;')
            normalized += line
    if replace_file_with_string(filename, normalized):
        print("Normalized {}".format(filename))

from argparse import ArgumentParser

usage = """normalize quiz
 * clear all outputs
 * check for notebookname
"""


def main():
    parser = ArgumentParser(usage=usage)
    parser.add_argument("quizes", metavar="QUIZES", nargs="*",
                        help="the quizes to normalize")

    args = parser.parse_args()

    if not args.quizes:
        import glob
        notebooks = glob.glob("*.quiz")

    for quiz in args.quizes:
        if quiz.find('.alt') >= 0:
            print('ignoring', quiz)
            continue
        normalize_quiz(quiz)

if __name__ == '__main__':
    main()
