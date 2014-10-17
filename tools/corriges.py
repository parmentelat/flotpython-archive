#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

from argparse import ArgumentParser

class Source (object):
    
    def __init__ (self, filename):
        self.filename = filename

    def parse (self):
        "return a list of tuples (function_name -> body)"
        function_name = None
        body = None
        result = []
        with open(self.filename) as input:
            for line in input:
                if '@BEG@' in line:
                    index = line.find("@BEG@")
                    function_name = line[index+5:].strip()
                    body = []
                elif '@END@' in line:
                    result.append( (function_name,body) )
                    function_name = None
                    body = None
                elif function_name:
                    body.append(line)
        return result




class Latex (object):

    header=r"""\documentclass [12pt]{article}
\usepackage{verbatim}
\begin{document}
\tableofcontents
"""

    footer=r"""
\end{document}
"""

# utiliser les {} comme un marqueur dans du latex ne semble pas
# être l'idée du siècle
    function_format=r"""
\section{%(function_latex)s}
\begin{verbatim}
%(body_latex)s
\end{verbatim}
"""

    def __init__ (self, output):
        self.output = output

    def write (self, a_list):
        with open(self.output, 'w') as output:
            output.write (Latex.header)
            for function_name,lines in a_list:
                body_latex = "".join(lines)
                function_latex = Latex.escape (function_name)
                output.write (Latex.function_format %locals())
            output.write (Latex.footer)
        print "{} (over)written".format(self.output)

    @staticmethod
    def escape (str):
        return str.replace ("_",r"\_")

def main ():
    parser = ArgumentParser ()
    parser.add_argument ("-o","--output", default=None)
    parser.add_argument ("files", nargs='+')
    args = parser.parse_args()

    complete = []
    for filename in args.files:
        complete += Source(filename).parse()

    output = args.output if args.output else "corriges.tex"
    Latex(output).write (complete)

if __name__ == '__main__':
    main ()
