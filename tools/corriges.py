#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path
import re

from argparse import ArgumentParser

import nbformat
from nbformat.notebooknode import NotebookNode

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
                 no_validation=None, no_example=None,
                 ):
        self.path = filename
        self.filename = os.path.basename(filename).replace('.py', '')
        self.week = week
        self.sequence = sequence
        self.name = name
        # something like 'v2' or 'suite' to label a new version or a
        # continuation
        self.more = more
        # set to footnotesize if a solution is too wide
        self.latex_size = latex_size
        # if set (to anything), no validation at all
        self.no_validation = no_validation
        # if set (to anything), no example show up in the validation nb
        self.no_example = no_example
        # internals : the Source parser will feed the code in there
        self.code = ""

    def __repr__(self):
        return f"<Solution from {self.filename} function={self.name} " \
               f"week={self.week} seq={self.sequence}>"

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
\addcontentsline{toc}{subsection}{
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
    def add_validation(self, notebook):

        class Cell:
            def __init__(self):
                self.lines = []
            def add_line(self, line):
                self.lines.append(line)
            def add_lines(self, lines):
                self.lines += lines
            def record(self):
                notebook.add_code_cell(self.lines)

        # some exercices are so twisted that we can't do anything for them here
        if self.no_validation:
            for i in range(2):
                notebook.add_text_cell("*****")
            cell = Cell()
            cell.add_line(
                f"#################### exo {self.name} has no_validation set")
            cell.record()
            return

        notebook.add_text_cell("*****")
        # the usual case
        module = f"corrections.{self.filename}"
        exo = f"corrections.{self.filename}.exo_{self.name}"
        cell = Cell()
        cell.add_line(f"########## exo {self.name} ##########")
        cell.add_line(f"import {module}")
        if self.no_example is None:
            cell.add_line(f"{exo}.example()")
        cell.record()
        cell = Cell()
        cell.add_line("# cheating - should be OK")
        cell.add_line(f"from {module} import {self.name}")
        cell.add_line(f"{exo}.correction({self.name})")
        cell.record()
        cell = Cell()
        cell.add_line(f"# dummy solution - should be KO")
        cell.add_line(f"""try:
   from {module} import {self.name}_ko
except:
   print("WARNING - variant {self.name}_ko not found")
   def {self.name}_ko(*args, **keywords):
       return 'your_code'
""")

        cell.add_line(f"{exo}.correction({self.name}_ko)")
        cell.record()

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


class Source:

    def __init__(self, filename):
        self.filename = filename

    # mandatory fields
    # 'name' truly is required
    # the other 2 can sometimes be inferred from the context (filename)
    fields_defaults = [('name', None), ('week', 0), ('sequence', 0)]

    beg_matcher = re.compile(
        r"\A. @BEG@(?P<keywords>(\s+[a-z_]+=[a-z_A-Z0-9-]+)+)\s*\Z"
    )
    end_matcher = re.compile(
        r"\A. @END@"
    )
    filename_matcher = re.compile(
        r"\Aw(?P<week>[0-9]+)s(?P<sequence>[0-9]+)_"
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
        basename = os.path.basename(self.filename)
        match = self.filename_matcher.match(basename)
        if match:
            context_from_filename = match.groupdict()
        else:
            context_from_filename = {}
        with open(self.filename) as input:
            for lineno, line in enumerate(input):
                lineno += 1
                # remove EOL for convenience
                if line[-1] == "\n":
                    line = line[:-1]
                begin = self.beg_matcher.match(line)
                end = self.end_matcher.match(line)
                if begin:
                    assignments = begin.group('keywords').split()
                    keywords = {}
                    for assignment in assignments:
                        k, v = assignment.split('=')
                        keywords[k] = v
                    for field, default in self.fields_defaults:
                        if field not in keywords:
                            if default is None:
                                print(f"{self.filename}:{lineno} missing keyword {field}")
                            elif field in context_from_filename:
                                keywords[field] = context_from_filename[field]
                                # print(f"Using inferred field {field} = {keywords[field]}")
                            else:
                                print(f"{self.filename}:{lineno} using default {field}={default}")
                                keywords[field] = default
                    try:
                        solution = Solution(filename=self.filename, **keywords)
                    except:
                        import traceback
                        traceback.print_exc()
                        print(f"{self.filename}:{lineno}: ERROR (ignored): {line}")
                elif end:
                    if solution == None:
                        print(f"{self.filename}:{lineno} - Unexpected @END@ - ignored\n{line}")
                    else:
                        # memorize current solution
                        solutions.append(solution)
                        # avoid duplicates in functions
                        if solution.name not in names:
                            names.append(solution.name)
                            functions.append(solution)
                        solution = None
                elif '@BEG@' in line or '@END@' in line:
                    print(f"{self.filename}:{lineno} Warning - misplaced @BEG|END@ - ignored\n{line}")
                    continue
                elif solution:
                    solution.add_code_line(line)
        return (solutions, functions)

############################################################


class Latex:

    header = r"""\documentclass [12pt]{article}
\usepackage[utf8]{inputenc}
\usepackage[francais]{babel}
%% for Verbatim
\usepackage{fancyvrb}
\usepackage[usenames,dvipsnames]{color}
\usepackage{hyperref}

\setlength{\oddsidemargin}{0cm}
\setlength{\textwidth}{16cm}
\setlength{\topmargin}{-1cm}
\setlength{\textheight}{22cm}
\setlength{\headsep}{1.5cm}
\setlength{\parindent}{0.5cm}
\begin{document}
\begin{center}
{\huge %(title)s}
\end{center}
\vspace{1cm}
"""

    contents = r"""
%\renewcommand{\baselinestretch}{0.75}\normalsize
\tableofcontents
%\renewcommand{\baselinestretch}{1.0}\normalsize
\newpage
"""

    footer = r"""
\end{document}
"""

    week_format = r"""
\addcontentsline{{toc}}{{section}}{{Semaine {}}}
"""

    def __init__(self, filename):
        self.filename = filename

    def write(self, solutions, title_list, contents):
        week = None
        with open(self.filename, 'w') as output:
            title_tex = " \\\\ \\mbox{} \\\\ ".join(title_list)
            output.write(Latex.header % (dict(title=title_tex)))
            if contents:
                output.write(Latex.contents)
            for solution in solutions:
                if solution.week != week:
                    week = solution.week
                    output.write(self.week_format.format(week))
                output.write(solution.latex())
            output.write(Latex.footer)
        print(f"{self.filename} (over)written")

    @staticmethod
    def escape(str):
        return str.replace("_", r"\_")

####################


class Text:

    def __init__(self, filename):
        self.filename = filename

    header_format = """# -*- coding: utf-8 -*-
############################################################ 
#
# {title}
#
############################################################
"""

    def write(self, solutions, title_list):
        with open(self.filename, 'w') as output:
            for title in title_list:
                output.write(self.header_format.format(title=title))
            for solution in solutions:
                output.write(solution.text())
        print(f"{self.filename} (over)written")

####################


class Notebook:

    def __init__(self, filename):
        self.filename = filename
        self.notebook = nbformat.v4.new_notebook()
        self.add_code_cell("%load_ext autoreload\n%autoreload 2")

    def _normalize(self, contents):
        if isinstance(contents, str):
            return contents
        elif isinstance(contents, list):
            return "\n".join(contents)

    def add_text_cell(self, contents):
        self.notebook['cells'].append(
            nbformat.v4.new_markdown_cell(
                self._normalize(contents)
            ))
        
    def add_code_cell(self, contents):
        self.notebook['cells'].append(
            nbformat.v4.new_code_cell(
                self._normalize(contents)
            ))
        
    def write(self, functions):
        
        for function in functions:
            function.add_validation(self)

        # JSON won't like an extra comma
        with open(self.filename, 'w') as output:
            nbformat.write(self.notebook, output)
        print(f"{self.filename} (over)written")

##########


class Stats:

    def __init__(self, solutions, functions):
        self.solutions = solutions
        self.functions = functions

    def print_count(self, verbose=False):
        skipped = [f for f in self.functions if f.no_validation]
        ns = len(self.solutions)
        nf = len(self.functions)
        nnv = len(skipped)
        print(f"We have a total of {ns} solutions for {nf} different exos  - {nnv} not validated:")
        for f in skipped:
            print(f"skipped {f.name} - w{f.week}s{f.sequence}")
        if verbose:
            for function in self.functions:
                print(function)

####################


def main():
    parser = ArgumentParser()
    parser.add_argument("-o", "--output", default=None)
    parser.add_argument(
        "-t", "--title", default="Donnez un titre avec --title")
    parser.add_argument("-c", "--contents", action='store_true', default=False)
    parser.add_argument("-L", "--latex", action='store_true', default=False)
    parser.add_argument("-N", "--notebook", action='store_true', default=False)
    parser.add_argument("-T", "--text", action='store_true', default=False)
    parser.add_argument("files", nargs='+')
    args = parser.parse_args()

    solutions, functions = [], []
    for filename in args.files:
        ss, fs = Source(filename).parse()
        solutions += ss
        functions += fs

    if args.latex:
        do_latex = True
        do_text = False
        do_notebook = False
    elif args.text:
        do_latex = False
        do_text = True
        do_notebook = False
    elif args.notebook:
        do_latex = False
        do_text = False
        do_notebook = True
    else:
        do_latex = True
        do_text = True
        do_notebook = False

    output = args.output if args.output else "corriges"
    texoutput = f"{output}.tex"
    txtoutput = f"{output}.txt"
    nboutput = f"{output}.ipynb"
    title_list = args.title.split(";")
    if do_latex:
        Latex(texoutput).write(
            solutions, title_list=title_list, contents=args.contents)
    if do_text:
        Text(txtoutput).write(solutions, title_list=title_list)
    if do_notebook:
        Notebook(nboutput).write(functions)
        stats = Stats(solutions, functions)
        stats.print_count(verbose=False)

if __name__ == '__main__':
    main()
