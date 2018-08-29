# -*- coding: utf-8 -*-

# pylint: disable=c0111, c0103, r1705, w0703

from itertools import islice

from IPython.display import HTML

from .log import log_correction
from .rendering import (
    Table, TableRow, TableCell, CellLegend,
    font_style, default_font_size, default_header_font_size,
    ok_style, ko_style,
    center_text_style, left_text_style,
    bottom_border_style, left_border_thick_style, left_border_thin_style,
)


########## defaults for columns widths - for FUN
# this historically was called 'columns' as it was used to specify
# the width of the 3 columns (in correction mode)
# or of the 2 columns (in example mode)
# however when adding new layouts like 'text', the argument passed to the layout
# function ceased to be a column width, so we call this layout_args instead
# but in most cases this does represent column widths
DEFAULT_LAYOUT_ARGS = (24, 28, 28)

##########
def pairwise(it):
    it_left = islice(it, 0, None, 2)
    it_right = islice(it, 1, None, 2)
    return zip(it_left, it_right)

class ScenarioClass(list):
    """
    Describes a scenario that can be applied to a class

    Typically we want to create an instance (using some args),
    and then run some methods (still with some args)

    So a class scenario in its simpler form is defined as a list
    of couples of the form
    ( method_name, Args_object )
    the latter being an instance of ArgsKeywords or Args
    """

    def __init__(self, init_args_obj, *steps_args_obj):
        list.__init__(self)
        if init_args_obj:
            self.set_init_args(init_args_obj)
        for methodname, args_obj in pairwise(steps_args_obj):
            self.add_step(methodname, args_obj)

    def set_init_args(self, args_obj):
        """
        Defines the arguments to constructor
        """
        if self and self[0][0] == '__init__':
            print("Only one __init__ step is allowed")
            return
        self.insert(0, ('__init__', args_obj))

    def add_step(self, methodname, args_obj):
        """
        Scenario is to proceed by calling method
        of that name with these arguments
        """
        self.append((methodname, args_obj,))

