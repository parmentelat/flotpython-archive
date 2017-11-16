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

# we drop older versions, requires IPython v4
assert IPython.version_info[0] >= 4

import nbformat
from nbformat.notebooknode import NotebookNode
from nbformat.sign import NotebookNotary as Notary

# not customizable yet
# at the notebook level

livereveal_metadata_padding = {
    'livereveal': {
        "theme": "simple",
        "start_slideshow_at": "selected",
        "auto_select" : "code",
        "auto_select_fragment" : True,
        "autolaunch" : False,
#        "slideNumber" : False,
#        "controls" : False,
    },
}

# this was for the video slides, it's bad on regular notebooks
livereveal_metadata_clear = {
    'celltoolbar': 'Slideshow',
}

livereveal_metadata_force = {
    'livereveal': {
        "backimage" : "media/nologo.png",
        "transition": "fade",
        "width": "100%",
        "height": "100%",
    }
}

extensions_metadata_cell_padding = {
    "deletable": True,
    "editable": True,
    "run_control": {
        "frozen": False,
        "read_only": False
    }
}

default_licence = 'Licence CC BY-NC-ND'

####################
# padding is a set of keys/subkeys
# that we want to make sure are defined
# this will never alter a key already present
# just add key-pair values from the default
# it means that we define these keys
# if not yet present

def pad_metadata(metadata, padding, force=False):
    """
    makes sure the keys in padding are defined in metadata
    if force is set, overwrite any previous value
    """
    for k, v in padding.items():
        if isinstance(v, dict):
            sub_meta = metadata.setdefault(k, {})
            pad_metadata(sub_meta, v, force)
        if not isinstance(v, dict):
            if force:
                metadata[k] = v
            else:
                metadata.setdefault(k, v)

