#!/usr/bin/env python
""" 
If you are an API user, you should almost always be using get_ast.py, rather
than this module.

This module contains functions that parse files and return asts. The
functions in this module should (generally) not be used directly. Instead, the
wrappers in redhawk/utils/get_last.py are to be used, as they also cache the
ASTs to store unnecessary parsing, and tree conversion.

      * GetLAST: Gets the Language Agnostic AST of a file. Essentially a
        function composition of ConvertAST and ParseFile.

      * ConvertAST: This function converts a language specific AST to the
        L-AST. This function takes an optional filename argument, to fill in
        the Module Node.



      The following functions are NOT required for external use:
      * ParseFile: This function delegates to the corresponding Parse
        function, using the language argument. If the language argument is
        None, utils.GuessLanguage is used.

      * ParsePython: This function parses Python files, and returns a
        python-ast. This function is generally not required for external use.

      * ParseC: This function parses C files, and returns a C-AST. This
        function is generally not required for external use.
"""

import redhawk.c.c_tree_converter as C
import redhawk.python.python_tree_converter as P
import util

import pycparser

import ast
import logging
import os
import sys

def GetLAST(filename, language=None):
  """ Parse the file using the respective parser, and return the Language
  Agnostic AST."""

  return ConvertAST(ParseFile(filename, language)
                    ,language or util.GuessLanguage(filename)
                    ,filename)


def ConvertAST(ast, language, filename=None):
  if language == 'c':
    converter = C.CTreeConverter(filename)
  elif language == 'python':
    converter = P.PythonTreeConverter(filename)
  else:
    raise NotImplementedError("Only C and Python Implemented so far")

  return converter.Convert(ast)




# ####
# Functions that return Language Dependent ASTs

def ParseFile(filename, language=None):
  """ Parse the file using the respective parser, and return a Language
  SPECIFIC ast."""
  language_parsers = {'c'       : ParseC
                     ,'python'  : ParsePython}

  language = language or util.GuessLanguage(filename)
  return language_parsers[language](filename)


def ParseC(filename):
  """ Parse a C file by running it through the preprocessor, and pycparser and
  return the C AST."""
  fake_libc_dir = os.path.join(os.path.dirname(__file__), "fake_libc_include")

  try:
    tree = pycparser.parse_file(filename,
        use_cpp = True,
        cpp_path='cpp',
        cpp_args='-I%s/'%fake_libc_dir)
    return tree
  except pycparser.plyparser.ParseError, e:
    error = "Error parsing file %s with pycparser (with cpp). Skipping\n"%(filename)
    logging.warning(error)
    return None


def ParsePython(filename):
  """ Parse a Python file using the ast module and return the Python AST."""
  # print "FILENAME: ", filename
  try:
    tree = ast.parse(open(filename).read(), filename = filename)
    return tree
  except SyntaxError, e:
    error = "Error parsing file %s with ast module. Skipping\n"%(filename)
    logging.warning(error)
    return None
