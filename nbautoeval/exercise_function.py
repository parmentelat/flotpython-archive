# -*- coding: utf-8 -*-



############################################################
# the low level interface - used to be used directly in the first exercises

from IPython.display import HTML

from .log import log_correction
from .rendering import (
    Table, TableRow, TableCell, CellLegend,
    font_style, header_font_style,
    ok_style, ko_style,
    center_cell_style,
    truncate_value)

DEBUG=False
#DEBUG=True

########## defaults for columns widths - for FUN 
# this historically was called 'columns' as it was used to specify
# the width of the 3 columns (in correction mode)
# or of the 2 columns (in example mode) 
# however when adding new layouts like 'text', the argument passed to the layout
# function ceased to be a column width, so we call this layout_args instead
# but in most cases this does represent column widths
default_layout_args =  (24, 28, 28)

####################        
class ExerciseFunction(object):
    """The class for an exercise where students are asked to write a
    function The teacher version of that function is provided as
    'solution' and is used against datasets to generate an online
    correction or example.
    A dataset is an instance of Args (or ArgsKeywords)

    The most useful method in this class is 'correction'; for each
    input in the dataset, we call both the teacher function and the
    student function, and compare the results using '==' to produce a
    table of green or red cells.

    The class provides a few other utility methods, like 'example'
    that can be used in the students notebook to show the expected
    result for some or all of the inputs.

    One important aspects of this is copying. Realizing that both
    teacher and student functions can do side effects in the inputs,
    it means that these need to be copied before any call is made. By
    default the copy is a deep copy, but for some corner cases it can
    be required to use shallow copy instead; in this case just pass
    copy_mode='shallow' to the constructor here.

    Some more cosmetic settings are supported as well, for defining
    the column widths in both the correction and example outputs. Also
    nb_examples allows you to specify how many inputs should be
    considered for generating the example table (starting of course at
    the top of the list).
    Finally render_name, if set to True, will cause the function name
    to appear in the first column together with arguments
    """
    def __init__(self, solution, datasets, 
                 copy_mode = 'deep',
                 layout = 'pprint',
                 call_layout = None,
                 render_name = True,
                 nb_examples = 1,
                 layout_args = None,
                 column_headers = None):
        # the 'official' solution
        self.solution = solution
        # the inputs - actually Args instances
        self.datasets = datasets
        # how to copy args
        self.copy_mode = copy_mode
        # applicable to all cells whose Args instance has not specified a layout
        self.layout = layout
        # supersedes the layout in the first column
        self.call_layout = call_layout
        # states if the function name should appear in the call cells
        self.render_name = render_name
        # how many examples 
        self.nb_examples = nb_examples
        # column details - 3-tuples 
        # sizes - defaults should be fine in most cases
        self.layout_args = layout_args 
        # header names - for some odd cases
        self.column_headers = column_headers
        ###
        # in some weird cases this won't exist
        self.name = getattr(solution, '__name__', "no_name")

    def set_call_layout(self):
        "set layout on all Args if/as specified in call_layout"
        if self.call_layout is not None:
            for dataset in self.datasets:
                dataset.set_layout(self.call_layout)

    def correction(self, student_function):
        """
        colums should be a 3-tuple for the 3 columns widths
        copy_mode can be either None, 'shallow', or 'deep' (default)
        """
        self.set_call_layout()
        datasets = self.datasets
        copy_mode = self.copy_mode
        columns = self.layout_args if self.layout_args \
                  else default_layout_args

        c1, c2, c3 = columns
        #print("Using columns={}".format(columns))

        table = Table(style=font_style)
        html = table.header()
        
        if self.column_headers:
            t1, t2, t3 = self.column_headers
        else:
            t1, t2, t3 = ("Arguments" if not self.render_name else "Appel",
                         "Attendu",
                         "Obtenu")
        html += TableRow (
            cells = [ TableCell (CellLegend(x), tag='th', style=center_cell_style)
                      for x in ( t1, t2, t3, '') ],
            style=header_font_style).html()
    
        overall = True
        for dataset in datasets:
            # will use original dataset for rendering to avoid any side-effects
            # during running
            if self.render_name:
                dataset.render_function_name(self.name)
            # always clone all inputs
            student_dataset = dataset.clone(copy_mode)
            ref_dataset = dataset.clone(copy_mode)
            
            # run both codes
            try:
                expected = ref_dataset.call(self.solution, debug=DEBUG)
            except Exception as e:
                expected = e

            try:
                student_result = student_dataset.call(student_function, debug=DEBUG)
            except Exception as e:
                student_result = e
    
            # compare results
            ok = expected == student_result
            if not ok:
                overall = False
            # render that run
            result_cell = '<td style="background-color:green;">'
            message = 'OK' if ok else 'KO'
            style = ok_style if ok else ko_style
            html += TableRow(
                style = style,
                cells = [ TableCell(dataset, layout=self.layout, width=c1),
                          TableCell(expected, layout=self.layout, width=c2),
                          TableCell(student_result, layout=self.layout, width=c3),
                          TableCell(CellLegend(message))]
            ).html()

        log_correction(self.name, overall)
        html += table.footer()
        return HTML(html)

    # public interface
    def example(self, how_many=None):

        self.set_call_layout()
        
        if how_many is None:
            how_many = self.nb_examples
        if how_many == 0:
            how_many = len(self.datasets)
    
        columns = self.layout_args if self.layout_args \
                  else default_layout_args

        # can provide 3 args (convenient when it's the same as correction) or just 2
        columns = columns[:2]
        c1, c2 = columns
        #print("Using columns={}".format(columns))

        table = Table(style=font_style)
        html = table.header()

        title1 = "Arguments" if not self.render_name else "Appel"
        html += TableRow(
            style=header_font_style,
            cells=[ TableCell (CellLegend(x), tag='th', style=center_cell_style)
                    for x in (title1, 'Résultat Attendu') ]
        ).html()
        for dataset in self.datasets[:how_many]:
            sample_dataset = dataset.clone(self.copy_mode)
            if self.render_name:
                dataset.render_function_name(self.name)
            try:
                expected = sample_dataset.call(self.solution)
            except Exception as e:
                expected = e
            html += TableRow(
                cells = [ TableCell(dataset, layout=self.layout, width=c1),
                          TableCell(expected, layout=self.layout, width=c2)
                ]).html()
    
        html += table.footer()
        return HTML(html)

