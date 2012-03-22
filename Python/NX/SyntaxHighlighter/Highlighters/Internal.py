'''
Created on Nov 11, 2011
@author: Nisheeth Barthwal
@contact: nbaztec@gmail.com
@copyright: Nisheeth Barthwal, 2011
@summary: This Module contains the Base classes to go with the SyntaxHighlighter. These include Fonts, Colors & Writers

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

from NX.Enum import Color
from NX.Main import FontStyle
from NX.SyntaxHighlighter.Base import SyntaxHighlighter, HighlightColor, HighlightFont, HighlightRule, HighlightRegex


class BasicHighlighter(SyntaxHighlighter):    
    """        
        @summary: A Simple Basic Highlighter
    """
    
    #Init
    def __init__(self, highlightRules=None, defaultForeground=None, defaultBackground=None, defaultFont=None, keywords=None, commands=None, defaultWriter=None):        
        super(BasicHighlighter, self).__init__(highlightRules, defaultForeground, defaultBackground, defaultFont, keywords, commands, defaultWriter)        
    
    #Overridden Method
    def SetLanguageWords(self):
        self.Keywords = "if|else|for|while"
        self.Commands = "echo|exit"
    
    def SetDefaultRules(self):
        self._highlightRules.AddRule(
                                     "dquote", 
                                     HighlightRule(HighlightRegex.QuotedString("dquote", '"'), HighlightColor("E60000"), None, None), 
                                     None
                                     )
        self._highlightRules.AddRule(
                                     "char", 
                                     HighlightRule(HighlightRegex.QuotedChar("char", "'"), HighlightColor("E60000"), None, None), 
                                     None
                                     )        
        self._highlightRules.AddRule(
                                     "comment", 
                                     HighlightRule(HighlightRegex.SingleLineComment("comment", '#'), HighlightColor(Color.Green), HighlightColor(Color.LightGray), HighlightFont(self.DefaultFont.FontName, self.DefaultFont.FontSize, FontStyle.Italic)), 
                                     None
                                     )
        self._highlightRules.AddRule(
                                     "keyword", 
                                     HighlightRule(HighlightRegex.LanguageWords("keyword", self.Keywords), HighlightColor(Color.Blue), None, HighlightFont(self.DefaultFont.FontName, self.DefaultFont.FontSize, FontStyle.Bold)), 
                                     None
                                     )
        self._highlightRules.AddRule(
                                     "command", 
                                     HighlightRule(HighlightRegex.LanguageWords("command", self.Commands), HighlightColor(Color.Chocolate), None, HighlightFont(self.DefaultFont.FontName, self.DefaultFont.FontSize, FontStyle.Regular)), 
                                     None
                                     )

class BashHighlighter(SyntaxHighlighter):    
    """
        @summary: Bash Script Highlighter
    """
    
    #Init
    def __init__(self, highlightRules=None, defaultForeground=None, defaultBackground=None, defaultFont=None, keywords=None, commands=None, defaultWriter=None):        
        super(BashHighlighter, self).__init__(highlightRules, defaultForeground, defaultBackground, defaultFont, keywords, commands, defaultWriter)        
    
    #Overridden Method
    def SetLanguageWords(self):
        self.Keywords = "if|then|else|elif|fi|for|done|do|while|in|case|esac|break|continue|function|return|in"
        self.Commands = "alias|apropos|awk|basename|bash|bc|bg|builtin|bzip2|cal|cat|cd|cfdisk|chgrp|chmod|chown|chroot|cksum|clear|cmp|comm|command|cp|cron|crontab|csplit|cut|date|dc|dd|ddrescue|declare|df|diff|diff3|dig|dir|dircolors|dirname|dirs|du|echo|egrep|eject|enable|env|ethtool|eval|exec|exit|expand|export|expr|false|fdformat|fdisk|fg|fgrep|file|find|fmt|fold|format|free|fsck|ftp|gawk|getopts|grep|groups|gzip|hash|head|history|hostname|id|ifconfig|import|install|join|kill|less|let|ln|local|locate|logname|logout|look|lpc|lpr|lprint|lprintd|lprintq|lprm|ls|lsof|make|man|mkdir|mkfifo|mkisofs|mknod|more|mount|mtools|mv|netstat|nice|nl|nohup|nslookup|open|op|passwd|paste|pathchk|ping|popd|pr|printcap|printenv|printf|ps|pushd|pwd|quota|quotacheck|quotactl|ram|rcp|read|readonly|renice|remsync|rm|rmdir|rsync|screen|scp|sdiff|sed|select|seq|set|sftp|shift|shopt|shutdown|sleep|sort|source|split|ssh|strace|su|sudo|sum|symlink|sync|tail|tar|tee|test|time|times|touch|top|traceroute|trap|tr|true|tsort|tty|type|ulimit|umask|umount|unalias|uname|unexpand|uniq|units|unset|unshar|useradd|usermod|users|uuencode|uudecode|v|vdir|vi|watch|wc|whereis|which|who|whoami|Wget|xargs|yes"
        
    def SetDefaultRules(self):
        self._highlightRules.AddRule(
                                     "dquote", 
                                     HighlightRule(HighlightRegex.QuotedString("dquote", '"'), HighlightColor("E60000"), None, None),
                                     [ "backtick", "refvar", "varblock_same", "varblock_diff", "let" ]
                                     )
        self._highlightRules.AddRule(
                                     "squote", 
                                     HighlightRule(HighlightRegex.QuotedString("squote", "'"), HighlightColor("E60000"), None, None),
                                     None
                                     )        
        self._highlightRules.AddRule(
                                     "comment", 
                                     HighlightRule(HighlightRegex.SingleLineComment("comment", '#'), HighlightColor(Color.CornflowerBlue), None, HighlightFont(self.DefaultFont.FontName, self.DefaultFont.FontSize, FontStyle.Regular)), 
                                     None
                                     )
        self._highlightRules.AddRule(
                                     "var", 
                                     HighlightRule(r'(?:^\s*)(?P<var>[A-Za-z_][\w\d_]*?(?==))', HighlightColor(Color.DarkCyan), None, None),
                                     None
                                     )
        # ${}
        self._highlightRules.AddRule(
                                     "varblock_same", 
                                     HighlightRule(HighlightRegex.SingleLineReferencedBlock("varblock", "refvar", "{", "}", '#'), None, None, None),  # Additional special char which is not allowed as it's for comment
                                     [ "refvar", "varblock_diff", "let", "keyword", "command", "option", "squote", "dquote"]
                                     )
        # $()
        self._highlightRules.AddRule(
                                     "varblock_diff", 
                                     HighlightRule(HighlightRegex.SingleLineReferencedBlock("varblock", "varblock_diff", "(", ")", "#"), HighlightColor(Color.Indigo), None, None),
                                     None
                                     )
        # (( ))
        self._highlightRules.AddRule(
                                     "let", 
                                     HighlightRule(r'(?:(?<!\\)(?:(?:\\{2})+)|[^\\])(?:(?P<varblock>(?P<let>\$\({2}\s+[A-Za-z0-9_]*)(?:[^)])*(?P<let>\)\))))', HighlightColor("FF33FF"), None, None),
                                     None
                                     )
        self._highlightRules.AddRule(
                                     "refvar", 
                                     HighlightRule(HighlightRegex.ReferencedVariable("refvar", "$"), HighlightColor(Color.BlueViolet),None, None), 
                                     None
                                     )
        self._highlightRules.AddRule(
                                     "keyword", 
                                     HighlightRule(HighlightRegex.LanguageWords("keyword", self.Keywords), HighlightColor(Color.Brown), None, HighlightFont(self.DefaultFont.FontName, self.DefaultFont.FontSize, FontStyle.Bold)), 
                                     None
                                     )
        self._highlightRules.AddRule(
                                     "command", 
                                     HighlightRule(HighlightRegex.LanguageWords("command", self.Commands), HighlightColor(Color.Chocolate), None, HighlightFont(self.DefaultFont.FontName, self.DefaultFont.FontSize, FontStyle.Regular)), 
                                     None
                                     )
        self._highlightRules.AddRule(
                                     "option", 
                                     HighlightRule(r'(?P<option>\s+--?[\w\d]+)', HighlightColor(Color.DarkGoldenRod), None, None), 
                                     None
                                     )
        self._highlightRules.AddRule(
                                     "test", 
                                     HighlightRule(r'(?:\s+)(?P<test>\[(?:"(?:(?:\\"|[^"])*")|[^\]])*\])', None, HighlightColor(Color.PapayaWhip), None), 
                                     [ "keyword", "command", "dquote", "squote", "refvar", "varblock_same", "varblock_diff", "let", "option" ]
                                     )
        self._highlightRules.AddRule(
                                     "backtick", 
                                     HighlightRule(r'(?:\s+)(?P<backtick>`[^`]*`)', None, HighlightColor(Color.PapayaWhip), None), 
                                     [ "keyword", "command", "dquote", "squote", "refvar", "varblock_same", "varblock_diff", "let", "option" ]
                                     )
        
        # Example: Simple HighlightRule
            # self._highlightRules.AddRule("varblock_highlight", HighlightRule(None, HighlightColor(Color.BlueViolet), None, None), None)
        
        # Simple Dependency Rule
        self._highlightRules.AddRule("varblock", None, [ "refvar", "varblock_same", "varblock_diff", "let", "keyword", "command", "option", "squote", "dquote" ])                

class CppHighlighter(SyntaxHighlighter):    
    """
        @summary: C++ Highlighter
    """
    
    # Init
    def __init__(self, highlightRules=None, defaultForeground=None, defaultBackground=None, defaultFont=None, keywords=None, commands=None, defaultWriter=None):        
        super(CppHighlighter, self).__init__(highlightRules, defaultForeground, defaultBackground, defaultFont, keywords, commands, defaultWriter)        
    
    # Overridden Method
    # @attention: You can add personal language words to use while setting rules as well.
    def SetLanguageWords(self):
        self.Keywords = "signed|break|case|catch|class|const|__finally|__exception|__try|const_cast|__fastcall|continue|private|public|protected|__declspec|default|delete|deprecated|dllexport|dllimport|do|dynamic_cast|else|enum|explicit|extern|if|for|friend|goto|inline|mutable|naked|namespace|new|noinline|noreturn|nothrow|register|reinterpret_cast|return|selectany|sizeof|static|static_cast|struct|switch|template|this|thread|throw|true|false|try|typedef|typeid|typename|union|using|uuid|virtual|void|volatile|whcar_t|while";
        self.Commands = "assert|isalnum|isalpha|iscntrl|isdigit|isgraph|islower|isprint|ispunct|isspace|isupper|isxdigit|tolower|toupper|errno|localeconv|setlocale|acos|asin|atan|atan2|ceil|cos|cosh|exp|fabs|floor|fmod|frexp|ldexp|log|log10|modf|pow|sin|sinh|sqrt|tan|tanh|jmp_buf|longjmp|setjmp|raise|signal|sig_atomic_t|va_arg|va_end|va_start|clearerr|fclose|feof|ferror|fflush|fgetc|fgetpos|fgets|fopen|fprintf|fputc|fputs|fread|freopen|fscanf|fseek|fsetpos|ftell|fwrite|getc|getchar|gets|perror|printf|putc|putchar|puts|remove|rename|rewind|scanf|setbuf|setvbuf|sprintf|sscanf|tmpfile|tmpnam|ungetc|vfprintf|vprintf|vsprintf|abort|abs|atexit|atof|atoi|atol|bsearch|calloc|div|exit|free|getenv|labs|ldiv|malloc|mblen|mbstowcs|mbtowc|qsort|rand|realloc|srand|strtod|strtol|strtoul|system|wcstombs|wctomb|memchr|memcmp|memcpy|memmove|memset|strcat|strchr|strcmp|strcoll|strcpy|strcspn|strerror|strlen|strncat|strncmp|strncpy|strpbrk|strrchr|strspn|strstr|strtok|strxfrm|asctime|clock|ctime|difftime|gmtime|localtime|mktime|strftime|time";
        self.Datatypes = "ATOM|BOOL|BOOLEAN|BYTE|CHAR|COLORREF|DWORD|DWORDLONG|DWORD_PTR|DWORD32|DWORD64|FLOAT|HACCEL|HALF_PTR|HANDLE|HBITMAP|HBRUSH|HCOLORSPACE|HCONV|HCONVLIST|HCURSOR|HDC|HDDEDATA|HDESK|HDROP|HDWP|HENHMETAFILE|HFILE|HFONT|HGDIOBJ|HGLOBAL|HHOOK|HICON|HINSTANCE|HKEY|HKL|HLOCAL|HMENU|HMETAFILE|HMODULE|HMONITOR|HPALETTE|HPEN|HRESULT|HRGN|HRSRC|HSZ|HWINSTA|HWND|INT|INT_PTR|INT32|INT64|LANGID|LCID|LCTYPE|LGRPID|LONG|LONGLONG|LONG_PTR|LONG32|LONG64|LPARAM|LPBOOL|LPBYTE|LPCOLORREF|LPCSTR|LPCTSTR|LPCVOID|LPCWSTR|LPDWORD|LPHANDLE|LPINT|LPLONG|LPSTR|LPTSTR|LPVOID|LPWORD|LPWSTR|LRESULT|PBOOL|PBOOLEAN|PBYTE|PCHAR|PCSTR|PCTSTR|PCWSTR|PDWORDLONG|PDWORD_PTR|PDWORD32|PDWORD64|PFLOAT|PHALF_PTR|PHANDLE|PHKEY|PINT|PINT_PTR|PINT32|PINT64|PLCID|PLONG|PLONGLONG|PLONG_PTR|PLONG32|PLONG64|POINTER_32|POINTER_64|PSHORT|PSIZE_T|PSSIZE_T|PSTR|PTBYTE|PTCHAR|PTSTR|PUCHAR|PUHALF_PTR|PUINT|PUINT_PTR|PUINT32|PUINT64|PULONG|PULONGLONG|PULONG_PTR|PULONG32|PULONG64|PUSHORT|PVOID|PWCHAR|PWORD|PWSTR|SC_HANDLE|SC_LOCK|SERVICE_STATUS_HANDLE|SHORT|SIZE_T|SSIZE_T|TBYTE|TCHAR|UCHAR|UHALF_PTR|UINT|UINT_PTR|UINT32|UINT64|ULONG|ULONGLONG|ULONG_PTR|ULONG32|ULONG64|USHORT|USN|VOID|WCHAR|WORD|WPARAM|WPARAM|WPARAM|char|bool|short|int|__int32|__int64|__int8|__int16|long|float|double|__wchar_t|clock_t|_complex|_dev_t|_diskfree_t|div_t|ldiv_t|_exception|_EXCEPTION_POINTERS|FILE|_finddata_t|_finddatai64_t|_wfinddata_t|_wfinddatai64_t|__finddata64_t|__wfinddata64_t|_FPIEEE_RECORD|fpos_t|_HEAPINFO|_HFILE|lconv|intptr_t|jmp_buf|mbstate_t|_off_t|_onexit_t|_PNH|ptrdiff_t|_purecall_handler|sig_atomic_t|size_t|_stat|__stat64|_stati64|terminate_function|time_t|__time64_t|_timeb|__timeb64|tm|uintptr_t|_utimbuf|va_list|wchar_t|wctrans_t|wctype_t|wint_t";
        
    def SetDefaultRules(self):
        self._highlightRules.AddRule(
                                     "dquote", 
                                     HighlightRule(HighlightRegex.QuotedString("dquote", '"'), HighlightColor("E60000"), None, None),
                                     None
                                     )
        self._highlightRules.AddRule(
                                     "char", 
                                     HighlightRule(HighlightRegex.QuotedChar("char", "'"), HighlightColor(Color.Fuchsia), None, None),
                                     None
                                     )        
        self._highlightRules.AddRule(
                                     "comment", 
                                     HighlightRule(HighlightRegex.SingleLineComment("comment", '//'), HighlightColor(Color.Green), None, HighlightFont(self.DefaultFont.FontName, self.DefaultFont.FontSize, FontStyle.Regular)), 
                                     None
                                     )
        self._highlightRules.AddRule(
                                     "mcomment", 
                                     HighlightRule(HighlightRegex.MultiLineComment("mcomment", "/*", "*/"), HighlightColor(Color.Green), None, None),
                                     None
                                     )        
        self._highlightRules.AddRule(
                                     "preprocess",  # Using a custom Preprocessor regex. Break at `/`, but resume if not a comment
                                     HighlightRule(HighlightRegex.Preprocessor("preprocess", "#", "/", "|/[^/*]"), HighlightColor(Color.CornflowerBlue), None, None),
                                     None
                                     )        
        self._highlightRules.AddRule(
                                     "keyword", 
                                     HighlightRule(HighlightRegex.LanguageWords("keyword", self.Keywords), HighlightColor(Color.Purple), None, HighlightFont(self.DefaultFont.FontName, self.DefaultFont.FontSize, FontStyle.Bold)), 
                                     None
                                     )
        self._highlightRules.AddRule(
                                     "command", 
                                     HighlightRule(HighlightRegex.LanguageWords("command", self.Commands), HighlightColor(Color.Chocolate), None, HighlightFont(self.DefaultFont.FontName, self.DefaultFont.FontSize, FontStyle.Regular)), 
                                     None
                                     )
        self._highlightRules.AddRule(
                                     "datatype", 
                                     HighlightRule(HighlightRegex.LanguageWords("datatype", self.Datatypes), HighlightColor(Color.RoyalBlue), None, None), 
                                     None
                                     )

class PythonHighlighter(SyntaxHighlighter):    
    """
        @summary: C++ Highlighter
    """
    
    # Init
    def __init__(self, highlightRules=None, defaultForeground=None, defaultBackground=None, defaultFont=None, keywords=None, commands=None, defaultWriter=None):        
        super(PythonHighlighter, self).__init__(highlightRules, defaultForeground, defaultBackground, defaultFont, keywords, commands, defaultWriter)        
    
    # Overridden Method
    # @attention: You can add personal language words to use while setting rules as well.
    def SetLanguageWords(self):
        self.Keywords = "and|assert|break|class|continue|def|del|elif|else|except|exec|finally|for|from|global|if|import|in|is|lambda|not|or|pass|print|raise|return|try|yield|while";
        self.Commands = "__import__|__init__|__str__|__iter__|abs|all|any|apply|basestring|bin|bool|buffer|callable|chr|classmethod|cmp|coerce|compile|complex|delattr|dict|dir|divmod|enumerate|eval|execfile|file|filter|float|format|frozenset|getattr|globals|hasattr|hash|help|hex|id|input|int|intern|isinstance|issubclass|iter|len|list|locals|long|map|max|min|next|object|oct|open|ord|pow|print|property|range|raw_input|reduce|reload|repr|reversed|round|set|setattr|slice|sorted|staticmethod|str|sum|super|tuple|type|type|unichr|unicode|vars|xrange|zip";
        self.Values = "None|True|False|self|cls|class_";
        
    def SetDefaultRules(self):
        self._highlightRules.AddRule(
                                     "tripledquote", 
                                     HighlightRule(HighlightRegex.MultiLineQuotedString("tripledquote", '"""', '"', '|"(?!"")'), HighlightColor(Color.Green), None, None),
                                     None
                                     )
        self._highlightRules.AddRule(
                                     "triplesquote", 
                                     HighlightRule(HighlightRegex.MultiLineQuotedString("triplesquote", "'''", "'", "|'(?!'')"), HighlightColor(Color.Green), None, None),
                                     None
                                     )
        self._highlightRules.AddRule(
                                     "dquote", 
                                     HighlightRule(HighlightRegex.QuotedString("dquote", '"'), HighlightColor(Color.Green), None, None),
                                     None
                                     )
        self._highlightRules.AddRule(
                                     "squote", 
                                     HighlightRule(HighlightRegex.QuotedString("squote", "'"), HighlightColor(Color.Green), None, None),
                                     None
                                     )        
        self._highlightRules.AddRule(
                                     "value", 
                                     HighlightRule(r'\b(?P<value>\d+\.?\w*)', HighlightColor(Color.Fuchsia), None, None),
                                     None
                                     )        
        self._highlightRules.AddRule(
                                     "comment", 
                                     HighlightRule(HighlightRegex.SingleLineComment("comment", '#'), HighlightColor(Color.Gray), None, HighlightFont(self.DefaultFont.FontName, self.DefaultFont.FontSize, FontStyle.Regular)), 
                                     None
                                     )           
        self._highlightRules.AddRule(
                                     "decorator",  # Using a custom Preprocessor regex. Break at `/`, but resume if not a comment
                                     HighlightRule(HighlightRegex.Preprocessor("decorator", "@", "#'", "|'[^'][^']"), HighlightColor(Color.CornflowerBlue), None, None),
                                     None
                                     )        
        self._highlightRules.AddRule(
                                     "keyword", 
                                     HighlightRule(HighlightRegex.LanguageWords("keyword", self.Keywords), HighlightColor(Color.Purple), None, HighlightFont(self.DefaultFont.FontName, self.DefaultFont.FontSize, FontStyle.Bold)), 
                                     None
                                     )
        self._highlightRules.AddRule(
                                     "command", 
                                     HighlightRule(HighlightRegex.LanguageWords("command", self.Commands), HighlightColor(Color.Chocolate), None, HighlightFont(self.DefaultFont.FontName, self.DefaultFont.FontSize, FontStyle.Regular)), 
                                     None
                                     )
        self._highlightRules.AddRule(
                                     "values", 
                                     HighlightRule(HighlightRegex.LanguageWords("values", self.Values), HighlightColor(Color.RoyalBlue), None, None), 
                                     None
                                     )                                        

