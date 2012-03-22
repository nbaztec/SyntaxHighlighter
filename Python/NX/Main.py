'''
Created on Nov 7, 2011
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

'''
    Fonts
    
    Classes included:
    + FontStyle      :    Enum for the various font styles.
    + NXFont         :    ABC for Fonts.
    + GenericFont    :    Concrete class of NXFont. Recommended for extending.
'''           
class FontStyle(object):
    '''
        @summary: Defines the various font styles
    '''
    Empty = 0; Regular = 1; Bold = 2; Italic = 4; Underline = 8;
    
class NXFont(object):   
    '''
        @summary: Abstract Class for fonts
    '''
    def __init__(self):
        raise NotImplementedError()
    
    # @return: bool
    def IsRegular(self):
        return True if self._style & FontStyle.Regular else False;
    
    # @return: bool
    def IsBold(self):
        return True if self._style & FontStyle.Bold else False;
    
    # @return: bool
    def IsItalic(self):
        return True if self._style & FontStyle.Italic else False;
    
    # @return: bool
    def IsUnderline(self):
        return True if self._style & FontStyle.Underline else False;

    def __str__(self):
        t = list();
        if self.IsRegular():
            t.append("Regular");
        if self.IsBold():
            t.append("Bold")
        if self.IsItalic(): 
            t.append("Italic")
        if self.IsUnderline():           
            t.append("Underline")
         
        return "%s %d [%s]" % (self._fontName, self._size, ','.join(t))
   
class GenericFont(NXFont):
    '''
        @summary: Concrete (Generic) Font Class.
    '''
    def __init__(self, name, size, style):
        '''
            @param name: str, Font-family name.
            @param size: int, Font size.
            @param style: FontStyle, The style of font. Multiple styles should be ORed. 
        '''
        self._fontName = name
        self._size = size
        self._style = style
    
    # @return: string
    @property
    def FontName(self):
        return self._fontName;
    @FontName.setter
    def FontName(self, value):
        self._fontName = value
        
    #@return: int
    @property
    def FontSize(self):
        return self._size;
    @FontSize.setter
    def FontSize(self, value):
        self._size = value

'''
    Colors
    
    Classes included:    
    + NXColor         :    ABC for Color.
    + GenericColor    :    Concrete class of NXColor. Recommended for extending.
'''
        
class NXColor(object):
    '''
        @summary: Abstract color class.
    '''
    def __init__(self):
        raise NotImplementedError()
        
    def SetColorString(self, c):
        '''
            @param c: str,  Hex color string. Exmple "D355E6"
            @summary: Sets color value from hex string.
        '''
        self._rgb = list()           
        self._color = c;
        for i in range(0,3):
            self._rgb.append(int(c[(i*2):(i*2)+2],16));
    
    def SetColorValue(self, v):
        '''
            @param c: int,  Color's integer value.
            
            @summary: Sets color from an integer value.
        '''        
        self.SetColorString("%X" % v);
    
    # Properties
    @property
    def Red(self): return self._rgb[0]
    
    @property
    def Green(self): return self._rgb[1]
    
    @property
    def Blue(self): return self._rgb[2]
    
    #@return: string, Color's hex string
    @property
    def Color(self): return self._color;    
    @Color.setter
    def Color(self, value): self.SetColorString(value)
    
    #@return: int, Color's int value
    @property
    def RGB(self): return (self._rgb[0] + self._rgb[1] + self._rgb[2])
    @RGB.setter 
    def RGB(self,value): self.SetColorValue(value)
        
    def __str__(self):            
        return  "%s [%d: %03d %03d %03d]" % (self._color, self._rgb[0]+self._rgb[1]+self._rgb[2], self._rgb[0], self._rgb[1], self._rgb[2])
        
class GenericColor (NXColor):    
    '''
        @summary: Basic color class.
    '''
    def __init__(self, c, v=None):
        '''
            @param c: Color's hex string. High priority is both args are supplied.
            @param v: Color's integer value.  
            
            @summary: Sets the color value based on either the hex string or the RGB value.
        '''
        if c is not None: self.SetColorString(c)
        elif v is not None: self.SetColorValue(v)        

'''
    Writer Classes
    
    Classes included:    
    + NXWriter         :    ABC for Writer.
    + GenericWriter    :    Concrete class of NXWriter. Recommended for extending.
    + HtmlWriter       :    Extended class of NXWriter. Writes HTML formatting for the highlighter.
    
    @todo: Implement RtfWriter and PdfWriter 
