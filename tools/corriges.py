#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os.path
import re

from argparse import ArgumentParser

############################################################
class Solution:
    """
    an object that describes one occurrence of a function solution
    provided in the corrections/ package
    it comes with a week number, a sequence number, 
    a function name, plus the code as a string

    there may be several solutions for a single function
    in general the first one is used for generating validation stuff
    """

    def __init__(self,
                 # mandatory
                 filename, week, sequence, name,
                 # additional tags supported on the @BEG@ line
                 more=None, latex_size='small',
                 no_validation=None, no_exemple=None,
             ):
        self.path = filename
        self.filename = os.path.basename(filename).replace('.py', '')
        self.week = week
        self.sequence = sequence
        self.name = name
        # something like 'v2' or 'suite' to label a new version or a continuation
        self.more = more
        # set to footnotesize if a solution is too wide
        self.latex_size = latex_size
        # if set (to anything), no validation at all
        self.no_validation = no_validation
        # if set (to anything), no exemple show up in the validation nb
        self.no_exemple = no_exemple
        # internals : the Source parser will feed the code in there
        self.code = ""

    def __repr__(self):
        return "<Solution from {} function={} week={} seq={}>"\
            .format(self.filename, self.name, self.week, self.sequence)

    def add_code_line(self, line):
        "convenience for the parser code"
        self.code += line + "\n"
# corriges.py would have the ability to do sorting, but..
# I turn it off because it is less accurate
# solutions appear in the right week/sequence order, but
# not necessarily in the order of the sequence..
#    @staticmethod
#    def key(self):
#        return 100*self.week+self.sequence

    
########################################
    # utiliser les {} comme un marqueur dans du latex ne semble pas
    # être l'idée du siècle -> je prends pour une fois %()s et l'opérateur %
    latex_format = r"""
\addcontentsline{toc}{section}{
\texttt{%(name)s}%(more)s -- {\small \footnotesize{Semaine} %(week)s \footnotesize{Séquence} %(sequence)s}
%%%(name)s
}
\begin{Verbatim}[frame=single,fontsize=\%(latex_size)s, samepage=true, numbers=left,
framesep=3mm, framerule=3px,
rulecolor=\color{Gray},
%%fillcolor=\color{Plum},
label=%(name)s%(more)s - {\small \footnotesize{Semaine} %(week)s \footnotesize{Séquence} %(sequence)s}]
%(code)s\end{Verbatim}
\vspace{1cm}
"""

    def latex(self):
        name = Latex.escape(self.name)
        week = self.week
        sequence = self.sequence
        latex_size = self.latex_size
        code = self.code
        more = r" {{\small ({})}}".format(self.more) if self.more else ""
        return self.latex_format % locals()

    # the validation notebook
    notebook_cell_format=r"""
    {{
     "cell_type": "code",
     "collapsed": false,
     "input": [
    {cell_lines}
     ],
     "language": "python",
     "metadata": {{}},
     "outputs": []
    }}
"""

    notebook_cell_separator=r"""
    {
     "cell_type": "markdown",
     "metadata": {},
     "source": [
      "*********"
     ]
    }
"""
    
    def notebook_cells(self):
        sep = self.notebook_cell_separator
        cell_lines = []
        def add_cell_line(line):
            cell_lines.append('"{}\\n"'.format(line))
        def make_cell():
            return self.notebook_cell_format.format(cell_lines=",\n".join(cell_lines))

        # some exercices are so twisted that we can't do anything for them here
        if self.no_validation:
            cell_lines = []
            add_cell_line("#################### exo {} has no_validation set"
                          .format(self.name))
            cell1 = make_cell()
            return [ sep, sep, sep, cell1 ]

        # the usual case
        module = "corrections.{filename}".format(**self.__dict__)
        exo = "corrections.{filename}.exo_{name}".format(**self.__dict__)
        cell_lines = []
        add_cell_line("########## exo {} ##########".format(self.name))
        add_cell_line("# remove comment out to reload")
        add_cell_line("# reload({module})".format(module=module))
        add_cell_line("import {module}".format(module=module))
        if self.no_exemple is None:
            add_cell_line("{exo}.exemple()".format(exo=exo))
        cell1 = make_cell()
        cell_lines = []
        add_cell_line("# cheating - should be OK")
        add_cell_line("from {module} import {name}"
                      .format(module=module, **self.__dict__))
        add_cell_line("{exo}.correction({name})"
                      .format(exo=exo, **self.__dict__))
        cell2 = make_cell()
        cell_lines = []
        add_cell_line("# dummy solution - should be KO")
        add_cell_line("try:")
        add_cell_line("   from {module} import {name}_ko"
                      .format(module=module, **self.__dict__))
        add_cell_line("except:")
        add_cell_line("   def {name}_ko(*args, **keywords): return 'your_code'"
                      .format(**self.__dict__))
        add_cell_line("{exo}.correction({name}_ko)"
                      .format(exo=exo, **self.__dict__))
        cell3 = make_cell()
        return [sep, sep, cell1, cell2, cell3]
    
