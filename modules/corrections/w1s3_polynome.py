# -*- coding: utf-8 -*-
from nbautoeval.exercise_function import ExerciseFunction
from nbautoeval.args import Args

def polynome(x):
    return 2*x*x - 4

inputs_polynome = [
    Args(x) for x in (-2, 0, 2, -10, -4, 3, 10, 100, 10000)
    ]

exo_polynome = ExerciseFunction(
    polynome, inputs_polynome,
    nb_examples = 2,
#    layout_args = (25, 25, 25),
#    render_name = False,
)
