using System;
using System.Collections.Generic;
using System.Drawing;
using System.Text;
using System.Text.RegularExpressions;

namespace NX.SyntaxHighlighter.Omega
{
    public class HighlightRule
    {
        public enum ColorType { Foreground, Background }
        public enum EditType { Color, BackColor, Font, FontStyle, Regex, Dependencies }

        #region Highlight Controllers
        public bool ColorEnabled { get; set; }
        public bool BackColorEnabled { get; set; }
        public bool FontEnabled { get; set; }
        #endregion

        #region Private Members
        private Color _color;
        private Color _backColor;
        private Font _font;
        private String _regex;
        #endregion

        #region Properties
        public Color HighlightColor { get { return this._color; } }
        public Color HighlightBackColor { get { return this._backColor; } }
        public Font HighlightFont { get { return this._font; } }
        public String RegexString { get { return this._regex; } }
        #endregion

        #region Constructors
        public HighlightRule()
        {
            this._regex = null;
            this._color = Color.Blue;
            this._backColor = Color.Transparent;
            this._font = new Font("Calibri", 12, FontStyle.Regular);
            this.ColorEnabled = this.BackColorEnabled = this.FontEnabled = false;
        }

        public HighlightRule(string regex)
        {
            this._regex = regex;
            this._color = Color.Blue;
            this._backColor = Color.Transparent;
            this._font = new Font("Calibri", 12, FontStyle.Regular);
            this.ColorEnabled = this.BackColorEnabled = this.FontEnabled = false;
        }

        public HighlightRule(HighlightRule hr)
        {
            this._regex = hr._regex;
            this._color = hr._color;
            this._backColor = hr._backColor;
            this._font = hr._font;
            this.ColorEnabled = hr.ColorEnabled;
            this.BackColorEnabled = hr.BackColorEnabled;
            this.FontEnabled = hr.FontEnabled;
        }

        public HighlightRule(Color color, Color backColor, Font font)
        {
            this._regex = null;
            this._color = color;
            this._backColor = backColor;
            this._font = font;
            this.ColorEnabled = this.BackColorEnabled = this.FontEnabled = true;
        }

        public HighlightRule(String regex, Color color, Color backColor, Font font)
        {            
            this._regex = regex;
            this._color = color;
            this._backColor = backColor;
            this._font = font;
            this.ColorEnabled = this.BackColorEnabled = this.FontEnabled = true;
        }

        public HighlightRule(String regex, Color color, ColorType ct)
        {
            if (ct == ColorType.Foreground)
            {
                this._color = color;
                this._backColor = Color.Transparent;
                this.ColorEnabled = true;
                this.BackColorEnabled = this.FontEnabled = false;
            }
            else
            {
                this._color = Color.Transparent;
                this._backColor = color;
                this.BackColorEnabled = true;
                this.ColorEnabled = this.FontEnabled = false;
            }
            this._font = new Font("Calibri", 12, FontStyle.Regular);
            this._regex = regex;
        }

        public HighlightRule(Color color, ColorType ct)
        {
            if (ct == ColorType.Foreground)
            {
                this._color = color;
                this._backColor = Color.Transparent;
                this.ColorEnabled = true;
                this.BackColorEnabled = this.FontEnabled = false;
            }
            else
            {
                this._color = Color.Transparent;
                this._backColor = color;
                this.BackColorEnabled = true;
                this.ColorEnabled = this.FontEnabled = false;
            }
            this._font = new Font("Calibri", 12, FontStyle.Regular);
            this._regex = null;
        }

        public HighlightRule(String regex, Color color, Color backColor)
        {
            this._regex = regex;
            this._color = color;
            this._backColor = backColor;
            this._font = new Font("Calibri", 12, FontStyle.Regular);
            this.ColorEnabled = this.BackColorEnabled = true;
            this.FontEnabled = false;
        }

        public HighlightRule(String regex, Color color, Font font)
        {
            this._regex = regex;
            this._color = color;
            this._backColor = Color.Transparent;
            this._font = font;
            this.ColorEnabled = this.FontEnabled = true;
            this.BackColorEnabled = false;
        }

        public HighlightRule(String regex, Font font)
        {
            this._regex = regex;
            this._color = Color.Blue;
            this._backColor = Color.Transparent;
            this._font = font;
            this.ColorEnabled = this.BackColorEnabled = false;
            this.FontEnabled = true;
        }
        #endregion

        #region Methods
     
        public void ConstructObject(ref Color color, ref Color backColor, ref Font font)
        {
            if (this.ColorEnabled)
                color = this._color;
            if (this.BackColorEnabled)
                backColor = this._backColor;
            if (this.FontEnabled)
                font = this._font;
        }

        public HighlightRule ConstructObject(System.Windows.Forms.RichTextBox rtf)
        {
            Color color = this.ColorEnabled ? this._color : rtf.SelectionColor;
            Color backColor = this.BackColorEnabled ? this._backColor : rtf.SelectionBackColor;
            Font font = this.FontEnabled ? this._font : rtf.SelectionFont;
            return new HighlightRule(color, backColor, font);
        }

        public HighlightRule GetModifiedObject(EditType type, object newValue)
        {
            HighlightRule hr = new HighlightRule(this);
            switch(type)
            {
                case EditType.Color:                    
                    hr._color = (Color)newValue;
                    hr.ColorEnabled = true;
                    break;
                case EditType.BackColor:
                    hr._backColor = (Color)newValue;
                    hr.BackColorEnabled = true;
                    break;
                case EditType.Font:
                    hr._font = (Font)newValue;
                    hr.FontEnabled = true;
                    break;
                case EditType.FontStyle:
                    hr._font = new Font(this._font, (FontStyle)newValue);
                    hr.FontEnabled = true;
                    break;
                case EditType.Regex:
                    hr._regex = newValue as string;                    
                    break;
            }
            return hr;           
        }
        #endregion
    }
}
