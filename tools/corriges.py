#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

from __future__ import print_function

from argparse import ArgumentParser

############################################################
class Function:
    """
an object that describes one occurrence of a function solution
provided in the corrections/ package
it comes with a week number, a sequence number, 
a function name, plus the code as a string
    """
    def __init__ (self, week, sequence, name):
        self.week=week
        self.sequence=sequence
        self.name=name
        self.code=""
    def add_line (self, line):
        "convenience for the parser code"
        self.code += line
# corriges.py would have the ability to do sorting, but..
# I turn it off because it is less accurate
# functions appear in the right week/sequence order, but
# not necessarily in the order of the sequence..
#    @staticmethod
#    def key (self):
#        return 100*self.week+self.sequence

########################################
    # utiliser les {} comme un marqueur dans du latex ne semble pas
    # être l'idée du siècle -> je prends pour une fois %()s et l'opérateur %
    latex_format=r"""
\addcontentsline{toc}{section}{
\texttt{%(name)s} -- {\small \footnotesize{Semaine} %(week)s \footnotesize{Séquence} %(sequence)s}
%%%(name)s
}
\begin{Verbatim}[frame=single,fontsize=\%(size)s, samepage=true, numbers=left,
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
        code = self.code
        return self.latex_format % locals()

########################################
    text_format = r"""
##################################################
# %(name)s - Semaine %(week)s Séquence %(sequence)s
##################################################
%(code)s
"""
    def text (self):
        return self.text_format %self.__dict__

############################################################
class Source (object):

    # these files are known to be unicode
    exceptions = [ "w4_files" ]
    
    def __init__ (self, filename):
        self.filename = filename
        # exceptions are in UTF8 but the latex source is declared as isolatin
        # so we recode into a isolatin copy and use that instead
        for exception in self.exceptions:
            if self.filename.find(exception) >= 0:
                self.create_isolatin_from_unicode()

    def create_isolatin_from_unicode(self):
        """
        create a isolatin copy from a unicode source and use this instead
        """
        print ("WARNING: for file {self.filename}, creating ISOLATIN version instead".format(**locals()))
        uni = self.filename
        iso = "{}.iso".format(uni)
        import os
        command = "cp {uni} {iso}; recode UTF-8..ISO-8859-15 {iso}".format(**locals())
        os.system(command)
        self.filename = iso

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
                        print ("ERROR - ignored {} in {}".format(line,self.filename))
                elif '@END@' in line:
                    functions.append(function)
                    function = None
                elif function:
                    function.add_line(line)
        return functions

############################################################
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

    def __init__ (self, filename):
        self.filename = filename

    def write (self, functions, title, contents):
        with open(self.filename, 'w') as output:
            output.write (Latex.header%(dict(title=title)))
            if contents:
                output.write(Latex.contents)
            for function in functions:
                output.write (function.latex())
            output.write (Latex.footer)
        print ("{} (over)written".format(self.filename))

    @staticmethod
    def escape (str):
        return str.replace ("_",r"\_")

########################################

class Text (object):
    
    def __init__ (self, filename):
        self.filename = filename

    header = """# -*- coding: iso-8859-15 -*-
############################################################ 
#
# %(title)s
#
############################################################
"""
    

    def write (self, functions, title):
        with open (self.filename, 'w') as output:
            output.write (self.header%dict(title=title))
            for function in functions:
                output.write (function.text())
        print ("{} (over)written".format(self.filename))

def main ():
    parser = ArgumentParser ()
    parser.add_argument ("-o","--output", default=None)
    parser.add_argument ("-t","--title", default="Donnez un titre avec --title")
    parser.add_argument ("-c","--contents", action='store_true', default=False)
    parser.add_argument ("-L","--latex", action='store_true', default=False)
    parser.add_argument ("-T","--text", action='store_true', default=False)
    parser.add_argument ("files", nargs='+')
    args = parser.parse_args()

    functions = []
    for filename in args.files:
        functions += Source(filename).parse()

    if args.latex:
        do_latex = True; do_text = False
    elif args.text:
        do_latex = False; do_text = True
    else:
        do_latex = True; do_text = True

    output = args.output if args.output else "corriges"
    texoutput = "{}.tex".format(output)
    txtoutput = "{}.txt".format(output)
    if do_latex:
        Latex(texoutput).write (functions, title=args.title, contents=args.contents)
    if do_text:
        Text (txtoutput).write (functions, title=args.title)

if __name__ == '__main__':
    main ()
