#!/usr/bin/env python3

# pylint: disable=c0111

"""
Purpose is to script the phase that evaluates our notebooks prior to being
translated into LaTeX for producing handouts

We have several kinds of ad hoc treatments to be done in this context

* some cells must not be evaluated at all (e.g. the one with ipythontutor
magic)
* some cells call input() and cannot be run unattended
* etc .. list to be completed

"""

# status right now:
#
# (*) a code cell that contains any of the IGNORE_IF_PRESENT strings
#     in its source gets ignored altogether (not evaluated at all)
# (*) a code cell that contains any of the IGNORE_IF_PRESENT_IN_METADATA
#     tag with value among the ones defined in IGNORE_IF_PRESENT_IN_METADATA
#     gets ignored as well


IGNORE_IF_PRESENT_IN_SOURCE = [
    '%ipythontutor',
]

IGNORE_IF_PRESENT_IN_METADATA = {
    'latex:ignore' : [True],
}


DEBUG=False

from pathlib import Path
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor


# helpers
def load_notebook(path: Path):
    with path.open() as feed:
        return nbformat.read(feed, as_version=4)

def save_notebook(notebook, path: Path):
    with path.open('w') as output:
        nbformat.write(notebook, output)



class CustomExecPreprocessor(ExecutePreprocessor):

    def preprocess_cell(self, cell, resources, cell_index):

        ignore_it = False

        source = cell.source
        for ignore in IGNORE_IF_PRESENT_IN_SOURCE:
            if ignore in source:
                ignore_it = True
                break

        metadata = cell.metadata
        for key, value in metadata.items():
            if (key in IGNORE_IF_PRESENT_IN_METADATA
                    and value in IGNORE_IF_PRESENT_IN_METADATA[key]):
                ignore_it = True
                break

        if DEBUG:
            print(f"evaluating cell #{cell_index} -> {ignore_it} "
                  f"type={type(cell.source)}")
        if not ignore_it:
            return ExecutePreprocessor.preprocess_cell(
                self, cell, resources, cell_index)
        # otherwise even if we skip that cell we need
        # to comply with the protocol implemented in the superclass
        return cell, resources


# main

def main():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-d", "--exec-dir", default="executing",
                        help="Directory to execute and store notebooks in")
    parser.add_argument("notebooks", nargs='+')

    args = parser.parse_args()

    exec_path = Path(args.exec_dir)
    if not exec_path.is_dir():
        print(f"Creating {exec_path}")
        exec_path.mkdir()
    if not exec_path.is_dir():
        print(f"Could not create exec dir {exec_path} - exiting")
        exit(1)
    resources = {'metadata': {'path': args.exec_dir}}

    for notebook in args.notebooks:
        path = Path(notebook)
        notebook = load_notebook(path)
        stem = path.stem
        output = exec_path / f"{stem}.ipynb"
        preprocessor = CustomExecPreprocessor(timeout=600, kernel_name='python3')
        executed, resources = preprocessor.preprocess(notebook, resources)
        save_notebook(executed, output)

if __name__ == '__main__':
    main()
