#!/usr/bin/env python3

from __future__ import print_function

import sys
import os
import tempfile
import shutil

from util import replace_file_with_string, xpath, truncate

####################
# MOOC session number
default_version = "1.0"

notebookname = "notebookname"

####################
import IPython
ipython_version = IPython.version_info[0]

if ipython_version == 2:
    import IPython.nbformat.current as current_notebook
    from IPython.nbformat.notebooknode import NotebookNode
    from IPython.nbformat.sign import NotebookNotary as Notary
elif ipython_version >= 4:
    import nbformat
    from nbformat.notebooknode import NotebookNode
    from nbformat.sign import NotebookNotary as Notary
else:
    print("normalizer tool has no support for IPython version {}".format(ipython_version))
    sys.exit(1)    
    
####################
class Notebook:
    def __init__(self, name, verbose):
        if name.endswith(".ipynb"): 
            name = name.replace(".ipynb", "")
        self.name = name
        self.filename = "{}.ipynb".format(self.name)
        self.verbose = verbose

    def parse(self):
        try:
            with open(self.filename) as f:
                if ipython_version == 2:
                    self.notebook = current_notebook.read(f, 'ipynb')
                else:
                    self.notebook = nbformat.reader.read(f)
                    
        except:
            print("Could not parse {}".format(self.filename))
            import traceback
            traceback.print_exc()

    def xpath(self, path):
        return xpath(self.notebook, path)

    def cells(self):
        try:
            return self.xpath( ['worksheets', 0, 'cells'] )
        except:
            return self.xpath( [ 'cells' ] )

    def cell_contents(self, cell):
        if ipython_version == 2:
            return cell['input']
        else:
            return cell['source']
        
    def first_heading1(self):
        for cell in self.cells():
#            print("Looking in cell ", cell)
            if cell['cell_type'] == 'heading' and cell['level'] == 1:
                return xpath(cell, ['source'])
            elif cell['cell_type'] == 'markdown':
                lines = self.cell_contents(cell).split("\n")
                if len(lines) == 1:
                    line = lines[0]
                    if line.startswith('# '):
                        return line[2:]
        return "NO HEADING 1 found"

    def set_name_from_heading1(self, force_name):
        """set 'name' in notebook metadata from the first heading 1 cell
        if force_name is provided, set 'notebookname' accordingly
        if force_name is None or False, set 'notebookname' only if it is not set"""
        metadata = self.xpath( ['metadata'])
        if metadata.get(notebookname, "") and not force_name:
            pass
        else:
            new_name = force_name if force_name else self.first_heading1()
            metadata[notebookname] = new_name
        # remove 'name' metadata that might come from previous versions of this script
        if 'name' in metadata:
            del metadata['name'] 
        if self.verbose:
            print("{} -> {}".format(self.filename, metadata[notebookname]))

    def set_version(self, version=default_version, force=False):
        metadata = self.xpath(['metadata'])
        if 'version' not in metadata or force:
            metadata['version'] = version

    # the kernel parameter here is the one that comes
    # from main, i.e. integers that can be
    # 0 if we want to leave this untouched
    #   (but that still means creating the kernelspec metadata if missing)
    # 2 for python2
    # 3 for python3
    def fill_kernelspec(self, kernel):
        kernelspec2 = {
            "display_name": "Python 2",
            "language": "python",
            "name": "python2",
        }
        kernelspec3 = {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        }
        metadata = self.xpath(['metadata'])
        # don't touch anything if kernel is not specified
        # and metadata already has a kernelspec
        if 'kernelspec' in metadata and kernel == 0:
            return
        newkernelspec = kernelspec2 if kernel <= 2 else kernelspec3
        # show the change only when relevant
        if 'kernelspec' not in metadata or metadata['kernelspec'] != newkernelspec:
            if self.verbose:
                print("setting kernel {}".format(newkernelspec['name']))
        metadata['kernelspec'] = newkernelspec

    # initial default logo_path was "media/inria-25.png"
    licence_format_left =  '<span style="float:left;">Licence CC BY-NC-ND</span>'
    licence_format_right = '<span style="float:right;">{html_authors}&nbsp;'\
                           '{html_logo_img}</span><br/>'
            
    def ensure_licence(self, authors, logo_path):
        html_logo_img_format = '<img src="{logo_path}" style="display:inline">'
        html_logo_img = "" if not logo_path else \
                        html_logo_img_format.format(logo_path=logo_path)
        def is_licence_cell(cell):
            return cell['cell_type'] == 'markdown' and cell['source'].find("Licence") >= 0
        licence_line = self.licence_format_left
        if authors:
            licence_line += self.licence_format_right.format(html_authors=" &amp; ".join(authors),
                                                             html_logo_img = html_logo_img)
        first_cell = self.cells()[0]
        # cell.source is a list of strings
        if is_licence_cell(first_cell):
            # licence cell already here, just overwrite contents to latest version
            first_cell['source'] = [ licence_line ]
        else:
            self.cells().insert(
                0,
                NotebookNode({
                "cell_type": "markdown",
                "metadata": {},
                "source": [ licence_line ],
            }))

    # I keep the code for these 2 but don't need this any longer
    # as I have all kinds of shortcuts and interactive tools now
    # plus, nbconvert(at least in jupyter) has preprocessor options to deal with this as well
    def clear_all_outputs(self):
        """clear the 'outputs' field of python code cells, and remove 'prompt_number' as well when present"""
        for cell in self.cells():
            if cell['cell_type'] == 'code':
                cell['outputs'] = []
                if 'prompt_number' in cell:
                    del cell['prompt_number']
                # this is now required in nbformat4
                if 'execution_count' in cell:
                    cell['execution_count'] = None

    def empty_cell(self, cell):
        try:
            return cell['cell_type'] == 'code' and not cell['input']
        except:
            return cell['cell_type'] == 'code' and not cell['source']
                
    def remove_empty_cells(self):
        """remove any empty cell - code cells only for now"""
        nb_empty = 0
        cells_to_remove = [ cell for cell in self.cells() if self.empty_cell(cell) ]
        nb_empty += len(cells_to_remove)
        for cell_to_remove in cells_to_remove:
             self.cells().remove(cell_to_remove)
        if nb_empty:
            print("found and removed {} empty cells".format(nb_empty))

    # likewise, this was a one-shot thing, we don't create rawnbconvert any longer
    def translate_rawnbconvert(self):
        """
        all cells of type rawnbconvert are translated into a markdown cell
        with 4 spaces indentation
        """
        nb_raw_cells = 0
        for cell in self.cells():
            if cell['cell_type'] == 'raw':
                source = cell['source']
                if self.verbose:
                    print("Got a raw cell with source of type {}".format(type(source)))
                    print(">>>{}<<<".format(source))
                    print("split:XXX{}XXX".format(source.split("\n")))
                if isinstance(cell['source'], str):
                    cell['cell_type'] = 'markdown'
                    cell['source'] = "    "+ "\n    ".join(source.split("\n"))
                    nb_raw_cells += 1
                elif isinstance(cell['source'], list):
                    cell['cell_type'] = 'markdown'
                    cell['source'] =  [ '    ' + line for line in cell['source']]
                    nb_raw_cells += 1
                else:
                    print("WARNING: dont know how to deal with a raw cell (type {})".format(type(cell['source'])))
        if nb_raw_cells:
            print("found and rewrote {} raw cells".format(nb_raw_cells))
        
    def sign(self):
        notary = Notary()
        signature = notary.compute_signature(self.notebook)
        if not signature.startswith("sha256:"):
            signature = "sha256:" + signature
        self.notebook['metadata']['signature'] = signature

    def save(self, keep_alt=False):
        if keep_alt:
            # xxx store in alt filename
            outfilename = "{}.alt.ipynb".format(self.name)
        else:
            outfilename = self.filename
        if ipython_version == 2:
            new_contents = current_notebook.writes(self.notebook,'ipynb')
        else:
            # xxx don't specify output version for now
            new_contents = nbformat.writes(self.notebook)
        if replace_file_with_string(outfilename, new_contents):
            print("{} saved into {}".format(self.name, outfilename))
            
    def full_monty(self, force_name, version, authors, logo_path,
                   kernel, sign):
        self.parse()
        self.set_name_from_heading1(force_name=force_name)
        if version is None:
            self.set_version()
        else:
            self.set_version(version, force=True)
        self.fill_kernelspec(kernel)
        self.ensure_licence(authors, logo_path)
        self.clear_all_outputs()
        self.remove_empty_cells()
        self.translate_rawnbconvert()
        if sign:
            self.sign()
        self.save()

