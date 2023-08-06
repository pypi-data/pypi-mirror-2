#!/usr/bin/env python
import script_util as S

import redhawk.common.xpath as X
import redhawk.common.position as P
import redhawk.utils.get_ast as G

import optparse
import sys

usage = S.MakeStringFromTemplate("""$prog query [options] <query> file1 file2 ..

This command is used to query the ASTs.

For an introduction queries, see the redhawk homepage on PyPi -
http://pypi.python.org/pypi/redhawk

For a further discussion on queries, please read pydoc
redhawk.common.xpath (assuming redhawk is installed on your path).
""")

def Main(args):
  parser = optparse.OptionParser(usage)

  parser.add_option(
      "-C",
      "--context",
      dest = "context",
      type = "int",
      default = None,
      help = "Context to be shown." + S.OPTIONS_DEFAULT_STRING)

  parser.add_option(
      "-n",
      "--no-database",
      action="store_false",
      dest="use_db",
      default=True,
      help = "Explicity tell redhawk to NOT use the database." + S.OPTIONS_DEFAULT_STRING)

  options, args = parser.parse_args(args)
  if not len(args):
      parser.error("No query or files given.")

  parsed_query = X.ParseXPath(args[0])
  if len(args) == 1:
    sys.stderr.write("No files given\n\n")
    sys.stderr.write("Query was parsed as: %s\n"%(parsed_query))
    sys.exit(1)

  database = S.GetDatabase() if options.use_db else None

  files = args[1:]

  ast_fetcher = G.CreateLASTFetcher(database)
  for f in S.GetSupportedFiles(files):
    ast = ast_fetcher.GetAST(f, key=S.GetKey(f, database))
    results = list(X.ApplyParsedXPathQuery([ast], parsed_query))

    if options.context:
      # TODO(spranesh): Fix the context
      for r in results:
        p = P.GetPosition(r)
        print "+++%s:%d"%(f, p.line)
        print P.ShowPosition(p, context = options.context)

    else:
      fp = open(f)
      lines = fp.readlines()
      for r in results:
        p = P.GetPosition(r)
        if len(lines) != 0:
          print "%s:%d:%s"%(f, p.line, lines[p.line-1].strip())
        else:
          print "%s:%d:%s"%(f, p.line, "")
      fp.close()
  ast_fetcher.WriteDatabase()
  return