class CSharpHighlighter(SyntaxHighlighter): 
    """
        @summary: C# Highlighter
    """
    
    # Init
    def __init__(self, highlightRules=None, defaultForeground=None, defaultBackground=None, defaultFont=HighlightFont("Consolas", 12, FontStyle.Regular), keywords=None, commands=None, defaultWriter=None):        
        super(CSharpHighlighter, self).__init__(highlightRules, defaultForeground, defaultBackground, defaultFont, keywords, commands, defaultWriter)        
    
    # Overridden Method
    # @attention: You can add personal language words to use while setting rules as well.
    def SetLanguageWords(self):
        self.Keywords = "abstract|event|new|struct|as|explicit|null|switch|base|extern|object|this|bool|false|operator|throw|break|finally|out|true|byte|fixed|override|try|case|float|params|typeof|catch|for|private|uint|char|foreach|protected|ulong|checked|goto|public|unchecked|class|if|readonly|unsafe|const|implicit|ref|ushort|continue|in|return|using|decimal|int|sbyte|virtual|default|interface|sealed|volatile|delegate|internal|short|void|do|is|sizeof|while|double|lock|stackalloc|else|long|static|enum|namespace|string|get|partial|set|value|where|yield";        
        self.Classes = "DllImport|StructLayout|List|Dictionary|String|Object|Enum|Array|ArrayList|BitArray|CaseInsensitiveComparer|CaseInsensitiveHashCodeProvider|CollectionBase|Comparer|DictionaryBase|Hashtable|Queue|ReadOnlyCollectionBase|SortedList|Stack|StructuralComparisons";        
        
    def SetDefaultRules(self):
        self._highlightRules.AddRule(
                                     "dquote", 
                                     HighlightRule(HighlightRegex.QuotedString("dquote", '"'), HighlightColor(Color.DarkRed), None, None),
                                     None
                                     )
        self._highlightRules.AddRule(
                                     "char", 
                                     HighlightRule(HighlightRegex.QuotedChar("char", "'"), HighlightColor("E60000"), None, None),
                                     None
                                     )        
        self._highlightRules.AddRule(
                                     "comment", 
                                     HighlightRule(HighlightRegex.SingleLineComment("comment", '//'), HighlightColor(Color.Green), None, HighlightFont(self.DefaultFont.FontName, self.DefaultFont.FontSize, FontStyle.Regular)), 
                                     None
                                     )
        self._highlightRules.AddRule(
                                     "mcomment", 
                                     HighlightRule(HighlightRegex.MultiLineComment("mcomment", "/*", "*/"), HighlightColor(Color.Green), None, None),
                                     None
                                     )        
        self._highlightRules.AddRule(
                                     "preprocess",  # region, endregion, etc.
                                     HighlightRule(HighlightRegex.Preprocessor("preprocess", "#", " \W/", "|/[^/*]"), HighlightColor(Color.DarkBlue), None, None),
                                     None
                                     )        
        self._highlightRules.AddRule(
                                     "keyword", 
                                     HighlightRule(HighlightRegex.LanguageWords("keyword", self.Keywords), HighlightColor(Color.Blue), None, None), 
                                     None
                                     )
        self._highlightRules.AddRule(
                                     "class", 
                                     HighlightRule(HighlightRegex.LanguageWords("class", self.Classes), HighlightColor(Color.DarkCyan), None, None), 
                                     None
                                     )
        pass