'''
                                      
class NXWriter(object):
    '''
        @attention: This is an top-most abstract class. For simple inherting extend GenericWriter.
        @attention: Format-Map has the following ordering:
                    Format-Map[ #Index: Format-Map-For-Index[ Color: Value, BackColor: Value, Font: Value, FontSize: Value, Bold: Value, ... ], ... ]
                    
        @summary: Abstract class for writing.        
    '''
    class Range(object):   
        '''
            @summary: Internal class used for selections.
        '''     
        def __init__(self, index, length):
            '''
                @param index: int, Starting index.
                @param length: int, Selection length.                
            '''
            self.Index = index;
            self.Length = length;
        def __str__(self):
            return "[%d, %d]" % (self.Index, self.Length)
    
    def __init__(self):
        raise NotImplementedError()
    
    # Properties    
    
    # @return: str
    @property
    def Text(self): return self._text
    
    @Text.setter
    def Text(self, value): 
        self._text = value
        # Add initial format
        self._formatMap = dict()
        self.AddFormat(self._defaultColor.Color, self._defaultBackColor.Color, self._defaultFont.FontName, self._defaultFont.FontSize, self._defaultFont.IsRegular(), self._defaultFont.IsBold(), self._defaultFont.IsItalic(), self._defaultFont.IsUnderline())    # Add initial root format
        
    # @return: str
    @property
    def FormattedText(self): return self.GetFormattedText();
    
    def FormattedHtml(self, title="Output | NX Syntax Highlighter", header="", footer=""):
        return "<html><head><title>%s</title><body bgcolor='#%s'>%s%s%s</body></html>" % (title, self._defaultBackColor.Color, header, self.FormattedText, footer)                         
        
    # Methods
    def Select(self, index, length):        
        if index >= 0 and length >= 0 and (index + length) <= len(self._text):  # Check for valid selection boundary
            self._selection.Index = index
            self._selection.Length = length
        else:
            if self._text is None:
                raise ValueError("Value of text is None")
            else:            
                raise IndexError("Selection should be between 0 and %d" % len(self._text))
        
    # Abstract Methods
    def GetFormattedText(self):
        raise NotImplementedError()
    def AddFormat(self, forecolor, backcolor, font, size, regular, bold, italic, underline):
        raise NotImplementedError()
    
    def Clear(self):
        self._text = "";
        
    def __str__(self):
        return "%s: , (Forecolor:  %s, Backcolor: %s, Font: %s)" % (self.__class__.__name__, self._defaultColor, self._defaultBackColor, self._defaultFont)    
       
class GenericWriter(NXWriter):
    '''
        @note: Extend this class for other writers
        @attention: Override AddFormat(self, forecolor, backcolor, font, size, regular, bold, italic, underline) & GetFormattedText(self) methods
        
        @summary: Generic writer to perform basic output operations.
    '''
    def __init__(self, color, backcolor, font):      
        '''
            @param color: GenericColor, The foreground color.
            @param backcolor: GenericColor, The background color.
            @param font: GenericFont, The font.             
        '''              
        self._selection = self.Range(-1,0)   # Cannot use Select(int, int). Index -1 is required for initial header 
        self._defaultColor = color;
        self._defaultBackColor = backcolor
        self._defaultFont = font      
        self._defaultSize = font.FontSize
        self.Text = None                # Initialize format map with initial header
    
    # Properties
    
    # @return: GenericColor
    @property
    def DefaultColor(self): return self._defaultColor;
    @property
    def DefaultBackColor(self): return self._defaultBackColor;
    # @return: GenericFont
    @property
    def DefaultFont(self): return self._defaultFont;
    # @return: str
    @property
    def DefaultFontName(self): return self._defaultFont.FontName;
    # @return: int
    @property
    def DefaultFontSize(self): return self._defaultSize;
    # @return: GenericColor
    @property
    def SelectionColor(self): return self.GetSelectionColor();  # Override `GetSelectionColor()` based on the Writer. 
    
    @SelectionColor.setter
    def SelectionColor(self, value):
        self.SetSelectionColor(value)
        
    @property
    def SelectionBackColor(self): return self.GetSelectionBackColor();  # Override `GetSelectionBackColor()` based on the Writer.
    
    @SelectionBackColor.setter
    def SelectionBackColor(self, value):
        self.SetSelectionBackColor(value)
    
    # @return: GenericFont            
    @property
    def SelectionFont(self): return self.GetSelectionFont();  # Override `GetSelectionFont()` based on the Writer.
        
    @SelectionFont.setter   
    def SelectionFont(self, value):        
        self.SetSelectionFont(value)
        
    # Methods
    def SetSelectionColor(self, color):   
        '''
            @param color: GenericColor, The selection's foreground color. 
        '''     
        if color is not None:
            self.AddFormat(color.Color, None, None, 0, False, False, False, False)
    
    def SetSelectionBackColor(self, color):
        '''
            @param color: GenericColor, The selection's background color.
        '''
        if color is not None:
            self.AddFormat(None, color.Color, None, 0, False, False, False, False)
             
    def SetSelectionFont(self, font):
        '''
            @param font: GenericFont, The selection's font.
        '''
        if font is not None:
            self.AddFormat(None, None, font.FontName, font.FontSize, font.IsRegular(), font.IsBold(), font.IsItalic(), font.IsUnderline())
        
    def SelectionFormat(self, forecolor, backcolor, font):        
        '''
            @param forecolor: GenericColor, The selection's foreground color.         
            @param backcolor: GenericColor, The selection's background color.        
            @param font: GenericFont, The selection's font.
            
            @summary: Formats the text according to the format specified in the args. 
        '''
        fc = forecolor.Color if forecolor is not None else None
        bc = backcolor.Color if backcolor is not None else None                                  
        
        # Add only is atleast one attribute is not None
        if font is not None:
            self.AddFormat(fc, bc, font.FontName, font.FontSize, font.IsRegular(), font.IsBold(), font.IsItalic(), font.IsUnderline())            
        elif fc is not None or bc is not None:
            self.AddFormat(fc, bc, None, 0, False, False, False, False)
            
    # Virtual Methods
    def GetFormattedText(self):
        pass
    
    def AddFormat(self, forecolor, backcolor, font, size, regular, bold, italic, underline):
        pass

class HtmlWriter(GenericWriter):
    '''
        @attention: Format-Map has the following ordering:
                    Format-Map[ 
                        #Index: [ "end": "indices separated by |", "color:": #Value, "background-color:": #Value, "font-family:": 'Value', "font-size:": Value+'px', "font-weight:": normal|bold, "font-style:": normal|italic, "text-decoration:": none|underline ], 
                        ... ]
                    The number of '|' in "end" signifies the number of distinct closing tags
        @note: Class used to write actual format by overriding AddFormat() & GetFormattedText() methods                        
        
        @summary: Provides functionality to write a formatted HTML file.
    '''
    def __init__(self, color, backcolor, font):
        '''
            @param color: GenericColor, The selection's foreground color.         
            @param backcolor: GenericColor, The selection's background color.        
            @param font: GenericFont, The selection's font.
        '''
        super(HtmlWriter, self).__init__(color, backcolor, font)
    
    # Methods    
    def AddFormat(self, forecolor, backcolor, font, size, regular, bold, italic, underline):
        '''
            @param forecolor: str, The selection's foreground color string.         
            @param backcolor: str, The selection's background color string.        
            @param font: str, The selection's font name.
            @param size: int, The selection's font size.
            @param regular: bool, If the selection should be regular.
            @param bold: bool, If the selection should be bold.
            @param italic: bool, If the selection should be italic.
            @param underline: bool, If the selection should be underlined.  
            
            @summary: Determines how the format is added to the format-map. This is read by the `GetFormattedText` function to produce the actual output.
        '''
        # Assign the selection for easy manipulation
        index = self._selection.Index        
        length = self._selection.Length
                
        # Insert End of tag
        if length > 0:
            strIndex = str(index)
            if self._formatMap.has_key(index + length):             # If mapping already exists
                if self._formatMap[index + length].has_key("end"):  # If end tag is already specified
                    s = self._formatMap[index + length]["end"]
                    if s.find(strIndex+"|") < 0:                    # Add another tag only if the requesting index is different ( For overlapping highlights ) 
                        self._formatMap[index + length]["end"] += strIndex + "|"    # Add with delimiter
                else:
                    self._formatMap[index + length]["end"] = strIndex + "|"
            else:
                self._formatMap[index + length] = dict()
                self._formatMap[index + length]["end"] = strIndex + "|"        
        
        # Beginnning of tag
        if not self._formatMap.has_key(index):
            self._formatMap[index] = dict()
            
        t = self._formatMap[index]  # Get the mapping for the index
        
        if forecolor is not None:                
            t["color:"] = "#" + forecolor
        if backcolor is not None:                
            t["background-color:"] = "#" + backcolor
        if font is not None:                
            t["font-family:"] = "'%s'" % font
        if size > 0:
            t["font-size:"] = "%dpx" % size                
        if bold is True:
            t["font-weight:"] = "bold"
        elif regular is True:
            t["font-weight:"] = "normal"
            
        if italic is True:
            t["font-style:"] = "italic"
        elif regular is True:
            t["font-style:"] = "normal"   
            
        if underline is True:
            t["text-decoration:"] = "underline"
        elif regular is True:
            t["text-decoration:"] = "none"      
        
    def GetFormatStack(self):
        '''
            @summary: Returns the format stack for the selection till the selected index.
        '''
        stack = list()                
        sortedKeys = sorted(self._formatMap.keys())     # Sort keys prior to searching for the last formatting        
        for k in sortedKeys:
            if k > self._selection.Index:
                break  
            if self._formatMap[k].has_key("end"):                
                for unused_j in range(1, len(self._formatMap[k]["end"].split("|"))):
                    if len(stack) == 0: 
                        break
                    else:
                        stack.pop()
                if len(self._formatMap[k]) > 1:     # If any formatting is present. (If it's not just a closing tag), then append.
                    stack.append(k)
            else:
                stack.append(k)            
        return stack
    
        
    def ParseFormatting(self, formatDict):
        '''
            @summary: Returns a format type object with wrapper classes from a formatMap entry
        '''                
        fmt = dict()
        fs = FontStyle.Empty
        fmt['Foreground'] = GenericColor(formatDict["color:"][1:])   # Slice the pound character from the color (#FF00FF)
        fmt['Background'] = GenericColor(formatDict["background-color:"][1:])   # Slice the pound character from the color (#FF00FF)
        if formatDict["font-weight:"] == "bold" : fs |= FontStyle.Bold
        if formatDict["font-style:"] == "italic" : fs |= FontStyle.Italic
        if formatDict["text-decoration:"] == "underline": fs |= FontStyle.Underline
        if fs == FontStyle.Empty: fs |= FontStyle.Regular                    
        fmt['Font'] = GenericFont(formatDict["font-family:"].strip("'"), int(formatDict["font-size:"].rstrip("px")), fs)
        
        return fmt
    
    def GetFormat(self):
        '''
            @return: A dictionary having the format of the selected item.
            @summary: Returns the format for the selection by recursing till the parent root.
        '''        
        stack = self.GetFormatStack()
        fmtDict= {'color:' : None, 'background-color:' : None, 'font-family:' : None, 'font-size:' : None, 'font-weight:' : None, 'font-style:' : None, 'text-decoration:' : None, 'end': ''}
        max_items = len(fmtDict)
        count = 1   # To compensate for the extra `end` key. `end` is not required for formatting, but only for the closing tag.
        #print self._formatMap
        while len(stack) > 0:   # Pop indices until all the entries have values. The top level node has all the attributes defined.
            i = stack.pop()            
            for k,v in self._formatMap[i].items():
                if fmtDict[k] is None:      # If the list item is empty, then add the value to list and increment the counter
                    fmtDict[k] = v                    
                    count += 1
                if count == max_items:      # If all items have values, then break.
                    break            
        del fmtDict['end'] # Remove the extra `end` key.
        return self.ParseFormatting(fmtDict)
                            
    def GetFormattedText(self):
        '''
            @summary: Formats the text & returns the formatted text
        '''
        fmt = ""
        length = len(self.Text)
        for i in range(-1, length+1):   # -1 & length+1 are due to the format map. Initial format is stored at key: -1 & Final closing tag(if any) is at key: len(text)+1  
            if self._formatMap.has_key(i):
                s = ""                
                for k,v in self._formatMap[i].items():  # Add format of corresponding CSS attribute
                    if k == "end":                        
                        for unused_j in range(1, len(v.split("|"))):  # Add closing tag n-times determined by the occurences of the delimiter
                            fmt = fmt + "</span>"
                    else:
                        s = s + k + v + ";"
                if s != "":     # Add format if the attribute is not empty (Can be empty in case of "end"-only value) 
                    fmt += '<span style="' + s + '">'
                                                
            if i != -1 and i != length:     # Append valid HTML text if iterator is within text's length range
                fmt += self.TranslateChar(self.Text[i])        
        fmt += "</span>"    # Final closing tag of the header. Required because it is never added while formatting.
        return fmt
    
    def TranslateChar(self, c):
        '''
            @param c: str, The character to translate.
             
            @summary: Translates the input char to another char. Used to put HTML equivalents 
        '''
        if   c in ('\n'): return "<br />"
        elif c in ('\r'): return ""
        elif c in ('\t'): return "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        elif c in ('>'): return "&gt;"
        elif c in ('<'): return "&lt;"
        elif c in (' '): return "&nbsp;"
        else: return c
        
    # Overridden Methods
    
    def GetSelectionColor(self):
        return self.GetFormat()['Foreground']
        
    def GetSelectionBackColor(self):
        return self.GetFormat()['Background']
        
    def GetSelectionFont(self):        
        return self.GetFormat()['Font']
                