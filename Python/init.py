'''
Created on Nov 11, 2011
@author: Nisheeth Barthwal
@contact: nbaztec@gmail.com
@copyright: Nisheeth Barthwal, 2011
@summary: This is the primary interface for the highlighter. This module is not required for the library to work and can be modified as required. 

@license: 
NX - Syntax Highlighter, an open source library for syntax highlighting in RTF and HTML
    Copyright (C) 2011 Nisheeth Barthwal

This file is part of NX - Syntax Highlighter.

    NX - Syntax Highlighter is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    NX - Syntax Highlighter is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with NX - Syntax Highlighter.  If not, see <http://www.gnu.org/licenses/>.
'''

import getopt
import sys

# @note: Variables for script.    
ifile = "-"             # Input file.  Default: <stdin>
ofile = "-";            # Output file. Default: <stdout>
highlighter = "basic"   # Highlighter. Default: BasicHighlighter
writer = "html"         # Writer.      Default: HtmlWriter

def usage():
    """
        @summary: Prints the usage details for the program.
    """
    hlp = """Usage Options:
          -i | --input-file      : Input file.
          -o | --output-file     : Output file.
          -t | --highlight-type  : DEFAULT: basic, Type of highlighter (basic, bash, cpp, python, csharp, sql, java, etc.).
          -w | --writer          : DEFAULT: html , Output writer (Currently only html)
          """
    print hlp

    
def getArgs():
    """
        @summary: Initializes the arguments for the program. 
    """
    global ifile, ofile, highlighter, writer
    try:
        opts, unused_args = getopt.getopt(sys.argv[1:], "i:o:t:w:h", ["input-file=", "output-file=", "highlight-type=", "writer=", "--help"])        
        for o,v in opts:                                    
            if o in ['-i', '--input-file']: 
                ifile = v
            elif o in ['-o', '--output-file']: 
                ofile = v
            elif o in ['-t', '--highlight-type']: 
                highlighter = v
            elif o in ['-h', '--help']:
                usage()
                sys.exit(0)
            # @attention: Only HtmlWriter is supported as of version 1.x  
            #elif o in ['-w', '--writer']: 
            #    writer = v                        
    except getopt.GetoptError, err:        
        print str(err)
        usage()
        sys.exit(2)

if __name__ == "__main__":
    getArgs()        
    import NX.SyntaxHighlighter.Highlighters.Internal as internal   # Import the internal in-built highlighters 
    if highlighter == "basic":
        sh = internal.BasicHighlighter()
    elif highlighter == "bash":
        sh = internal.BashHighlighter()
    elif highlighter == "cpp":
        sh = internal.CppHighlighter()
    elif highlighter == "csharp":
        sh = internal.CSharpHighlighter()
    elif highlighter == "python":
        sh = internal.PythonHighlighter()    
    # @attention: Insert custom highlighters here. 
    # Example:
    # elif highlighter == "my_highlighter":
    #     sh = MyHighlighter()
    else:
        print "The highlighter '%s' is not supported/cannot be found." % highlighter
        sys.exit(1)
    
    if ifile == "-":        
        print "Enter text:"
        data = "".join(sys.stdin.readlines())
    else:
        with open(ifile, "r") as inFile:
            data = inFile.read()      
    
    if ofile == "-":
        print sh.Highlight(data,ifile if ifile != "-" else None)
    else:  
        with open(ofile, "w") as f:    
            f.write(sh.Highlight(data, ifile if ifile != "-" else None))     
    
        
        
            