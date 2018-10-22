#!/usr/bin/env python3

# pylint: disable=c0111

"""
Purpose is to script the phase that evaluates our notebooks prior to being
translated into LaTeX for producing handouts

We have several kinds of ad hoc treatments to be done in this context

* some cells must not be evaluated at all (e.g. the one with ipythontutor
magic)
* some cells call input() and cannot be run in the background
* etc .. list to be completed

"""


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

        run_it = True

        source = cell.source
        if '%ipythontutor' in source:
            run_it = False

        if DEBUG:
            print(f"evaluating cell #{cell_index} -> {run_it} "
              f"type={type(cell.source)}")
        if run_it:
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