def clear_metadata(metadata, padding):
    """
    makes sure the keys in padding are removed in metadata
    """
    for k, v in padding.items():
        # supertree missing in metadata : we're good
        if k not in metadata:
            continue
        if isinstance(v, dict):
            sub_meta = metadata[k]
            clear_metadata(sub_meta, v)
        if not isinstance(v, dict):
            del metadata[k]

                
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
                self.notebook = nbformat.reader.read(f)

        except:
            print("Could not parse {}".format(self.filename))
            import traceback
            traceback.print_exc()

    def xpath(self, path):
        return xpath(self.notebook, path)

    def cells(self):
        try:
            return self.xpath(['worksheets', 0, 'cells'])
        except:
            return self.xpath(['cells'])

    def cell_contents(self, cell):
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
        metadata = self.xpath(['metadata'])
        if metadata.get(notebookname, "") and not force_name:
            pass
        else:
            new_name = force_name if force_name else self.first_heading1()
            metadata[notebookname] = new_name
        # remove 'name' metadata that might come from previous versions of this
        # script
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
    def handle_kernelspec(self, kernel):
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
        # is there really a change ?
        if 'kernelspec' not in metadata or metadata['kernelspec'] != newkernelspec:
            # if we're here, we're about to mess with the kernelspec
            # and so language_info' is irrelevant
            if 'language_info' in metadata:
                del metadata['language_info']
            if self.verbose:
                print("setting kernel {}".format(newkernelspec['name']))
        metadata['kernelspec'] = newkernelspec

    def fill_rise_metadata(self, rise):
        """
        if rise is set:
        if metadata is missing the 'livereveal' key,
        fill it with a set of hard-wired settings
        """
        if not rise:
            return
        metadata = self.notebook['metadata']
        pad_metadata(metadata, livereveal_metadata_padding)
        pad_metadata(metadata, livereveal_metadata_force, force=True)
        clear_metadata(metadata, livereveal_metadata_clear)

    def fill_extensions_metadata(self, exts):
        """
        if exts is set, fill each cell metadata's with a hard-wired
        set of defaults for extensions; this is to minimize git diffs
        """
        if not exts:
            return
        for cell in self.cells():
            pad_metadata(cell['metadata'], extensions_metadata_cell_padding)

    def ensure_title(self, licence, authors, logo_path):
        """
        make sure the first cell is a author + licence cell
        """

        # the title cell has 3 parts that are equidistant
        # xxx it looks like this <style> tag somehow gets
        # trimmed away when rendered inside of edx
        # so I had to add it in nbhosting's custom.css as well
        title_style = '''<style>
div.title-slide {
    width: 100%;
    display: flex;
    flex-direction: row;            /* default value; can be omitted */
    flex-wrap: nowrap;              /* default value; can be omitted */
    justify-content: space-between;
}
</style>
'''

        title_format = '''<div class="title-slide">
<span style="float:left;">{licence}</span>
<span>{html_authors}</span>
<span>{html_image}</span>
</div>'''

        
        title_image_format = '<img src="{logo_path}" style="display:inline" />'
        html_image = "" if not logo_path else \
                      title_image_format.format(logo_path=logo_path)
        # a bit rustic but good enough

        def is_title_cell(cell):
            # for legacy - notebooks tweaked with older versions
            # of this tool, we want to consider first cells that have
            # Licence as being our title cell as well
            return cell['cell_type'] == 'markdown' \
                and (cell['source'].find("title-slide") >= 0
                     or cell['source'].find("Licence") >= 0)
        html_authors = "" if not authors \
                       else " &amp; ".join(authors)

        title_line = title_style.replace("\n", "") \
                       + title_format.format(
                           licence=licence,
                           html_authors=html_authors,
                           html_image=html_image)

        # when opened interactively and then saved again, this is how the result looks like
        title_lines = [ line + "\n" for line in title_line.split("\n") ]
        # remove last \n
        title_lines[-1] = title_lines[-1][:-1]
        
        first_cell = self.cells()[0]
        # cell.source is a list of strings
        if is_title_cell(first_cell):
            # licence cell already here, just overwrite contents to latest version
            first_cell['source'] = title_lines
        else:
            self.cells().insert(
                0,
                NotebookNode({
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": title_lines,
                }))

    # I keep the code for these 2 but don't need this any longer
    # as I have all kinds of shortcuts and interactive tools now
    # plus, nbconvert(at least in jupyter) has preprocessor options to deal
    # with this as well
    def clear_all_outputs(self):
        """
        clear the 'outputs' field of python code cells,
        and remove 'prompt_number' as well when present
        """
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
        """
        remove any empty cell - code cells only for now
        """
        nb_empty = 0
        cells_to_remove = [
            cell for cell in self.cells() if self.empty_cell(cell)]
        nb_empty += len(cells_to_remove)
        for cell_to_remove in cells_to_remove:
            self.cells().remove(cell_to_remove)
        if nb_empty:
            print("found and removed {} empty cells".format(nb_empty))

    # likewise, this was a one-shot thing, we don't create rawnbconvert any
    # longer
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
                    print("Got a raw cell with source of type {}".format(
                        type(source)))
                    print(">>>{}<<<".format(source))
                    print("split:XXX{}XXX".format(source.split("\n")))
                if isinstance(cell['source'], str):
                    cell['cell_type'] = 'markdown'
                    cell['source'] = "    " + "\n    ".join(source.split("\n"))
                    nb_raw_cells += 1
                elif isinstance(cell['source'], list):
                    cell['cell_type'] = 'markdown'
                    cell['source'] = ['    ' + line for line in cell['source']]
                    nb_raw_cells += 1
                else:
                    print("WARNING: dont know how to deal with a raw cell (type {})".format(
                        type(cell['source'])))
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
        # don't specify output version for now
        new_contents = nbformat.writes(self.notebook)
        if replace_file_with_string(outfilename, new_contents):
            print("{} saved into {}".format(self.name, outfilename))

    def full_monty(self, force_name, version, licence, authors, logo_path,
                   kernel, rise, exts, sign):
        self.parse()
        self.set_name_from_heading1(force_name=force_name)
        if version is None:
            self.set_version()
        else:
            self.set_version(version, force=True)
        self.handle_kernelspec(kernel)
        self.fill_rise_metadata(rise)
        self.fill_extensions_metadata(exts)
        self.ensure_title(licence, authors, logo_path)
        self.clear_all_outputs()
        self.remove_empty_cells()
        self.translate_rawnbconvert()
        if sign:
            self.sign()
        self.save()


def full_monty(name, **kwds):
    verbose = kwds['verbose']
    del kwds['verbose']
    nb = Notebook(name, verbose)
    nb.full_monty(**kwds)

from argparse import ArgumentParser

usage = """normalize notebooks
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
    parser.add_argument("-t", "--licence-text", dest='licence', default=default_licence,
                        help="the text for the licence string in titles")
    parser.add_argument("-a", "--author", dest='authors', action="append", default=[], type=str,
                        help="define list of authors")
    parser.add_argument("-l", "--logo-path", dest='logo_path', action="store", default="", type=str,
                        help="path to use when inserting the logo img (should be about 25px high)")
    parser.add_argument("-k", "--kernel", dest='kernel', type=int, default=0, choices=(2, 3),
                        help="Set to use python2 or 3; remains unchanged if not set")
    parser.add_argument("-r", "--rise", dest='rise', default=False, action='store_true',
                        help="fill in RISE/livereveal metadata with hard-wired settings")
    parser.add_argument("-e", "--extensions", dest='exts', action='store_true', default=False,
                        help="fill cell metadata for extensions, if missing")
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

    for notebook in args.notebooks:
        if notebook.find('.alt') >= 0:
            print('ignoring', notebook)
            continue
        if args.verbose:
            print("{} is opening notebook".format(sys.argv[0]), notebook)
        full_monty(notebook, force_name=args.force_name, version=args.version,
                   licence=args.licence, authors=args.authors, logo_path=args.logo_path,
                   kernel=args.kernel, rise=args.rise, exts=args.exts,
                   sign=args.sign, verbose=args.verbose)

if __name__ == '__main__':
    main()
