#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

from argparse import ArgumentParser

class Function:
    """
an object that describe one occurrence of a function solution
provided in the corrections/ pacakge
it comes with a week number, a sequence number, 
a function name, plus the code as a list of lines
    """
    def __init__ (self, week, sequence, name):
        self.week=week
        self.sequence=sequence
        self.name=name
        self.code=[]
    def add_line (self, line):
        "convenience for the parser code"
        self.code.append(line)
# corriges.py would have the ability to do sorting, but..
# I turn it off because it is less accurate
# functions appear in the right week/sequence order, but
# not necessarily in the order of the sequence..
#    @staticmethod
#    def key (self):
#        return 100*self.week+self.sequence

    # utiliser les {} comme un marqueur dans du latex ne semble pas
    # être l'idée du siècle -> je prends pour une fois %()s et l'opérateur %
    latex_format=r"""
\addcontentsline{toc}{section}{
\texttt{%(name)s} -- {\small \footnotesize{Semaine} %(week)s \footnotesize{Séquence} %(sequence)s}
%%%(name)s
}
\begin{Verbatim}[frame=single,fontsize=\%(size)s,numbers=left, samepage=true, 
framesep=3mm, framerule=3px,
rulecolor=\color{Gray},
%%fillcolor=\color{Plum},
label=%(name)s - {\small \footnotesize{Semaine} %(week)s \footnotesize{Séquence} %(sequence)s}]
%(code)s\end{Verbatim}
\vspace{1cm}
"""
    # on peut tricher un peu si un problème ne rentre pas bien dans les clous
    # \tiny, \scriptsize, \footnotesize, \small, \normalsize
    exceptions_size = { 'diff': 'footnotesize',
#                        'decode_zen' : 'small',
                    }

    def latex (self):
        name = Latex.escape (self.name)
        week = self.week
        sequence = self.sequence
        size = Function.exceptions_size.get(self.name,'small')
        code = "".join(self.code)
        return Function.latex_format % locals()

class Source (object):
    
    def __init__ (self, filename):
        self.filename = filename

    def parse (self):
        "return a list of Function objects"
        function = None
        functions = []
        with open(self.filename) as input:
            for line in input:
                if '@BEG@' in line:
                    index = line.find("@BEG@")
                    end_of_line = line[index+5:].strip()
                    try:
                        week, sequence, name = end_of_line.split(' ')
                        function = Function (week, sequence, name)
                    except:
                        print "ERROR - ignored {} in {}".format(line,filename)
                elif '@END@' in line:
                    functions.append(function)
                    function = None
                elif function:
                    function.add_line(line)
        return functions

class Latex (object):

    header=r"""\documentclass [12pt]{article}
\usepackage[latin1]{inputenc}
\usepackage[francais]{babel}
%% for Verbatim
\usepackage{fancyvrb}
\usepackage[usenames,dvipsnames]{color}
\setlength{\oddsidemargin}{0cm}
\setlength{\textwidth}{16cm}
\setlength{\topmargin}{0cm}
\setlength{\textheight}{21cm}
\setlength{\headsep}{1.5cm}
\setlength{\parindent}{0.5cm}
\begin{document}
\centerline{\huge{%(title)s}}
\vspace{2cm}
"""

    contents=r"""
\tableofcontents
\newpage
"""


    footer=r"""
\end{document}
"""

    def __init__ (self, output):
        self.output = output

    def write (self, functions, title, contents):
        with open(self.output, 'w') as output:
            output.write (Latex.header%(dict(title=title)))
            if contents:
                output.write(Latex.contents)
            for function in functions:
                output.write (function.latex())
            output.write (Latex.footer)
        print "{} (over)written".format(self.output)

    @staticmethod
    def escape (str):
        return str.replace ("_",r"\_")

def main ():
    parser = ArgumentParser ()
    parser.add_argument ("-o","--output", default=None)
    parser.add_argument ("-t","--title", default="Donnez un titre avec --title")
    parser.add_argument ("-c","--contents", action='store_true', default=False)
    parser.add_argument ("files", nargs='+')
    args = parser.parse_args()

    functions = []
    for filename in args.files:
        functions += Source(filename).parse()

# see above
#    functions.sort(key=Function.key)

    output = args.output if args.output else "corriges.tex"
    Latex(output).write (functions, title=args.title, contents=args.contents)

if __name__ == '__main__':
    main ()
