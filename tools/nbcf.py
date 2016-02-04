#!/usr/bin/env python3

### TODO
# add options to specify liverelease metadata with merge -o

hard_coded_metadata = {
  "livereveal": {
    "width": 1200,
#   available are default simple beige sky solarized
#   need to stay away from darkish ones for now apparently
    "theme": "simple",
    "transition": "zoom",
    "start_slideshow_at": "selected",
    "height": 800
  }
}    


"""
Simple tools to convert back and forth into a quick & dirty format
named 'cf' for CompactFormat

The purpose here is to use a standard text editor to do
one-shot mass-input of slides

The CF format is just a collection of cells
delimited with a line that starts with at least 4 '='
plus additional directives like markdown, code, slide or similar

Example of a CF file would be

====
a cell is markdown by default
==== code
def fact(n):
   from math import factorial
   return factorial(n)
==== slide
A cell can easily be marked as 'slide' or 'subslide' or 'fragment'
==== slide code
def foo(n):
    "a code cell that is first in its slide"
    pass

--------------------
2 tools are available (based on sys.argv[0] for now)

* merge: 
  * takes all input args - either notebooks or cf's - and merges them into a ipynb
  * default is to merge into the first input argument
  * unless optional -o argument is specified, in which case a new notebook is created

* reverse:
  * takes one ipynb
  * and creates related cf file

NOTES.

this is truly experimental !

metadata - like typically width/height/theme/ and the like - is not handled yet at all
so this may be lost when 
 * creating a new ipynb with merge -o
 * and of course when reversing because .cf has no provision for that at all
"""

import sys
import os
import re

from util import replace_file_with_string, xpath, truncate

import IPython
ipython_version = IPython.version_info[0]

if ipython_version == 4:
    import nbformat
    from nbformat.notebooknode import NotebookNode
    current_format = nbformat.v4
else:
    print("merge tool for ipython == 4 only")
    exit(1)
    
def xpath(top, path):
    result = top
    for i in path:
        result = result[i]
    return result

def truncate(s, n):
    return s if len(s) < n else s[:n-2] + ".."


####################
class Notebook:
    def __init__(self, name):
        if name.endswith(".ipynb"): 
            name = name.replace(".ipynb", "")
        self.name = name
        self.filename = "{}.ipynb".format(self.name)

    def exists(self):
        return os.path.exists(self.filename)

    def create(self):
        self.notebook = current_format.new_notebook()
        self.notebook.metadata.update(hard_coded_metadata)
        self.cells = self.notebook.cells

    def parse(self):
        """return a bool indicating success"""
        try:
            with open(self.filename) as f:
                self.notebook = nbformat.reader.read(f)
                self.cells = self.notebook.cells
            return True
        except OSError as e:
#            print("file not found {}".format(self.filename))
            return False
        except:
            print("Could not parse {}".format(self.filename))
            import traceback
            traceback.print_exc()
            return False

    def xpath(self, path):
        return xpath(self.notebook, path)

    def save(self, keep_alt=False):
        if keep_alt:
            # xxx store in alt filename
            outfilename = "{}.alt.ipynb".format(self.name)
        else:
            outfilename = self.filename
        # xxx don't specify output version for now
        new_contents = nbformat.writes(self.notebook)
        if replace_file_with_string(outfilename, new_contents):
            print("{} saved into {}".format(self.name, outfilename))
            
    def cell_contents(self, cell):
        return cell['source']
            
