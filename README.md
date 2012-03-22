# SyntaxHighlighter

SyntaxHighlighter is a light-weight extensible syntax highlighter. Currently supports common languages like C, C++, C#, SQL, Python, Java and the versatile Bash scripting. 
The output formats supported are HTML and RTF and the application is a multi-port b/w C# and Python.

* The application is available both as a standalone and as a library. 
* All the features are fully customizable including the highlight rules, highlight colors, highlight fonts and the library interface can be used with or without additional parameters. 
* Simple addition of adding regex lexers.
* C# version supports a Windows Aero GUI, while the Python version boasts of a versatile command-line support.
* Wrapper for Python 's `re` module to support multiple capture groups.


## Requisites

* C# 
 * .NET Framework 3.5
* Python
 * Python 2.7
 
## Installation

You will need to compile the project in Microsoft Visual Studio 2010 for the C# version.

## License

SyntaxHighlighter is licensed under GNU LGPL v3 (http://www.gnu.org/licenses/lgpl-3.0.html).

SyntaxHighlighter is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SyntaxHighlighter is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with SyntaxHighlighter.  If not, see <http://www.gnu.org/licenses/>.

## Running SyntaxHighlighter

*C#
	Form based selection on the executable.
	
* Python
	Usage Options:
          -i | --input-file      : Input file.
          -o | --output-file     : Output file.
          -t | --highlight-type  : DEFAULT: basic, Type of highlighter (basic, bash, cpp, python, csharp, sql, java, etc.).
          -w | --writer          : DEFAULT: html , Output writer (Currently only html)