def full_monty(name, force_name, version, authors, logo_path,
               kernel, sign, verbose):
    nb = Notebook(name, verbose)
    nb.full_monty(force_name=force_name, version=version,
                  authors=authors, logo_path=logo_path,
                  kernel=kernel, sign=sign)

from argparse import ArgumentParser

usage="""normalize notebooks
 * Metadata
   * checks for notebookname (from first heading1 if missing, or from forced name on the command line)
   * always checks for kernelspec metadata
   * sets version if specified on the command-line
 * Contents
   * makes sure a correct licence line is inserted
   * clears all outputs
   * removes empty code cells
"""

def main():
    parser = ArgumentParser(usage=usage)
    parser.add_argument("-f", "--force", action="store", dest="force_name", default=None,
                         help="force writing notebookname even if already present")
    parser.add_argument("-s", "--sign", action="store_true", dest="sign", default=False,
                         help="sign the notebooks")
    parser.add_argument("-a", "--author", dest='authors', action="append", default=[], type=str,
                        help="define list of authors")
    parser.add_argument("-l", "--logo-path", dest='logo_path', action="store", default="", type=str,
                        help="path to use when inserting the logo img (should be about 25px high)")
    parser.add_argument("-k", "--kernel", dest='kernel', type=int, default=0, choices=(2, 3),
                        help="Set to use python2 or 3; remains unchanged if not set")
    parser.add_argument("-v", "--verbose", dest="verbose", action="store_true", default=False,
                         help="show current notebookname")
    parser.add_argument("-V", "--version", dest="version", action="store", default=None,
                         help="set version in notebook metadata")
    parser.add_argument("notebooks", metavar="IPYNBS", nargs="*", 
                         help="the notebooks to normalize")

    args = parser.parse_args()

    if not args.notebooks:
        import glob
        notebooks = glob.glob("*.ipynb")

    print("kernel=", args.kernel)

    for notebook in args.notebooks:
        if notebook.find('.alt') >= 0 :
            print('ignoring', notebook)
            continue
        if args.verbose:
            print("{} is opening notebook".format(sys.argv[0]), notebook)
        full_monty(notebook, force_name=args.force_name, version=args.version,
                   authors=args.authors, logo_path = args.logo_path,
                   kernel = args.kernel, sign=args.sign, verbose=args.verbose)

if __name__ == '__main__':
    main()
