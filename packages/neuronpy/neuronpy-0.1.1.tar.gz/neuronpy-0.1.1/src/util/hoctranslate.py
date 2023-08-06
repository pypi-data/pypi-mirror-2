# -*- coding: utf-8 -*-
"""
Utility methods for translating Python dicts into hoc template objects or
global variables in NEURON accessible to hoc.

@author: - Thomas McTavish
"""
# While this software is under the permissive MIT License, 
# (http://www.opensource.org/licenses/mit-license.php)
# We ask that you cite the neuronpy package (or tools used in this package)
# in any publications and contact the author with your referenced publication.
#
# Format:
# McTavish, T.S. NeuronPy library, version 0.1, http://bitbucket.org/tommctavish/neuronpy
#
# Copyright (c) 2010 Thomas S. McTavish
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

def dict_to_global(hoc, the_dict):
    """
    Translate the numbers an string values of a Python dictionary into global 
    variables in NEURON. The keys of the dict become the variable names in hoc. 
    If the variables already exist,
    they will be overwritten. All values that are ints or floats are translated
    to a double in hoc. Strings are treated as hoc ``strdef`` objects. Any
    other types of the dict are ignored.
    
    :param hoc: A hoc instance as attained by ``from neuron import h``.
    
    :param the_dict: Dict to translate.
    """
    for (key, val) in the_dict.iteritems():
        try:
            if type(val) == type(int()) or \
                type(val) == type(float()):
                exec_str = 'hoc(\"' + key + '=' + str(val) + '\")'
                exec(exec_str)
            elif type(val) == type(str()):
                exec_str = 'hoc(\"strdef ' + key + '\")'
                exec(exec_str)
                exec_str = 'hoc.' + key + '=\"' + str(val) + '\"'
                exec(exec_str)
        except Exception as _ex:
            print _ex # Print the exception, but try to keep going