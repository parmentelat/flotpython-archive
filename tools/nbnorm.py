#!/usr/bin/env python

from __future__ import print_function

import sys

# compute signature
from IPython.nbformat.sign import NotebookNotary as Notary
# store to file
import IPython.nbformat.current as current_notebook

def xpath (top, path):
    result = top
    for i in path: result=result[i]
    return result

def truncate (s, n):
    if len(s)<n: return s
    return s[:n-2]+".."

notebookname = "notebookname"

####################
class Notebook:
    def __init__ (self, name):
        if name.endswith(".ipynb"): 
            name=name.replace(".ipynb","")
        self.name=name
        self.filename="{}.ipynb".format(self.name)

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
        cells = self.xpath( ['worksheets',0, 'cells'] )
        for cell in cells:
            if cell['cell_type']=='heading' and cell['level'] == 1:
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
            metadata[notebookname]=new_name
        # remove 'name' metadata that might come from previous versions of this scrip
        if 'name' in metadata:
            del metadata['name'] 
        if verbose:
            print ("{} -> {}".format(self.filename,metadata[notebookname]))

    def set_version (self, version="1.0"):
        metadata = self.xpath (['metadata'])
        metadata['version']=version

    def clear_all_outputs (self):
        """clear the 'outputs' field of python code cells, and remove 'prompt_number' as well when present"""
        for worksheet in self.notebook.worksheets:
            for cell in worksheet.cells:
                if cell['cell_type'] == 'code' and cell['language'] == 'python':
                    cell['outputs'] = []
                    if 'prompt_number' in cell:
                        del cell['prompt_number'] 

    def sign (self):
        notary = Notary ()
        signature=notary.compute_signature (self.notebook)
        self.notebook['metadata']['signature'] = signature

    def save (self, keep_alt=True):
        if keep_alt:
            # xxx store in alt filename
            outfilename = "{}.alt.ipynb".format(self.name)
        else:
            outfilename = self.filename
        with open (outfilename, "w") as f:
            current_notebook.write (self.notebook,f,'ipynb')
        print("{} saved into {}".format(self.name, outfilename))
            
    def full_monty (self, force_name, keep_alt, verbose):
        self.parse()
        self.set_name_from_heading1(force_name=force_name, verbose=verbose)
        self.set_version()
        self.clear_all_outputs ()
        self.sign()
        self.save(keep_alt=keep_alt)

def full_monty (name, force_name, keep_alt, verbose):
    nb=Notebook(name)
    nb.full_monty (force_name=force_name, keep_alt=keep_alt, verbose=verbose)

from argparse import ArgumentParser

usage="""normalize notebooks
 * clear all outputs
 * check for notebookname
"""

def main ():
    parser = ArgumentParser(usage=usage)
    parser.add_argument ("-f", "--force", action="store", dest="force_name", default=None,
                         help="force writing notebookname even if already present")
    parser.add_argument ("-k", "--keep", dest="keep_alt", type=bool, default=False,
                         help="if set, output is saved into <>.alt.ipynb instead of overwriting")
    parser.add_argument ("-v", "--verbose", dest="verbose", action="store_true", default=False,
                         help="show current notebookname")
    parser.add_argument ("notebooks", metavar="IPYNBS", nargs="*", 
                         help="the notebooks to normalize")

    args = parser.parse_args ()

    if not args.notebooks:
        import glob
        notebooks = glob.glob("*.ipynb")

    for notebook in args.notebooks:
        if notebook.find ('.alt') >=0 :
            print ('ignoring', notebook)
            continue
        full_monty (notebook, args.force_name, args.keep_alt, args.verbose)

main()
