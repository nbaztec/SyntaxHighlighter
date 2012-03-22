using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;
using System.Text;
using System.Drawing;

namespace NX.SyntaxHighlighter.Omega
{
    /// <summary>
    /// Abstract Parent Class
    /// </summary>
    public abstract class SyntaxHighlighter : IHighlighter
    {
        #region Private Members
        //
        #endregion

        #region Protected Members
        protected HighlightRules _highlightRules;
        protected System.Windows.Forms.RichTextBox _backupRtf;
        protected string Keywords;
        protected string Commands;
        #endregion

        #region Properties
        public Color DefaultTextColor { get; set; }
        public Color DefaultTextBackColor { get; set; }
        public Font DefaultFont { get; set; }
        #endregion

        #region Interface Methods
        /// <summary>
        /// Sets the rules of highlighter
        /// </summary>
        /// <param name="highlightRules"></param>
        public void SetRules(HighlightRules highlightRules)
        {
            this._highlightRules = highlightRules;
        }

        /// <summary>
        /// Gets the rules of highlighter
        /// </summary>
        /// <returns>Current highlight rules</returns>
        public HighlightRules GetRules()
        {
            return this._highlightRules;
        }

        /// <summary>
        /// Initiates Highlighting
        /// </summary>
        /// <param name="inputText"></param>
        /// <returns>Output highlighted text</returns>
        public string Highlight(string inputText)
        {
            this._backupRtf.Clear();
            this._backupRtf.SelectionColor = this.DefaultTextColor;
            this._backupRtf.SelectionBackColor = this.DefaultTextBackColor;
            this._backupRtf.SelectionFont = this.DefaultFont;
            this._backupRtf.SelectedText = inputText;
            this.RecursiveHighlight(inputText, null, 0);
            return this._backupRtf.Rtf;
        }
        #endregion

        #region Abstract Methods
        /// <summary>
        /// Performs a recursive highlighting on the input text
        /// </summary>
        /// <param name="input">The matched token</param>
        /// <param name="group">Group to which the token belongs</param>
        /// <param name="index">Index from the original input string</param>
        protected abstract void RecursiveHighlight(string input, string group, int index);
        /// <summary>
        /// Sets the default rules of the highlighter
        /// </summary>
        protected abstract void SetDefaultRules();
        /// <summary>
        /// Sets the default keywords & commands for the highlighter
        /// </summary>
        protected abstract void SetDefaultKeywords();        
        #endregion

        #region Virtual Methods
        //
        #endregion

        #region Constructors

        /// <summary>
        /// Basic Constructor
        /// </summary>
        /// <param name="defaultRules">Option to set default rules or not</param>
        public SyntaxHighlighter(bool defaultRules = true)
        {
            this._highlightRules = new HighlightRules();
            this._backupRtf = new System.Windows.Forms.RichTextBox();
            this.DefaultTextColor = Color.Black;
            this.DefaultTextBackColor = Color.White;
            this.DefaultFont = new Font("Lucida Console", 10);
            if (defaultRules)
            {
                this.SetDefaultKeywords();
                this.SetDefaultRules();
            }
        }

        /// <summary>
        /// Basic Constructor
        /// </summary>
        /// <param name="defaultFont">Default font to be used</param>
        public SyntaxHighlighter(Font defaultFont) : this(true)
        {            
            this.DefaultFont = defaultFont;            
        }

        /// <summary>
        /// Custom Constructor
        /// </summary>
        /// <param name="highlightRules">Object of type HighlightRules</param>
        /// <param name="defaultFont">Default font to be used</param>
        public SyntaxHighlighter(HighlightRules highlightRules, Font defaultFont) : this(defaultFont)
        {
            this._highlightRules = highlightRules;            
        }

        /// <summary>
        /// Custom Constructor
        /// </summary>
        /// <param name="highlightRules">Object of type HighlightRules</param>
        public SyntaxHighlighter(HighlightRules highlightRules) : this(true)
        {
            this._highlightRules = highlightRules;            
        }

        /// <summary>
        /// Custom Constructor
        /// </summary>
        /// <param name="keywords">Array of keywords</param>
        /// <param name="commands">Array of commands</param>
        /// <param name="defaultFont">Default font to be used</param>
        public SyntaxHighlighter(string[] keywords, string[] commands, Font defaultFont) : this(false)
        {            
            if (keywords != null)
                this.Keywords = String.Join("|", keywords);                            
            if(commands != null)
                this.Commands = String.Join("|",commands);
            
            this.DefaultFont = defaultFont;
            this.SetDefaultRules();
        }

        /// <summary>
        /// Custom Constructor
        /// </summary>
        /// <param name="keywords">Array of keywords</param>
        /// <param name="commands">Array of commands</param>
        public SyntaxHighlighter(string[] keywords, string[] commands) : this(false)
        {
            if (keywords != null)
                this.Keywords = String.Join("|", keywords);
            if (commands != null)
                this.Commands = String.Join("|", commands);

            this.SetDefaultRules();
        }

        #endregion

        #region Methods
        /// <summary>
        /// Create a single regex string for selected groups
        /// </summary>
        /// <param name="groups">Specific groups to include. `null` indicates all groups</param>
        /// <returns>Generated regex string</returns>
        protected string GetRegexStringForGroups(string[] groups = null)
        {
            String regExStr = "";
            if (groups == null)
            {
                foreach (HighlightRule h in this._highlightRules.Rules)
                    if(h.RegexString != null)
                        regExStr += h.RegexString + "|";
            }
            else
            {
                foreach (string s in groups)
                    if (this._highlightRules[s].RegexString != null)
                        regExStr += this._highlightRules[s].RegexString + "|";
            }
            return regExStr.TrimEnd('|');
        }        
        #endregion
    }
}
