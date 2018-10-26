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

from pathlib import Path
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor


##########
# status so far:
#
# (*) a code cell that contains any of the IGNORE_IF_PRESENT strings
#     in its source gets ignored altogether (not evaluated at all)
# (*) a code cell that contains any of the IGNORE_IF_PRESENT_IN_METADATA
#     tag with value among the ones defined in IGNORE_IF_PRESENT_IN_METADATA
#     gets ignored as well
# (*) a cell that has a metadata tagged with the tag defined here as
#     CODE_TO_EXEC_INSTEAD: we execute the metadata value instead of the
#     cell source; this typically for cells that use input()

IGNORE_IF_PRESENT_IN_SOURCE = [
    '%ipythontutor',
    # cells about auto-evaluated exercises
    '.correction(',
]

IGNORE_IF_PRESENT_IN_METADATA = {
    'latex:skip-eval' : [True],
}

# if this key is set in metadata, we evaluate that code
# instead of the cell's code
CODE_TO_EXEC_INSTEAD = "latex:hidden-code-instead"
CODE_TO_EXEC_BEFORE = "latex:hidden-code-before"
CODE_TO_EXEC_AFTER = "latex:hidden-code-after"

# replace on the fly
CODE_REPLACEMENT = "latex:replace"
REPLACE_ALL = '*all*'

# attach to this key either
#  * one list with 2 strings
# [ "ab", "cd"]
#  * or a list of 2-string lists of that kind
# [ ["ab", "cd"], ["ef", "gh"]]
# this will replace all occurrences of "ab" into "cd"
# and same with the second couple
#
#  note that '*ALL*' as the left-hand-side
# in a replacement means the whole cell gets rewritten


# all annotations will mention this string
MARKER = "auto-exec-for-latex"

##########

# helpers
def load_notebook(path: Path):
    with path.open() as feed:
        return nbformat.read(feed, as_version=4)

def save_notebook(notebook, path: Path):
    with path.open('w') as output:
        nbformat.write(notebook, output)



class CustomExecPreprocessor(ExecutePreprocessor):

    def preprocess_cell(self, cell, resources, cell_index):

        # even if we skip a cell, we need to comply with the protocol
        # implemented in the superclass, which expects
        ignored_result = cell, resources
        def mark_ignored(cell):
            if cell.cell_type == 'code':
                cell.source = (f"# NOTE\n"
                               f"# {MARKER} has skipped execution of this cell\n\n"
                               + cell.source)

        substituted_code = None

        source = cell.source
        for ignore in IGNORE_IF_PRESENT_IN_SOURCE:
            if ignore in source:
                mark_ignored(cell)
                return ignored_result

        metadata = cell.metadata
        for key, value in metadata.items():

            if (key in IGNORE_IF_PRESENT_IN_METADATA
                    and value in IGNORE_IF_PRESENT_IN_METADATA[key]):
                mark_ignored(cell)
                return ignored_result

            if key == CODE_TO_EXEC_INSTEAD:
                substituted_code = cell.source
                cell.source = metadata[key]

            if key == CODE_TO_EXEC_BEFORE:
                substituted_code = cell.source
                cell.source = metadata[key] + "\n" + cell.source

            if key == CODE_TO_EXEC_AFTER:
                substituted_code = cell.source
                cell.source = cell.source + "\n" + metadata[key]

            if key == CODE_REPLACEMENT:
                replacements = metadata[key]
                # should be either a 2-string list
                # or a list of 2-string lists
                def is_replacement(x):
                    return isinstance(x, list) and len(x) == 2
                if is_replacement(replacements):
                    replacements = [replacements]
                for replacement in replacements:
                    if not is_replacement(replacement):
                        print(f"Could not use replacement {replacement}")
                        continue
                    before, after = replacement
                    if before == REPLACE_ALL:
                        cell.source = after
                    else:
                        cell.source = cell.source.replace(before, after)

        execution_result = ExecutePreprocessor.preprocess_cell(
            self, cell, resources, cell_index)

        if substituted_code is not None and cell.cell_type == 'code':
            cell.source = (substituted_code
                           + f"\n\n# NOTE:\n# {MARKER} has used instead:"
                           + f"\n##########"
                           + f"\n{cell.source}"
                           + f"\n##########"
                           )

        return execution_result

# main

def main():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-v", "--verbose", default=False, action='store_true',
                        help="List notebook names as they are taken care of")
    parser.add_argument("-e", "--exec-dir", default=".",
                        help="Directory to execute in")
    parser.add_argument("-o", "--output-dir", default="executing",
                        help="Directory to store notebooks in")
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

    output_path = Path(args.output_dir)
    if not output_path.is_dir():
        print(f"Creating {output_path}")
        output_path.mkdir()
    if not output_path.is_dir():
        print(f"Could not create output dir {output_path} - exiting")
        exit(1)

    for notebook in args.notebooks:
        path = Path(notebook)
        notebook = load_notebook(path)
        stem = path.stem
        output = output_path / f"{stem}.ipynb"
        if args.verbose:
            print(f"{path} -> {output}")
        preprocessor = CustomExecPreprocessor(timeout=600, kernel_name='python3')
        executed, resources = preprocessor.preprocess(notebook, resources)
        save_notebook(executed, output)

if __name__ == '__main__':
    main()
