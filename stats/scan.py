#!/usr/bin/env python

from __future__ import print_function

import sys
import os.path
import traceback

from glob import glob

from argparse import ArgumentParser

class Attempts:
    def __init__(self):
        self.ok = 0
        self.ko = 0
    def record(self, msg):
        if msg=="OK":
            self.ok += 1
        else:
            self.ko += 1
    def __repr__(self):
        return "{} ok + {} ko = {}".format(self.ok, self.ko, self.ok + self.ko)

def scan (dirname):
    nb_dirs = 0
    nb_students = 0
    total_attempts = Attempts()
    attempts_by_exo = {}

    subdirs = glob (os.path.join(dirname,"*"))
    for subdir in subdirs:
        nb_dirs += 1
        try:
            with open(os.path.join(subdir,".correction")) as log:
                nb_students += 1
                for lineno,line in enumerate(log):
                    try:
                        date, id1, id2, function, result = line.split()
                        attempts_by_exo.setdefault(function, Attempts())
                        attempts_by_exo[function].record(result)
                        total_attempts.record(result)
                    except:
                        print ('skipping line=', line, '\tin subdir', subdir, file=sys.stderr)
                        pass
        except:
            traceback.print_exc()
            pass

    print ("{nb_students} students have tried at least once".format(**locals()))
    if nb_dirs != nb_students:
        print ("{nb_dirs} dirs were found (should be {nb-students})".format(**locals()))

    ok = total_attempts.ok
    ko = total_attempts.ko
    total = ok + ko
    exos = len(attempts_by_exo)
    trials_per_student = total / float(nb_students)
    ratio = float(ok)/total
    print ("""  {ok} ok (successful) trials
+ {ko} ko (unsuccessful) trials
= {total} total trials ({ratio}% success)

{exos} different exercices -> an average of {trials_per_student} attempts per student"""\
    .format(**locals()))

    print ()

    for function in sorted(attempts_by_exo):
        print (function, attempts_by_exo[function])

    return nb_dirs, nb_students, total_attempts, attempts_by_exo
        



parser = ArgumentParser()
parser.add_argument ("dirname")
args = parser.parse_args()

scanned = scan (args.dirname)

