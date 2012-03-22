'''
Created on Nov 8, 2011
@author: Nisheeth Barthwal
@contact: nbaztec@gmail.com
@copyright: Nisheeth Barthwal, 2011
@summary: This Module contains the Base classes for the NX - Syntax Highlighter. These are required by the subsequent highlighters. 

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

import re
from collections import OrderedDict
from NX.Enum import Color
from NX.Main import HtmlWriter, FontStyle
from NX.Main import GenericColor, GenericFont

# @note: Modify any generic regular expressions here 
class HighlightRegex(object):
    """
        @summary: Returns the generic regular expressions
        @note: Modify any generic regular expressions here 
    """
    @classmethod
    def RemoveDuplicates(cls, delim):
        s = ""
        for c in delim:
            if c not in s:
                s += c
        return s
    
    @classmethod    
    def Escape(cls, delim):
        """
            @summary: Escapes the reserved regex literals \^$.|?*+(){}. re.escape would've worked too.
        """
        s = ""
        for c in delim:
            if r'\^$.|?*+(){}'.find(c) >= 0:
                s += '\\'
            s += c
        return s
         
    @classmethod    
    def LanguageWords(cls, group, words):
        """
            @return: Regex for matching keywords, commands, etc. (Eg: for, while, return)
        """ 
        return r'(?P<' + group + r'>\b(?:' + words + r')\b)'
        
    @classmethod    
    def QuotedChar(cls, group, delim):
        """
            @return: Regex for matching single-length quoted characters (Eg: 'c')
        """
        delim = cls.Escape(delim) 
        return r'(?<!\\)(?P<' + group + r'>' + delim + r'(?:\\.|[^' +  cls.RemoveDuplicates(delim) + r'])' + delim + r')'
        
    @classmethod
    def QuotedString(cls, group, delim, special="", extra=""):
        """
            @return: Regex for matching quoted string (Eg: "My String")
        """
        delim = cls.Escape(delim) 
        return r'(?<!\\)(?P<' + group + r'>' + delim + r'(?:[^\\' + cls.RemoveDuplicates(delim) + special + r'\r\n]|\\.' + extra + r')*' +  delim + r')'
        
    @classmethod
    def MultiLineQuotedString(cls, group, delim, special="", extra=""):
        """
            @return: Regex for matching multiline quoted string Eg: "My Multi-line
                                                                     String"
        """
        delim = cls.Escape(delim) 
        return r'(?<!\\)(?P<' + group + r'>' + delim + r'(?:[^\\' + cls.RemoveDuplicates(delim) + special + r']|\\[\w\W]|\r\n' + extra + r')*' +  delim + r')'
        
    @classmethod
    def SingleLineComment(cls, group, delim):
        """
            @return: Regex for matching single-line comments (Eg: // Comment)
        """
        delim = cls.Escape(delim) 
        return r'(?P<' + group + r'>(?:(?<!\$)' + delim + r'.*))'           
        
    @classmethod
    def MultiLineComment(cls, group, delim_1, delim_2=None):
        """
            @param delim_1: Starting delimiter (Eg: /*)
            @param delim_2: Closing delimiter  (Eg: */)
            @return: Regex for matching multi-line comments Eg: /* 
                                                                    My Comment on a
                                                                    New Line 
                                                                */            
        """
        if delim_2 is None: 
            delim_2 = delim_1
        delim_1 = cls.Escape(delim_1)
        delim_2 = cls.Escape(delim_2)
         
        return r'(?P<' + group + r'>' + delim_1 + r'(?:.|[\r\n])*?' + delim_2 + r')'
        
    @classmethod
    def ReferencedVariable(cls, group, delim):
        """
            @return: Regex for matching referenced variables (Eg: $var)
        """
        delim = cls.Escape(delim) 
        return r'(?:(?<!\\)(?:(?:\\{2})*)|[^\\])(?P<' + group + r'>' + delim + r'[a-zA-z0-9@#$*?][\w\d]*)'  
    
    @classmethod
    def Preprocessor(cls, group, delim, special="", extra=""):
        """
            @param special: Chars to break the matching.
            @param extra: Chars to add to the matching.
            @return: Regex for matching preprocessor directives (Eg: #include <abcd.h>)            
        """
        delim = cls.Escape(delim) 
        return r'(?P<' + group + r'>^\s*' + delim + r'(?:[^\r\n' + special + r']|\\' + extra + r')*)'  
        
    
    @classmethod
    def SingleLineReferencedBlock(cls, group_begin, group_ref, delim_1, delim_2, special_chars=""):
        """            
            @param group_begin: Group name for the entire match. Used for recursive dependencies.
            @param group_ref:   Group name for the initial highlight part (Eg: ${myIndex of ${myIndex[3]}). Used for highlighting.
            @param delim_1: Starting delimiter (Eg: {)
            @param delim_2: Closing delimiter  (Eg: })
            @param special_chars: Any chars that should not be allowed in a single line reference block. Eg: a comment char (#, //)
            @return: Regex for matching referenced blocks. Example Bash-style ${ }, $( ), $(( )) 
        """
        delim_1 = cls.Escape(delim_1)
        delim_2_un = delim_2
        delim_2 = cls.Escape(delim_2)
        return r'(?:(?<!\\)(?:(?:\\{2})+)|[^\\])(?:(?P<' + group_begin + r'>(?P<' + group_ref + r'>\$' + delim_1 + r'\s*[A-Za-z0-9_]+)(?:[^' + cls.RemoveDuplicates(delim_2_un) + special_chars + r'])*(?P<' + group_ref + r'>' + delim_2 + r')))'
                
                
'''
    Highlighter Classes
    
    Classes included:    
    + HighlightColor          :    Empty extension of GenericColor.
    + HighlightFont           :    Empty extension of GenericFont.
    + HighlightRule           :    Class to maintain a single highlight rule.
    + EditType                :    Enum to specify the parameter of the HighlightRule object to edit.
    + HighlightRules          :    Class to maintain the various HighlightRule objects & their recursive dependencies on each other.
    + SyntaxHighlighter       :    Base class to highlight an input text. Currently uses HtmlWriter as the default/only writer.
