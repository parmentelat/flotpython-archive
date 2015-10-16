#!/usr/bin/env python

from __future__ import print_function

import sys
import os
import tempfile
import shutil
from types import StringTypes, ListType

# MOOC session number
default_version = "2.0"

# compute signature
from IPython.nbformat.sign import NotebookNotary as Notary
# store to file
import IPython.nbformat.current as current_notebook

def xpath (top, path):
    result = top
    for i in path:
        result = result[i]
    return result

def truncate (s, n):
    return s if len(s) < n else s[:n-2] + ".."

notebookname = "notebookname"

############################## stolen from nodemanager.tools
# replace a target file with a new contents - checks for changes
# can handle chmod if requested
# can also remove resulting file if contents are void, if requested
# performs atomically:
#    writes in a tmp file, which is then renamed (from sliverauth originally)
# returns True if a change occurred, or the file is deleted
def replace_file_with_string (target, new_contents, chmod=None, remove_if_empty=False):
    try:
        current = file(target).read()
    except:
        current = ""
    if current == new_contents:
        # if turns out to be an empty string, and remove_if_empty is set,
        # then make sure to trash the file if it exists
        if remove_if_empty and not new_contents and os.path.isfile(target):
            logger.verbose("tools.replace_file_with_string: removing file %s"%target)
            try: os.unlink(target)
            finally: return True
        return False
    # overwrite target file: create a temp in the same directory
    path = os.path.dirname(target) or '.'
    fd, name = tempfile.mkstemp('','repl',path)
    os.write(fd,new_contents)
    os.close(fd)
    if os.path.exists(target):
        os.unlink(target)
    shutil.move(name,target)
    if chmod:
        os.chmod(target,chmod)
    return True