##########
class ExerciseClass:                                    # pylint: disable=r0902
    """
    Much like the ExerciseFunction class, this allows to define
    an exercise as
    (*) a solution which is the correct implementation of a class
    (*) a list of scenarios that will be executed on that class

    From that plus a few accessories for fine-grained customization
    we can generate online example and correction.
    """

    def __init__(self, solution, scenarios,             # pylint: disable=r0913
                 copy_mode='deep',
                 layout=None,
                 call_layout=None,
                 nb_examples=1,
                 obj_name='o',
                 layout_args=None,
                 font_size=default_font_size,
                 header_font_size=default_header_font_size):
        self.solution = solution
        self.scenarios = scenarios
        self.copy_mode = copy_mode
        self.layout = layout
        self.call_layout = call_layout
        self.nb_examples = nb_examples
        self.obj_name = obj_name
        self.layout_args = layout_args
        # sizes for the table
        self.font_size = font_size
        self.header_font_size = header_font_size
        # computed
        self.name = solution.__name__

    # adding this feature on ExerciseClass as a mirror of ExerciseFunction
    # but this it is unclear if it's really useful as class exos will be likely
    # to always use the same layout..
    def set_call_layout(self):
        "set layout on all Args if/as specified in call_layout"
        if self.call_layout is not None:
            for scenario in self.scenarios:
                for step in scenario:
                    step[1].set_layout(self.call_layout)

    def correction(self, student_class):        # pylint: disable=r0914, r0915

        self.set_call_layout()

        overall = True

        # should be customizable
        columns = self.layout_args
        if not columns:
            columns = DEFAULT_LAYOUT_ARGS
        c1, c2, c3 = columns
        ref_class = self.solution

        table = Table(style=font_style(self.font_size))
        html = table.header()

        for i, scenario in enumerate(self.scenarios):
            # first step has to be a constructor
            assert len(scenario) >= 1 and scenario[0][0] == '__init__'

            methodname, args_obj = scenario[0]

            # start of scenario
            legend = CellLegend("Scénario {}".format(i+1))
            html += TableRow(
                cells=[TableCell(legend, colspan=4, tag='th',
                                 style='text-align:center')],
                style=font_style(self.header_font_size)).html()
            cells = [TableCell(CellLegend(x), tag='th')
                     for x in ('Appel', 'Attendu', 'Obtenu', '')]
            html += TableRow(cells=cells).html()

            # XXX TODO : take care of copying Args instances before using them

            # initialize both objects
            try:
                # clone args for both usages
                ref_args = args_obj.clone(self.copy_mode)
                student_args = args_obj.clone(self.copy_mode)
                # always render the classname - with a name
                args_obj.render_function_name(self.name)
                args_obj.render_prefix("{}=".format(self.obj_name))
                # initialize both objects
                ref_obj = ref_args.init_obj(ref_class)
                student_obj = student_args.init_obj(student_class)
                cells = (TableCell(args_obj, layout=self.layout, width=c1),
                         TableCell(CellLegend('-'),
                                   style=left_border_thick_style),
                         TableCell(CellLegend('-'),
                                   style=left_border_thin_style),
                         TableCell(CellLegend('OK'),
                                   style=left_border_thick_style))
                html += TableRow(cells=cells, style=ok_style).html()
            except Exception as e:
                import traceback
                traceback.print_exc()
                cell1 = TableCell(args_obj, layout=self.layout, width=c1+c2,
                                  colspan=2)
                error = "Exception {}".format(e)
                cell2 = TableCell(CellLegend(error), width=c3,
                                  style=left_border_thick_style)
                cell3 = TableCell(CellLegend('KO'),
                                  style=left_border_thick_style)
                html += TableRow(cells=(cell1, cell2, cell3),
                                 style=ko_style).html()
                overall = False
                continue

            # other steps of that scenario
            for methodname, args_obj in scenario[1:]:
                # clone args for both usages
                ref_args = args_obj.clone(self.copy_mode)
                student_args = args_obj.clone(self.copy_mode)
                # so that we display the function name
                args_obj.render_function_name(methodname)
                args_obj.render_prefix("{}.".format(self.obj_name))
                ref_result = ref_args.call_obj(ref_obj, methodname)
                try:
                    student_result = student_args.call_obj(student_obj, methodname)
                    if ref_result == student_result:
                        style = ok_style
                        msg = 'OK'
                    else:
                        style = ko_style
                        msg = 'KO'
                        overall = False
                except Exception as e:
                    style = ko_style
                    msg = 'KO'
                    overall = False
                    student_result = "Exception {}".format(e)

                # xxx styling maybe a little too much...
                cells = (TableCell(args_obj, layout=self.layout, width=c1),
                         TableCell(ref_result, layout=self.layout, width=c2,
                                   style=left_border_thick_style
                                   +left_text_style),
                         TableCell(student_result, layout=self.layout, width=c3,
                                   style=left_border_thin_style
                                   +left_text_style),
                         TableCell(CellLegend(msg),
                                   style=left_border_thick_style))
                html += TableRow(cells=cells, style=style).html()

        log_correction(self.name, overall)

        html += "</table>"

        return HTML(html)

    def example(self):                                  # pylint: disable=r0914
        """
        display a table with example scenarios
        """
        self.set_call_layout()
        columns = self.layout_args if self.layout_args \
                  else DEFAULT_LAYOUT_ARGS
        ref_class = self.solution

        how_many_samples = self.nb_examples if self.nb_examples \
                           else len(self.scenarios)

        # can provide 3 args (convenient when it's the same as correction) or just 2
        columns = columns[:2]
        c1, c2 = columns
        #print("Using columns={}".format(columns))
        table = Table(style=font_style(self.font_size))
        html = table.header()

        sample_scenarios = self.scenarios[:how_many_samples]
        for i, scenario in enumerate(sample_scenarios):
            # first step has to be a constructor
            assert len(scenario) >= 1 and scenario[0][0] == '__init__'

            methodname, args_obj = scenario[0]
            # always render the classname
            args_obj.render_function_name(self.name)

            # start of scenario
            legend = CellLegend("Scénario {}".format(i+1))
            html += TableRow(
                cells=[TableCell(legend, colspan=4, tag='th',
                                 style=center_text_style)],
                style=font_style(self.header_font_size)).html()
            cells = [TableCell(CellLegend(x), tag='th')
                     for x in ('Appel', 'Attendu')]
            html += TableRow(cells=cells).html()

            ref_args = args_obj.clone(self.copy_mode)
            ref_args.render_function_name(self.name)
            ref_obj = ref_args.init_obj(ref_class)
            cells = (TableCell(args_obj, layout=self.layout, width=c1),
                     TableCell(CellLegend('-'),
                               style=left_border_thick_style
                               + left_text_style))
            html += TableRow(cells=cells).html()

            for methodname, args_obj in scenario[1:]:
                ref_args = args_obj.clone(self.copy_mode)
                ref_args.render_function_name(methodname)
                ref_result = ref_args.call_obj(ref_obj, methodname)
                cells = (TableCell(ref_args, layout=self.layout, width=c1),
                         TableCell(ref_result, layout=self.layout, width=c2,
                                   style=left_border_thick_style
                                   +left_text_style))
                html += TableRow(cells=cells).html()

        html += table.footer()
        return HTML(html)