########################################
    text_format = r"""
##################################################
# {name}{more} - Semaine {week} Séquence {sequence}
##################################################
{code}
"""
    def text(self):
        more = " ({})".format(self.more) if self.more else ""
        return self.text_format.format(
            name=self.name,
            more=more,
            week=self.week,
            sequence=self.sequence,
            code=self.code)

############################################################
# as of dec. 11 2014 all files are UTF-8 and that's it
class Source(object):

    def __init__(self, filename):
        self.filename = filename

    mandatory_fields = [ 'name', 'week', 'sequence' ]
        
    beg_matcher = re.compile(
        r"\A. @BEG@(?P<keywords>(\s+[a-z_]+=[a-z_A-Z0-9-]+)+)\s*\Z"
    )
    end_matcher = re.compile(
        r"\A. @END@"
        )
    def parse(self):
        """
        return a tuple of
        * list of all Solution objects
        * list of unique (first) Solution per function
        that is to say, if one function has several solutions,
        only the first instance appears in tuple[1]
        """
        solution = None
        solutions = []
        functions = []
        names = []
        with open(self.filename) as input:
            for lineno, line in enumerate(input):
                lineno += 1
                # remove EOL for convenience
                if line[-1] == "\n":
                    line = line[:-1]
                begin = self.beg_matcher.match(line)
                end   = self.end_matcher.match(line)
                if begin:
                    assignments = begin.group('keywords').split()
                    keywords = {}
                    for assignment in assignments:
                        k, v = assignment.split('=')
                        keywords[k] = v
                    for field in self.mandatory_fields:
                        if field not in keywords:
                            print("{}:{} missing keyword {}"
                                  .format(self.filename, lineno, field))
                    try:
                        solution = Solution(filename = self.filename, **keywords)
                    except:
                        import traceback
                        traceback.print_exc()
                        print("{}:{}: ERROR (ignored): {}".format(self.filename, lineno, line))
                elif end:
                    if solution == None:
                        print("{}:{} - Unexpected @END@ - ignored\n{}"
                              .format(self.filename, lineno, line))
                    else:
                        # memorize current solution
                        solutions.append(solution)
                        # avoid duplicates in functions
                        if solution.name not in names:
                            names.append(solution.name)
                            functions.append(solution)                        
                        solution = None
                elif '@BEG@' in line or '@END@' in line:
                    print("{}:{} Warning - misplaced @BEG|END@ - ignored\n{}"
                          .format(self.filename, lineno, line))
                    continue
                elif solution:
                    solution.add_code_line(line)
        return (solutions, functions)

