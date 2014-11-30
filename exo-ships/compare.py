#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

class FileComparator(object):
    def __init__(self, out_name, ref_name=None):
        self.out_name = out_name
        self.ref_name = ref_name or "{}.ref".format(self.out_name)
        
    def _compare(self):
        """return True if files match"""
        outputs = [None, None]
        for i, name in enumerate( [self.out_name, self.ref_name] ):
            try:
                with open(name, "ru") as output:
                    outputs[i] = output.read()
            except Exception as e:
                print ("Could not read output {}".format(name))
                return False
        if outputs[0] == outputs[1]:
            return True
        # xxx improve me : could use a little more details here
        else:
            return False

    def compare(self):
        bool_result = self._compare()
        status = "OK" if bool_result else "KO"
        message = "Comparison between {self.out_name} and {self.ref_name} -> {status}".\
                  format(**locals())
        print (message)
        return bool_result