####################
class CompactFormat:

    def __init__(self, name):
        if name.endswith(".cf"): 
            name = name.replace(".cf", "")
        self.name = name
        self.filename = "{}.cf".format(self.name)

    def exists(self):
        return os.path.exists(self.filename)

    def parse(self):
        """
        reads the .cf file looks for separator, and returns 
        a list of cells like e.g.
        {'metadata': {}, 'cell_type': 'markdown', 'source': ['# my title\n', '## a subtitle' ]}
        variants
        'cell_type' : 'code' 
        'metadata': {'slideshow': {'slide_type': 'slide'}}
        'metadata': {'slideshow': {'slide_type': '-'}}

        returns a bool indicating success
        """

        # v0 : keep it simple
        # start with at least 4 =, and a list of python-like idents
        match_sep = re.compile("\A={4,}\s*((\S+)?(\s+\S+)*)\Z")
        def is_sep(line):
            """
            returns either None
            or a list of idents if that's a match
            """
            line = line.strip()
            match = match_sep.match(line)
            if not match:
                return
            # the complete rest of line after initial = signs
            idents = match.group(1).split()
            return idents

        def new_cell(idents, filename, lineno, source = None):
            cell_types = ['markdown', 'code' ]
            slide_types = ['slide', 'subslide', 'fragment' ]
            cell = {'metadata' : {},
                    'cell_type' : 'markdown'}
            if source is not None:
                cell['source'] = source
            for ident in idents:
                if ident in cell_types:
                    cell['cell_type'] = ident
                    if ident == 'code':
                        cell['outputs'] = []
                        cell['execution_count'] = 0
                elif ident in slide_types:
                    if 'slideshow' not in cell['metadata']:
                        cell['metadata']['slideshow'] = {}
                    cell['metadata']['slideshow']['slide_type'] = ident
                else:
                    print("{}:{} - ignored directive `{}' in separator".format(filename, lineno, ident))    
            return NotebookNode(cell)

        # accumulate cells over file
        self.cells = []
        # idents are specified at the beginning of the cell
        cell_idents = None
        try:
            with open(self.filename) as f:
                source = ""
                for lineno, line in enumerate(f):
                    line_idents = is_sep(line)
                    # not a separator
                    if line_idents is None:
                        source += line
                    else:
                        # a pending cell has been started
                        if cell_idents is not None:
                            self.cells.append(new_cell(cell_idents, self.filename, lineno+1, source=source))
                            source = ""
                        # remember for next cell
                        cell_idents = line_idents
                # don't forget last cell
            if cell_idents is not None:
                self.cells.append(new_cell(cell_idents, self.filename, lineno+1, source=source))
            return True
        except:
            import traceback
            traceback.print_exc()
            return False

    def save(self, notebook, keep_alt=False):
        if keep_alt and self.exists():
            # xxx store in alt filename
            outfilename = "{}.alt.cf".format(self.name)
        else:
            outfilename = self.filename
        with open(outfilename, "w") as out:
            for cell in notebook.cells:
                idents = [ cell.cell_type ]
                if 'slideshow' in cell.metadata:
                    idents.append(cell.metadata.slideshow.slide_type)
                out.write("==== {}\n".format(" ".join(idents)))
                out.write(cell.source)
                if cell.source and cell.source[-1] != "\n":
                    out.write("\n")
        print("saved {}".format(outfilename))

####################
from argparse import ArgumentParser

##### merging one or more inputs (regardless of their type) into a notebook
def merge():
    parser = ArgumentParser()
    parser.add_argument("-o", "--output", help="name for the output ipynb", default=None)
    parser.add_argument("inputs", nargs="*", help="notebooks (.ipynb) or compact format (.cf)")
    args = parser.parse_args()

    inputs = args.inputs

    # the receiver for the merge is
    # (*) if --output is specified:
    #     it is expected to not exist yet, and a new notebook is created with name args.output
    # (*) otherwise
    # the first argument is expected to be a notebook (as opposed to a .cf)
    # and in this case the rest of the inputs are merged into it
    if args.output:
        output = args.output
        receiver = Notebook(output)
        receiver.create()
    else:
        output = inputs.pop(0)
        receiver = Notebook(output)
        if not receiver.parse():
            print("First arg is required to denote a notebook")
            exit(1)

    print("Entering: {} has {} cells".format(output, len(receiver.cells)))

    for index, input in enumerate(args.inputs):
        file = Notebook(input)
        if file.parse():
            print("{} is a notebook with {} cells".format(input, len(file.cells)))
        else:
            file = CompactFormat(input)
            if file.parse():
                print("{} is a compact format with {} cells".format(input, len(file.cells)))
            else:
                print("could not read {} -- ignored".input)
                continue
        receiver.cells += file.cells

    print("Done: {} now has {} cells".format(output, len(receiver.cells)))
    receiver.save()
    print("saved {}".format(receiver.filename))
            
##### converting back to cf
def reverse():
    parser = ArgumentParser()
    parser.add_argument("notebook")
    args = parser.parse_args()
    input = args.notebook

    notebook = Notebook(input)
    if not notebook.parse():
        print("Could not parse input {}".format(input))
        exit(1)
    cf = CompactFormat(notebook.filename.replace(".ipynb", ""))
    cf.save(notebook, keep_alt = True)
    

####################
if __name__ == '__main__':
    if sys.argv[0].find('merge') >= 0:
        merge()
    elif sys.argv[0].find('reverse') >= 0:
        reverse()