############################################################
class Latex(object):

    header=r"""\documentclass [12pt]{article}
\usepackage[utf8]{inputenc}
\usepackage[francais]{babel}
%% for Verbatim
\usepackage{fancyvrb}
\usepackage[usenames,dvipsnames]{color}
\setlength{\oddsidemargin}{0cm}
\setlength{\textwidth}{16cm}
\setlength{\topmargin}{-1cm}
\setlength{\textheight}{22cm}
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

    def __init__(self, filename):
        self.filename = filename

    def write(self, solutions, title, contents):
        with open(self.filename, 'w') as output:
            output.write(Latex.header%(dict(title=title)))
            if contents:
                output.write(Latex.contents)
            for solution in solutions:
                output.write(solution.latex())
            output.write(Latex.footer)
        print("{} (over)written".format(self.filename))

    @staticmethod
    def escape(str):
        return str.replace("_",r"\_")

####################
class Text(object):
    
    def __init__(self, filename):
        self.filename = filename

    header_format = """# -*- coding: utf-8 -*-
############################################################ 
#
# {title}
#
############################################################
"""
    

    def write(self, solutions, title):
        with open(self.filename, 'w') as output:
            output.write(self.header_format.format(title=title))
            for solution in solutions:
                output.write(solution.text())
        print("{} (over)written".format(self.filename))

####################
class Notebook(object):
    def __init__(self, filename):
        self.filename = filename

    header = r"""
{
 "metadata": {
  "notebookname": "VALIDATION",
  "signature": "sha256:843fabf07c2d056925e263e004388ed1a2e08532c706063406f32466db14ba23",
  "version": "1.0"
 },
 "nbformat": 3,
 "nbformat_minor": 0,
 "worksheets": [
  {
   "cells": [
"""

    footer = r"""
   ],
   "metadata": {}
  }
 ]
}
"""
    def write(self, functions):
        # JSON won't like an extra comma
        with open(self.filename, 'w') as output:
            output.write(self.header)
            all_cells = [ cell for function in functions
                               for cell in function.notebook_cells() ]
            output.write(",".join(all_cells))
            output.write(self.footer)
        print("{} (over)written".format(self.filename))

##########
class Stats(object):
    def __init__(self, solutions, functions):
        self.solutions = solutions
        self.functions = functions
    def print_count(self, verbose=False):
        skipped = [ f for f in self.functions if f.no_validation ] 
        print("We have a total of {} solutions for {} different exos  - {} not validated:"
              .format(len(self.solutions), len(self.functions), len(skipped)))
        for f in skipped:
            print("skipped {name} - w{week}s{sequence}"
                  .format(**f.__dict__))
        if verbose:
            for function in self.functions:
                print (function)

####################
def main():
    parser = ArgumentParser()
    parser.add_argument("-o","--output", default=None)
    parser.add_argument("-t","--title", default="Donnez un titre avec --title")
    parser.add_argument("-c","--contents", action='store_true', default=False)
    parser.add_argument("-L","--latex", action='store_true', default=False)
    parser.add_argument("-N","--notebook", action='store_true', default=False)
    parser.add_argument("-T","--text", action='store_true', default=False)
    parser.add_argument("files", nargs='+')
    args = parser.parse_args()

    solutions, functions = [], []
    for filename in args.files:
        ss, fs = Source(filename).parse()
        solutions += ss
        functions += fs

    if args.latex:
        do_latex = True; do_text = False; do_notebook = False
    elif args.text:
        do_latex = False; do_text = True; do_notebook = False
    elif args.notebook:
        do_latex = False; do_text = False; do_notebook = True
    else:
        do_latex = True; do_text = True; do_notebook = False

    output = args.output if args.output else "corriges"
    texoutput = "{}.tex".format(output)
    txtoutput = "{}.txt".format(output)
    nboutput = "{}.ipynb".format(output)
    if do_latex:
        Latex(texoutput).write(solutions, title=args.title, contents=args.contents)
    if do_text:
        Text(txtoutput).write(solutions, title=args.title)
    if do_notebook:
        Notebook(nboutput).write(functions)
        stats = Stats(solutions, functions)
        stats.print_count(verbose=False)
        
if __name__ == '__main__':
    main()