####################
class Notebook:
    def __init__ (self, name):
        if name.endswith(".ipynb"): 
            name = name.replace(".ipynb","")
        self.name = name
        self.filename = "{}.ipynb".format(self.name)

    def parse (self):
        try:
            with open(self.filename) as f:
                self.notebook = current_notebook.read(f,'ipynb')
        except:
            print("Could not parse {}".format(self.filename))
            import traceback
            traceback.print_exc()

    def xpath (self, path):
        return xpath (self.notebook, path)

    def first_heading1 (self):
        cells = self.xpath( ['worksheets', 0, 'cells'] )
        for cell in cells:
            if cell['cell_type'] == 'heading' and cell['level'] == 1:
                return xpath (cell, ['source'])
        return "NO HEADING 1 found"

    def set_name_from_heading1(self, force_name, verbose):
        """set 'name' in notebook metadata from the first heading 1 cell
        if force_name is provided, set 'notebookname' accordingly
        if force_name is None or False, set 'notebookname' only if it is not set"""
        metadata = self.xpath ( ['metadata'])
        if metadata.get(notebookname,"") and not force_name:
            pass
        else:
            new_name = force_name if force_name else self.first_heading1()
            metadata[notebookname] = new_name
        # remove 'name' metadata that might come from previous versions of this script
        if 'name' in metadata:
            del metadata['name'] 
        if verbose:
            print ("{} -> {}".format(self.filename,metadata[notebookname]))

    def set_version (self, version=default_version, force=False):
        metadata = self.xpath (['metadata'])
        if 'version' not in metadata or force:
            metadata['version'] = version

    def fill_kernelspec(self):
        metadata = self.xpath (['metadata'])
        if 'kernelspec' not in metadata:
            metadata['kernelspec'] = {
        "display_name": "Python 2",
        "language": "python",
        "name": "python2",
        }

    # I keep the code for these 2 but don't need this any longer
    # as I have all kinds of shortcuts and interactive tools now
    # plus, nbconvert (at least in jupyter) has preprocessor options to deal with this as well
    def clear_all_outputs (self):
        """clear the 'outputs' field of python code cells, and remove 'prompt_number' as well when present"""
        for worksheet in self.notebook.worksheets:
            for cell in worksheet.cells:
                if cell['cell_type'] == 'code' and cell['language'] == 'python':
                    cell['outputs'] = []
                    if 'prompt_number' in cell:
                        del cell['prompt_number'] 

    def remove_empty_cells (self):
        """remove any empty cell - code cells only for now"""
        nb_empty = 0
        for worksheet in self.notebook.worksheets:
            cells_to_remove = []
            for cell in worksheet.cells:
                if cell['cell_type'] == 'code' and cell['language'] == 'python' and not cell['input']:
                    cells_to_remove.append (cell)
            nb_empty += len (cells_to_remove)
            for cell_to_remove in cells_to_remove:
                worksheet.cells.remove(cell_to_remove)
        if nb_empty:
            print ("found and removed {} empty cells".format(nb_empty))

    # likewise, this was a one-shot thing, we don't create rawnbconvert any longer
    def translate_rawnbconvert (self, verbose):
        """
        all cells of type rawnbconvert are translated into a markdown cell
        with 4 spaces indentation
        """
        nb_raw_cells = 0
        for worksheet in self.notebook.worksheets:
            for cell in worksheet.cells:
                if cell['cell_type'] == 'raw':
                    source = cell['source']
                    if verbose:
                        print("Got a raw cell with source of type {}".format(type(source)))
                        print(">>>{}<<<".format(source))
                        print("split:XXX{}XXX".format(source.split("\n")))
                    if isinstance (cell['source'], StringTypes):
                        cell['cell_type'] = 'markdown'
                        cell['source'] = "    "+ "\n    ".join(source.split("\n"))
                        nb_raw_cells += 1
                    elif isinstance (cell['source'], ListType):
                        cell['cell_type'] = 'markdown'
                        cell['source'] =  [ '    ' + line for line in cell['source']]
                        nb_raw_cells += 1
                    else:
                        print ("WARNING: dont know how to deal with a raw cell (type {})".format(type(cell['source'])))
        if nb_raw_cells:
            print ("found and rewrote {} raw cells".format(nb_raw_cells))
        
    def sign (self):
        notary = Notary ()
        signature = notary.compute_signature (self.notebook)
        if not signature.startswith("sha256:"):
            signature = "sha256:" + signature
        self.notebook['metadata']['signature'] = signature

    def save (self, keep_alt=False):
        if keep_alt:
            # xxx store in alt filename
            outfilename = "{}.alt.ipynb".format(self.name)
        else:
            outfilename = self.filename
        new_contents = current_notebook.writes (self.notebook,'ipynb')
        if replace_file_with_string (outfilename, new_contents):
            print("{} saved into {}".format(self.name, outfilename))
            
    def full_monty (self, force_name, version, sign, verbose):
        self.parse()
        self.set_name_from_heading1(force_name=force_name, verbose=verbose)
        if version is None:
            self.set_version()
        else:
            self.set_version(version, force=True)
        self.fill_kernelspec()
        self.clear_all_outputs ()
        self.remove_empty_cells ()
        self.translate_rawnbconvert(verbose)
        if sign:
            self.sign()
        self.save()

def full_monty (name, force_name, version, sign, verbose):
    nb = Notebook(name)
    nb.full_monty(force_name=force_name, version=version, sign=sign, verbose=verbose)

from argparse import ArgumentParser

usage="""normalize notebooks
 * clear all outputs
 * check for notebookname
"""

def main ():
    parser = ArgumentParser(usage=usage)
    parser.add_argument ("-f", "--force", action="store", dest="force_name", default=None,
                         help="force writing notebookname even if already present")
    parser.add_argument ("-s", "--sign", action="store_false", dest="sign", default=True,
                         help="skip signing the notebooks")
    parser.add_argument ("-v", "--verbose", dest="verbose", action="store_true", default=False,
                         help="show current notebookname")
    parser.add_argument ("-V", "--version", dest="version", action="store", default=None,
                         help="set version in notebook metadata")
    parser.add_argument ("notebooks", metavar="IPYNBS", nargs="*", 
                         help="the notebooks to normalize")

    args = parser.parse_args ()

    if not args.notebooks:
        import glob
        notebooks = glob.glob("*.ipynb")

    for notebook in args.notebooks:
        if notebook.find ('.alt') >= 0 :
            print ('ignoring', notebook)
            continue
        if args.verbose:
            print("{} is opening notebook".format(sys.argv[0]), notebook)
        full_monty (notebook, force_name=args.force_name, version=args.version, sign=args.sign, verbose=args.verbose, )

if __name__ == '__main__':
    main()
