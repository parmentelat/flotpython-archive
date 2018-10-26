#!/usr/bin/env python3

from pathlib import Path
from argparse import (ArgumentParser, ArgumentDefaultsHelpFormatter)

# this is where we put boxes around code cells
# as well as code included in the notebook with
# ```python
# some code
# ```
#
# note that with other ways to achieve the same effect, namely
# * code between ``` lines but without the python mention, or
# * code preceded with 4 spaces
# the resulting latex contains a plain \begin{verbatim}
# which is not as easily customizable

replacements = [

    # set all Verbatim (i.e. In[] and Out[]) with a colored frame
    (r'\begin{Verbatim}[commandchars=\\\{\}]',
     r'\begin{Verbatim}[commandchars=\\\{\},frame=single,framerule=0.3mm,rulecolor=\color{cellframecolor}]'),

    # set all Highlighting (i.e. inserted code) with a colored frame
    (r'\begin{Highlighting}[]',
     r'\begin{Highlighting}[frame=lines,framerule=0.6mm,rulecolor=\color{asisframecolor}]'),
]

def strip_latex(in_path, out_name=None):

    in_path = Path(in_path)

    print(f"in_path = {in_path}")

    if out_name is None:
        out_path = in_path + ".strip"
    else:
        out_path = Path(out_name)

    with in_path.open() as in_file, \
            out_path.open('w') as out_file:

        ignoring = True

        for line in in_file:
            if r'\begin{document}' in line:
                ignoring = False
                continue
            if r'\end{document}' in line:
                ignoring = True
                continue
            if r'\maketitle' in line:
                continue
            if r'Licence CC BY-NC-ND' in line:
                continue
            if not ignoring:
                for before, after in replacements:
                    line = line.replace(before, after)
                out_file.write(line)
    print(f"(over)wrote ${out_path}")


def main():
    parser = ArgumentParser()
    parser.add_argument("-d", "--directory", default=None,
                        help="Store stripped tex files in this directory")
    parser.add_argument("tex_files", nargs='+')

    args = parser.parse_args()

    for arg in args.tex_files:
        if args.directory:
            out = Path(args.directory) / Path(arg).name
        else:
            out = None
        strip_latex(arg, out)
    return 0

if __name__ == '__main__':
    main()
