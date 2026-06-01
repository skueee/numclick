# Source - https://stackoverflow.com/a/1769577
# Posted by Ned Batchelder
# Retrieved 2026-06-01, License - CC BY-SA 2.5

import sys, token, tokenize, os, io

def do_file(fname):
    """ Run on just one file.

    """
    with open(fname, 'r') as source:
        content = source.read()
    
    mod = open(fname, "w")

    prev_toktype = token.INDENT
    first_line = None
    last_lineno = -1
    last_col = 0
    skip_next_newline = False

    tokgen = tokenize.generate_tokens(io.StringIO(content).readline)
    for toktype, ttext, (slineno, scol), (elineno, ecol), ltext in tokgen:
        if 0:   # Change to if 1 to see the tokens fly by.
            print("%10s %-14s %-20r %r" % (
                tokenize.tok_name.get(toktype, toktype),
                "%d.%d-%d.%d" % (slineno, scol, elineno, ecol),
                ttext, ltext
                ))
        if slineno > last_lineno:
            last_col = 0
        if scol > last_col:
            mod.write(" " * (scol - last_col))
        if toktype == token.STRING and prev_toktype == token.INDENT:
            # Docstring
            mod.write("#--")
        elif toktype == tokenize.COMMENT:
            # Comment
            skip_next_newline = True
            prev_toktype = toktype
            last_col = ecol
            last_lineno = elineno
            continue
        elif skip_next_newline and toktype in (tokenize.NEWLINE, tokenize.NL):
            # Skip newline after comment
            skip_next_newline = False
            prev_toktype = toktype
            last_col = ecol
            last_lineno = elineno
            continue
        else:
            mod.write(ttext)
        prev_toktype = toktype
        last_col = ecol
        last_lineno = elineno
    
    mod.close()

if __name__ == '__main__':
    do_file(sys.argv[1])
