using System;
using System.Collections.Generic;
using System.Drawing;
using System.Text;
using System.Text.RegularExpressions;

namespace NX.SyntaxHighlighter.Omega
{
    public class BasicHighlighter : SyntaxHighlighter
    {
        #region Required Constructors

        /// <summary>
        /// Basic Constructor
        /// </summary>
        public BasicHighlighter() 
            : base()
        {              
        }

        public BasicHighlighter(Font defaultFont) : base(defaultFont)
        {                        
        }
        
        /// <summary>
        /// Constructor specifies custom keywords, commands & default font to use
        /// </summary>
        /// <param name="keywords">Array of keywords</param>
        /// <param name="commands">Array of commands</param>
        /// <param name="defaultFont">Custom Font object</param>
        public BasicHighlighter(string[] keywords, string[] commands, Font defaultFont)
            : base(keywords, commands, defaultFont)
        {                        
        }

        /// <summary>
        /// Constructor specifies custom keywords and commands to use
        /// </summary>
        /// <param name="keywords">Array of keywords</param>
        /// <param name="commands">Array of commands</param>
        public BasicHighlighter(string[] keywords, string[] commands)
            : base(keywords, commands)
        {
        }

        /// <summary>
        /// Constructor specifies custom highlight rules & default font to use
        /// </summary>
        /// <param name="highlightRules">HighlightRules object which specifies the highlighting rules to apply</param>
        /// <param name="defaultFont">Custom Font object</param>
        public BasicHighlighter(HighlightRules highlightRules, Font defaultFont) 
            : base(highlightRules, defaultFont)
        {            
        }

        #endregion

        #region Overridden Abstract Methods
        /// <summary>
        /// Sets the default rules of the highlighter
        /// </summary>
        protected override void SetDefaultRules()
        {
            this._highlightRules.AddRule("dquote", new HighlightRule("(?<!\\\\)(?<dquote>\"(?:[^\\\\\"\r\n]|\\\\.)*\")", Color.FromArgb(0xE60000), HighlightRule.ColorType.Foreground));
            this._highlightRules.AddRule("char", new HighlightRule("(?<!\\\\)(?<char>'(?:\\\\'|[^'])')", Color.Fuchsia, HighlightRule.ColorType.Foreground));
            this._highlightRules.AddRule("comment", new HighlightRule("(?<comment>(?:(?<!\\$)//.*))", Color.Green, new Font(this.DefaultFont, FontStyle.Italic)));            
            this._highlightRules.AddRule("keyword", new HighlightRule("(?<keyword>\\b[^\\$]?(" + this.Keywords + ")\\b)", Color.Blue, new Font(this.DefaultFont, FontStyle.Bold)));
            this._highlightRules.AddRule("command", new HighlightRule("(?<command>\\b[^\\$]?(" + this.Commands + ")\\b)", Color.Chocolate, new Font(this.DefaultFont, FontStyle.Regular)));                        
        }

        /// <summary>
        /// Sets the default keywords & commands for the highlighter
        /// </summary>
        protected override void SetDefaultKeywords()
        {
            this.Keywords = "if|else|for|while";
            this.Commands = "echo|exit";
        }

        /// <summary>
        /// Performs a recursive highlighting on the input text
        /// </summary>
        /// <param name="input">The matched token</param>
        /// <param name="group">Group to which the token belongs</param>
        /// <param name="index">Index from the original input string</param>
        protected override void RecursiveHighlight(string input, string group, int index)
        {
            MatchCollection matches = null;
            /*
             * Match for a pattern
             * A null `group` signifies first entry into a recursive match
             */ 
            if (group == null)
                matches = Regex.Matches(input, this.GetRegexStringForGroups(), RegexOptions.Multiline);
            else if( this._highlightRules.RecursiveDependencies.ContainsKey(group) )
                 matches = Regex.Matches(input, this.GetRegexStringForGroups(this._highlightRules.RecursiveDependencies[group]), RegexOptions.Multiline);
            /*
             * Highlight all matches
             */
            foreach (Match m in matches)
            {
                // Find the group of the match
                String groupKey = "";
                foreach (string key in this._highlightRules.Keys)
                    if (m.Groups[key].Success)
                    {
                        groupKey = key;
                        break;
                    }

                // Highlight using the group's rule
                this._backupRtf.Select(m.Groups[groupKey].Index + index, m.Groups[groupKey].Length);
                HighlightRule ho = this._highlightRules[groupKey].ConstructObject(this._backupRtf);
                this._backupRtf.SelectionColor = ho.HighlightColor;
                this._backupRtf.SelectionBackColor = ho.HighlightBackColor;
                this._backupRtf.SelectionFont = ho.HighlightFont;                
                // Initiate recursive highlight on the matched token
                if(this._highlightRules.RecursiveDependencies.ContainsKey(groupKey))
                    this.RecursiveHighlight(m.Groups[groupKey].Value, groupKey, m.Groups[groupKey].Index + index);
            }
        }
        
        #endregion
    }
}
