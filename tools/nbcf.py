#!/usr/bin/env python3

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
class CellsFile:
    """
    a generic class for a pack of cells
    either in ipynb or cf format
    """
    def __init__(self, name, ext):
        dotext = "." + ext
        if name.endswith(dotext): 
            name = name.replace(dotext, "")
        self.name = name
        self.filename = "{}{}".format(self.name, dotext)
        # subclass will need to have a .cells attribute
        
    def exists(self):
        return os.path.exists(self.filename)

    @staticmethod
    def is_slide(cell, types = ('slide') ):
        return 'metadata' in cell and \
            'slideshow' in cell.metadata and \
            'slide_type' in xpath(cell, ('metadata', 'slideshow')) and \
            xpath(cell, ('metadata', 'slideshow', 'slide_type')) in types
            

    def __repr__(self):
        result = "{}".format(self.filename)
        if not self.exists():
            result += " (non-existing yet)"
        result += " has {} cells".format(len(self.cells))
        slide_cells = list(c for c in self.cells if self.is_slide(c))
        result += " and {} slides".format(len(slide_cells))
        return result

class Notebook(CellsFile):
    def __init__(self, name):
        CellsFile.__init__(self, name, 'ipynb')

    def create(self, *metadata_dicts):
        self.notebook = current_format.new_notebook()
        for metadata in metadata_dicts:
            self.notebook.metadata.update(metadata)
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
class CompactFormat(CellsFile):

    def __init__(self, name):
        CellsFile.__init__(self, name, 'cf')

    def parse(self):
        """
        reads the .cf file looks for separator, and returns 
        a list of cells like e.g.
        {'metadata': {}, 'cell_type': 'markdown', 'source': '# my title\n## a subtitle'}
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
                if source and source[-1] == "\n":
                    source = source[:-1]
                cell['source'] = source
            for ident in idents:
                if ident in cell_types:
                    cell['cell_type'] = ident
                    if ident == 'code':
                        cell['outputs'] = []
                        cell['execution_count'] = None
                elif ident in slide_types:
                    if 'slideshow' not in cell['metadata']:
                        cell['metadata']['slideshow'] = {}
                    cell['metadata']['slideshow']['slide_type'] = ident
                else:
                    print("{}:{} - ignored directive `{}' in separator"
                          .format(filename, lineno, ident))    
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
                            self.cells.append(new_cell(cell_idents, self.filename,
                                                       lineno+1, source=source))
                            source = ""
                        # remember for next cell
                        cell_idents = line_idents
                # don't forget last cell
            if cell_idents is not None:
                self.cells.append(new_cell(cell_idents, self.filename,
                                           lineno+1, source=source))
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
    meaningful = "relevant only with -o"
    parser = ArgumentParser()
    parser.add_argument("-o", "--output", help="name for the output ipynb", default=None)
    parser.add_argument("-O", help="like -o based on the first input - typically for converting one cf into ipynb ",
                        dest='output_first', action='store_true', default=False)
    parser.add_argument("inputs", nargs="+",
                        help="notebooks (.ipynb) or compact format (.cf)")
    parser.add_argument("-W", "--width", type=int, default=1200, help=meaningful)
    parser.add_argument("-H", "--height", type=int, default=800, help=meaningful)
    parser.add_argument("-t", "--theme", default='simple', help=meaningful)
    parser.add_argument("-r", "--transition", default='cube', help=meaningful)
    parser.add_argument("-s", "--start-option", dest='start_slideshow_at', default='selected', help=meaningful)
    args = parser.parse_args()

    def slideshow_metadata(args):
        dict = {}
        for attr in ['width', 'height', 'theme', 'transition', 'start_slideshow_at']:
            dict[attr] = getattr(args, attr)
        return {"livereveal": dict }

    # python3 hard-wired for now
    def kernelspec_metadata():
        return {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.4.4"
            }}
    
    inputs = args.inputs

    # the receiver for the merge is
    # (*) if --output is specified:
    #     it is expected to not exist yet, and a new notebook is created with name args.output
    # (*) otherwise
    # the first argument is expected to be a notebook (as opposed to a .cf)
    # and in this case the rest of the inputs are merged into it
    output = None
    if args.output_first:
        output = args.inputs[0].replace('.cf', '')
    elif args.output:
        output = args.output
    if output:
        receiver = Notebook(output)
        receiver.create(slideshow_metadata(args), kernelspec_metadata())
    else:
        output = inputs.pop(0)
        receiver = Notebook(output)
        if not receiver.parse():
            print("First arg is required to denote a notebook")
            exit(1)

    print("Entering: {}".format(receiver))

    for index, input in enumerate(args.inputs):
        file = Notebook(input)
        if file.parse():
            print("Merging notebook {}".format(file))
        else:
            file = CompactFormat(input)
            if file.parse():
                print("Merging compactfile {}".format(file))
            else:
                print("could not read {} -- ignored".input)
                continue
        receiver.cells += file.cells

    receiver.save()
    print("Saved: {}".format(receiver))
            
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
