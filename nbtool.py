#!/usr/bin/env python

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
            print "Could not parse {}".format(self.filename)
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

    def set_name_from_heading1(self, force=False):
        """set 'name' in notebook metadata from the first heading 1 cell
        if force is True, always set 'notebookname'
        if force is False, set 'name' only if it is not set"""
        metadata = self.xpath ( ['metadata'])
        if metadata.get(notebookname,"") and not force:
            return
        heading1 = self.first_heading1()
        metadata[notebookname]=heading1
        # keep both 'name' and 'notebookname' in sync
        metadata['name']=heading1

    def set_version (self, version="1.0"):
        metadata = self.xpath (['metadata'])
        metadata['version']=version

    def clear_all_outputs (self):
        for worksheet in self.notebook.worksheets:
            for cell in worksheet.cells:
                if cell['cell_type'] == 'code' and cell['language'] == 'python':
                    cell['outputs'] = []

    def sign (self):
        notary = Notary ()
        signature=notary.compute_signature (self.notebook)
        self.notebook['metadata']['signature'] = signature

    def save (self, alt=True):
        if alt:
            # xxx store in alt filename
            outfilename = "{}.alt.ipynb".format(self.name)
        else:
            outfilename = self.filename
        with open (outfilename, "w") as f:
            current_notebook.write (self.notebook,f,'ipynb')
        print "{} saved into {}".format(self.name, outfilename)
            
    def full_monty (self, force_name, alt):
        self.parse()
        self.set_name_from_heading1(force=force_name)
        self.set_version()
        self.clear_all_outputs ()
        self.sign()
        self.save(alt=alt)

def full_monty (name, force_name, alt):
    nb=Notebook(name)
    nb.full_monty (force_name=force_name, alt=alt)

force_name = True
alt=False
for a in sys.argv[1:]:
    if a.find ('.alt') >=0 :
#        print 'ignoring', a
        continue
    full_monty (a, force_name, alt)
