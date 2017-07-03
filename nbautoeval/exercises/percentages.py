# -*- coding: utf-8 -*-

# importing the ExerciseFunction class
from nbautoeval.exercise_function import ExerciseFunction
# the Args object is for defining inputs 
from nbautoeval.args import Args

# 
nucleotides = 'CAGT'

# As a side note, I also have a simple tool for collecting corrections
# and publish them in pdf format.
# This is what the @BEG@ / @END@ thingy is for, just ignore this for now

########## step 1
# You need to define the correct function 

# @BEG@ name=percentages
def percentages(adn):
    "calcule des percentages de CAGT dans un adn"
    total = len(adn)
    return {
        nucleotide : len([p for p in adn if p == nucleotide])*100./total
        for nucleotide in nucleotides
    }
# @END@

# xxx to be clarified : there may be some code that uses this
# but I can't remember it off the top of my head
#def percentages_ko():
#    return { p:0.25 for p in nucleotides }

########## step 2
# You need to provide datasets<
# This is expected to be a list of Args instances
# each one describes all the arguments to be passed
# to the function
# in this particular case we define 2 input sets, so
# the correction will have 2 meaningful rows
inputs_percentages = [
    Args('ACGTACGA'),
    Args('ACGTACGATCGATCGATGCTCGTTGCTCGTAGCGCT'),
]

########## step 3
# finally we create the exercise object
# NOTE on names:
# 
# this is the only name that should be imported from this module
exo_percentages = ExerciseFunction(
    # first argument is the 'correct' function
    # it is recommended to use the same name as in the notebook, as the
    # python function name is used in HTML rendering 
    percentages,
    # the inputs
    inputs_percentages,
    # various tweaks on how to display input arguments
    layout='pprint',
    # in particular here, the widths of the first 3 columns in the correction table
    layout_args=(40, 25, 25),
)