'''

class HighlightColor(GenericColor):
    """
        @summary: Highlighter's Color Class.
        @note: No further functionality is provided. This class is extended just to specify the semantics.
    """
    def __init__(self, color):
        super(HighlightColor, self).__init__(color)

class HighlightFont(GenericFont):
    """
        @summary: Highlighter's Font Class.
        @note: No further functionality is provided. This class is extended just to specify the semantics.
    """
    def __init__(self, name, size, style):
        super(HighlightFont, self).__init__(name, size, style)        
        
class EditType(object):
    Color = 1; BackColor = 2; Font = 3; FontStyle = 4; Regex = 5; Dependencies = 6;
    
class HighlightRule(object):
    """
        @summary: Provides provision for specifying a single highlight rule.
    """
    def __init__(self, regex=None, forecolor=None, backcolor=None, font=None):
        """
            @param regex: str, The regex string.
            @param forecolor: HighlightColor, The foreground color to set for the match.
            @param backcolor: HighlightColor, The background color to set for the match.
            @param font: HighlightFont, The font to set for the match.
        """
        self.__regex = regex
        self.__color = forecolor
        self.__backcolor = backcolor
        self.__font = font        
            
    # Properties    
    @property
    def ForeColor(self): return self.__color;
    @ForeColor.setter
    def ForeColor(self, value): self.__color = value
    
    @property
    def BackColor(self): return self.__backcolor
    @BackColor.setter
    def BackColor(self, value): self.__backcolor = value
    
    @property
    def Font(self): return self.__font
    @Font.setter
    def Font(self, value): self.__font = value
    
    # @return: The actual regex string with multiple groups
    @property
    def RegexString(self): return self.GetActualRegex()
    # @return: The internal regex string with #ids apppended to all the groups
    @property
    def InternalRegexString(self): return self.__regex

    # Methods
    def GetModifiedRule(self, attribType, value, renameIndex=None):
        """
            @param attribType: EditType, The attribute to modify (color, backcolor, font, fontstyle or regex)
            @param value: FontStyle|str|HighlightColor|HighlightFont, The new value
            @param renameIndex: int, The count of the number of items already in index. Used to simulate multiple groups, which Python's `re` module doesn't support
            
            @summary: Returns the modified rule object. The object's regex is renamed base on the #id  
        """
        self.__renameCount = value
        hr = HighlightRule(self.__regex, self.__color, self.__backcolor, self.__font)
        if   (attribType == EditType.Color): hr.__color = value
        elif (attribType == EditType.BackColor): hr.__backcolor = value
        elif (attribType == EditType.Font): hr.__font = value
        elif (attribType == EditType.FontStyle): hr.__font = GenericFont(self.__font.FontName, self.__font.FontSize, value)
        elif (attribType == EditType.Regex): 
            hr.__regex = value
            if renameIndex is not None:
                self.RenameRegexGroup(renameIndex)
        return hr
    
    # @return: The new group name (appended by a unique #id)            
    def reSubHandler(self, matchObject):
        """
            @param matchObject: MatchObject, The match of the calling re method.
             
            @summary: Substitution Handler: Appends a unique positional #id to the regex group. The value to `self.__renameCount` is incremented to signify the latest #id 
        """           
        t = "%s_%02d" % (matchObject.group(0), self.__renameCount)            
        self.__renameCount = self.__renameCount + 1
        return t
        
    # @return: The new value for the counter. External calling object must update it in it's own counter.
    def RenameRegexGroup(self, value):
        """            
            @attention: The function is called externally to rename the groups.             
            @param value: int, The latest #id. This is specified externally and signifies the starting value to start naming the groups with.
            
            @summary: Generates an internal regex having unique group names. These are of the form:
                          OriginalName_dd    :where dd is a 2-width unique integer
                      Original group names can be recovered by slicing '_dd' through group[:-3] 
        """            
        self.__renameCount = value        
        if self.__regex is not None:
            self.__regex = re.sub(r'\(\?P<([^>]+)', self.reSubHandler, self.__regex)
        return self.__renameCount     
    
    # @return: The actual regex by removing all the #ids from the groups
    def GetActualRegex(self):                                            
        return re.sub(r'\(\?P<([^>]+)_\d+', r'(?P<\1', self.__regex) if self.__regex is not None else None         
        
    def __str__(self):
        return "{%s}  : %s, %s, %s" % (self.RegexString, self.ForeColor, self.BackColor, self.Font)

class HighlightRules(object):
    """
        @summary: Provides provision for specifying a list of rules & their recursive dependencies on other rules.
    """
    def __init__(self, rules=None, dependencies=None):
        """
            @param rules: dict(str: HighlightRule), A dictionary of `str: HighlightRule` pairs.
            @param dependencies: dict(str: list(str), A dictionary of dependencies having `str: list(str)` pairs.
        """
        self.__itemCount = 0    # Set initial __itemCount to 0. This is an autonumber for generating the unique #ids for named groups by calling HighlightRule.RenameRegexGroup(self.__itemCount)
        if rules is None:
            self.__highlightRules = OrderedDict()            
        else:
            self.__highlightRules = rules            
        if dependencies is None: 
            self.__highlightDependencies = dict()
        else:
            self.__highlightDependencies = dependencies            
    
    def __getitem__(self, key):         # [] get
        return self.__highlightRules[key]
    
    def __setitem__(self, key, value):  # [] set
        self.__highlightRules[key] = value
        
    # @return: int, Number of rules 
    @property       
    def Count(self): return len(self.__highlightRules);
    # @return: list(str), Keys
    @property       
    def Keys(self): return self.__highlightRules.keys();
    # @return: list(str), Rules
    @property       
    def Rules(self): return self.__highlightRules.values();
    # @return: list(str), Dependencies
    @property       
    def RecursiveDependencies(self): return self.__highlightDependencies;

    # @return: bool, Checks if a key is present
    def Has_Key(self, key): 
        return self.__highlightRules.has_key(key)
        
    def AddRule(self, key, rule, dependencies):
        """
            @param key: str, The key for both dict() for rules & dict() for dependencies.
            @param rule: HighlightRule, Required.
            @param dependencies: list(str), A list of recursive dependencies realised by the key names in this list. 
            
            @summary: Adds the rule & dependencies with the value of `key`
        """        
        if rule is None:  # @attention: rule should not be None. Required to avoid uneccesarry checks elsewhere.
            rule = HighlightRule()
            
        self.__itemCount = rule.RenameRegexGroup(self.__itemCount)  # Request to rename the group starting with self.__itemCount as the #id. 
                                                                    # @attention: The new value for self.__itemCount is returned & saved.
        self.__highlightRules[key] = rule
        if dependencies is not None:
            self.__highlightDependencies[key] = dependencies
    
    def SetRule(self, key, rule, dependencies):
        """            
            @param key: str, The key for both dict() for rules & dict() for dependencies.
            @param rule: HighlightRule, Required.
            @param dependencies: list(str), A list of recursive dependencies realised by the key names in this list.
            
            @summary: Sets the rule & dependencies to the value of `key`.
        """        
        self.AddRule(key, rule, dependencies)   # @note: All checks & modifications are automatically done in AddRule.
    
    def RemoveRule(self, key):
        """            
            @param key: str, The key specifying the rules & dependencies
            
            @summary: Removes the rules & dependencies specified by the key. Also removes the key from the dependency list of other rules. 
        """
        del self.__highlightRules[key]  # Remove from dict() of rules
        for k in self.__highlightDependencies.keys():   # Remove from dependency lists of other rules, if present
            if key in self.__highlightDependencies[k]:
                self.__highlightDependencies[k].remove(key)                                
        if self.__highlightDependencies.has_key(key): del self.__highlightDependencies[key] # Remove from dict() of dependencies if present
    
    def EditRules(self, keys_list, updates_list):     # keys = list(), updates = dict() [ EditType : object ]
        """
            @param keys: A list of keys to perform updates on. Multiple updates require multiple entries in this list.
            @param updates: a dict(EditType, FontStyle|str|HighlightColor|HighlightFont) item
            
            @summary: Performs modifications on the rules specified by the entry in keys.            
        """
        index = 0
        for keys in keys_list:
            for key in keys:                
                updates = updates_list[index]                
                for utype in updates.keys():
                    newValue = updates[utype]
                    if (utype == EditType.Dependencies):    # Edit Dependencies
                        if (newValue is None):
                            if self.__highlightDependencies.has_key(key):   # If new value is None                     
                                del self.__highlightDependencies[key]       # Delete entry from dict()
                        else:
                            self.__highlightDependencies[key] = newValue    # Or, Assign new the new value                    
                    else:   # Assign new rule & increment the #id counter
                        self.__highlightRules[key] = self.__highlightRules[key].GetModifiedRule(utype, newValue, self.__itemCount)
                        if utype == EditType.Regex:                            
                            self.__itemCount = self.__highlightRules[key].__renameCount
                pass
            index += 1
        pass
    
    # Generators
    def item_rules(self):
        """
            @summary: Get a tuple pair of the form: HighlightRule, list(sting).
        """
        for k in self.__highlightRules.keys():            
            yield self.__highlightRules[k], self.__highlightDependencies[k] if self.__highlightDependencies.has_key(k) else None
        pass
            
    def item_highlights(self):
        """
            @summary: Get the iteration for highligh rules.
        """
        for k in self.__highlightRules.keys():
            yield self.__highlightRules[k]
            
    def item_dependencies(self):
        """
            @summary: Get the iteration for dependencies.
        """
        for k in self.__highlightDependencies.keys():
            yield self.__highlightDependencies[k]
    
    def __str__(self):
        ret = list()    # Prepare a list of all rules
        for k in self.__highlightRules.keys():
            ret.append("%-5s -> : [ %s ] [%s]" % (k,self.__highlightRules[k],self.__highlightDependencies[k] if self.__highlightDependencies.has_key(k) else None))  
        return "\n".join(ret)

class SyntaxHighlighter(object):
    """
        @note: Extend this class for all the generic highlighters.        
        @requires: A Writer object (Currently using HtmlWriter)
        @attention: Currently only HtmlWriter is supported.
        
        @summary: Provides the functionality for Syntax Highlighting.
    """
    
    from datetime import datetime
    # Attributes
    _versionMax = 1
    _versionMin = 5
    _codename = "Omega"
    _author = "Nisheeth Barthwal"
    _lastModified = datetime(2011, 11, 16, 18, 37)
        
    # Properties
        
    @property
    def VersionInfo(self): return "NX - Syntax Highlighter version %s.%s (%s) , Copyright %s" % (self._versionMax, self._versionMin, self._codename, self._author)
    @property
    def ClassInfo(self): return "NX - Syntax Highlighter version %s.%s, Copyright %s\nLast Modified: %s" % (self._versionMax, self._versionMin, self._author, self._lastModified.strftime("%a, %d %B %Y, %H:%M Hours"))
    
    @property       # HighlightColor
    def DefaultTextColor(self): return self.__defaultTextColor
    @DefaultTextColor.setter
    def DefaultTextColor(self, value): self.__defaultTextColor = value
    
    @property       # HighlightColor
    def DefaultBackColor(self): return self.__defaultBackColor
    @DefaultBackColor.setter
    def DefaultBackColor(self, value): self.__defaultBackColor = value
    
    @property       # HighlightFont
    def DefaultFont(self): return self.__defaultFont
    @DefaultFont.setter
    def DefaultFont(self, value): self.__defaultFont = value
    
    @property       # Boolean
    def MatchCaseSensitive(self): return self.__matchCaseSensitive
    @MatchCaseSensitive.setter
    def MatchCaseSensitive(self, value): self.__matchCaseSensitive = value
    
    @property
    def RuleNames(self): return self._highlightRules.Keys
    @property
    def Rules(self): return self._highlightRules
    
    #Init
    def __init__(self, highlightRules, defaultForecolor, defaultBackcolor, defaultFont, keywords, commands, defaultWriter=None):
        """
            @param highlightRules: HighlightRules, An existing HighlightRules object.
            @param defaultForecolor: HighlightColor, The default foreground color to use.
            @param defaultBackcolor: HighlightColor, The default background color to use.
            @param defaultFont: HighlightFont, The default font color to use.
            @param keywords: list(str), The default keyword list to use. If omitted can be added by overriding SetLanguageWords() method.
            @param commands: list(str), The default command list to use. If omitted can be added by overriding SetLanguageWords() method.
            @param defaultWriter: Writer, The default writer to use for formatting.
            @attention: Currently only HtmlWriter is supported.
            
            @summary: Initialize the SyntaxHighlighter
        """        
        
        # Attributes
        self.MatchCaseSensitive = True  # Set regex matching as case-sensitive.
                        
        self.DefaultTextColor = HighlightColor(Color.Black) if defaultForecolor is None else defaultForecolor
        self.DefaultBackColor = HighlightColor(Color.White) if defaultBackcolor is None else defaultBackcolor
        self.DefaultFont      = HighlightFont("Lucida Console", 12, FontStyle.Regular) if defaultFont is None else defaultFont
        
        # Call to set the language words (keywords, commands, etc.).
        # @note: Override this methods to initialize keywords, commands, functions, etc.        
        self.SetLanguageWords()
        
        # Override default keywords/commands if any.
        if keywords is not None:
            self.Keywords = "|".join(keywords)
        if commands is not None:
            self.Commands = "|".join(commands)
        
        # Attach the highlighting rules.
        # @attention: Override SetDefaultRules() in your Highlighters to add rules to `self._highlightRules`. See Basic/Bash Highlighter for example. 
        if highlightRules is None:
            self._highlightRules = HighlightRules(None, None)                   
            self.SetDefaultRules()
        else:
            self._highlightRules = highlightRules
            
        # Attach the default writer.
        if defaultWriter is None:   
            defaultWriter = HtmlWriter
        self._outputWriter = defaultWriter(self.DefaultTextColor, self.DefaultBackColor, self.DefaultFont)
        
    # Methods 
    def SetRules(self, highlightRules):
        """
            @param highlightRules: HighlightRules, Attaches the highlight rules to the highlighter.
            
            @summary: Attaches the highlight rules to the highlighter.
        """
        self._highlightRules = highlightRules
    
    def GetRules(self):     # Gets the highligting rules
        return self._highlightRules
    
    def Highlight(self, inputText, formatDocument=None):
        '''
            @param inputText: str, The text to highlight
            @return: Formatted text.
            
            @attention: This function is generally used to interact with the user.            
            @summary: The function highlights the input text by the `_highlightRules` & prints the output defined by `_outputWriter`. 
        '''
        # Empty the writer & assign text
        self._outputWriter.Clear()      
        self._outputWriter.Text = inputText
        # Highlight using the rules
        self.RecursiveHighlight(inputText, None, 0)     # (Text to highlight, Initial group, Starting index).
        if formatDocument is None:
            return self._outputWriter.FormattedText         # Return formatted text.
        else:
            return self._outputWriter.FormattedHtml(formatDocument + " | NX - Syntax Highlighter","<!--%s-->" % self.VersionInfo)   # Return formatted document
    
    # Virtual Methods
    
    # @attention: Override these methods in all highlighters, espc. the `SetDefaultRules` method.
    def SetDefaultRules(self): pass     # Called when setting the default keywords, commands, etc.
    def SetLanguageWords(self): pass    # Called when setting the default rules for highlighting.
    
    #def OverrideHighlightFormat(self, group, highlightObject): return highlightObject
    # @note: Attach this function if the user wants to edit simply the color or font of a highlight  
    OverrideHighlightFormat = None
    
    
    # Virtual Methods
    # @attention: Do not override this method unless you come up with a new algorithm for recursive highlighting. If you do contact the author & contribute. Thank you.
    def RecursiveHighlight(self, inputText, group, index):
        '''
        @param inputText: str, The text to highlight. The same text must exist in the Writer prior to calling this function.
        @param group: str, The group under which to perform all the highlighting. Required for recursive highlight using dependencies. Root group is always `None`.
        @param index: int, Current index of the highlight engine. All formatting is done relative to this index.  
            
        @attention: Withing this function [:-3] is used to slice the groups back to their original unmodified form (as they are registered). Internally the groups has an additional "_DD" appended (D is a digit).
        @summary: Recursively highlights the text in the writer based on the recursive dependencies.        
        ''' 
        
        # Set regex flags        
        re_flags = re.M
        if not self.MatchCaseSensitive:
            re_flags |= re.I
        
        matches = []
        
        if group is None:   # Root group
            matches = re.finditer(self.GetRegexStringForGroups(), inputText, re_flags)
        elif self._highlightRules.RecursiveDependencies.has_key(group):     # Highlight recursively using the dependencies
            matches = re.finditer(self.GetRegexStringForGroups(self._highlightRules.RecursiveDependencies[group]), inputText, re_flags)        
        
        # Highlight each match
        for m in matches:
            
            # Get the groups which matched successfully in the regex.            
            groupKeys = list()            
            m_groups = m.groupdict()                    
            for key in m_groups:    # Group must be present in the `_highlightRules` for higlighting. Even dependecy-only rules are registered in `_highlightRules`.
                if m_groups[key] is not None and self._highlightRules.Has_Key(key[:-3]):    # Slice the group because groups have #ids internally. 
                    groupKeys.append(key)                    
                
            # Highlight the groups found
            for groupKey in groupKeys:                              
                self._outputWriter.Select(m.start(groupKey) + index, m.end(groupKey) - m.start(groupKey))   # Select in the Writer.                
                ho = self._highlightRules[groupKey[:-3]]    # Get the rule's highlighting rule.
                if self.OverrideHighlightFormat is not None:
                    self.OverrideHighlightFormat(groupKey[:-3], ho)
                self._outputWriter.SelectionFormat(ho.ForeColor, ho.BackColor, ho.Font)     # Highlight the text in the writer                       
                if self._highlightRules.RecursiveDependencies.has_key(groupKey[:-3]):       # Check for any groups that can be contained in this group (dependencies)
                    self.RecursiveHighlight(m.group(groupKey), groupKey[:-3], m.start(groupKey) + index)    # (Text captured by the group, Group's actual name, Current index in text)
    
    # Helper Protected Methods        
    def GetRegexStringForGroups(self, groups = None):
        """
            @param groups: str, The groups to get the regex's for. `None` means get the regex string for all groups
            @return: str, The final regex matcher string.
            
            @summary: The function ORs all the regexes for the groups specified in the arg & returns them.
        """
        regexStr = ""          
        if groups is None:
            #for t in self._highlightRules.Keys: print t
            for h in self._highlightRules.Rules:                
                if h.InternalRegexString is not None:
                    regexStr += h.InternalRegexString + "|"                    
        else:            
            for s in groups:
                if self._highlightRules[s].InternalRegexString is not None:
                    regexStr += self._highlightRules[s].InternalRegexString + "|"            
        return regexStr.rstrip("|")
                                        
    def __str__(self):
        return str(self._highlightRules)