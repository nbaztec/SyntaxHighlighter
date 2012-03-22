using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;
using System.Text;
using System.Drawing;

namespace NX.SyntaxHighlighter.Omega
{
    /*
        * (?<!\\)(?<dquote>"(?:[^\\"\r\n]|\\"|\\[^"]|\\\\)*")|
        * (?<!\\)(?<squote>'(?:[^\\'\r\n]|\\'|\\[^']|\\\\)*')|
        * (?<=(?<!\\)(?:(?:\\{2})+)|[^\\]|^)(?:(?<varblock>\${[A-Za-z0-9_]+)(?:[^}])*(?<varblock_end>})|(?<varblock>\$\([A-Za-z0-9_]+)(?:[^)])*(?<varblock_end>\)))     
     */
    /* 
       * (?<!\\)(?<dquote>"(?:[^\\"\r\n]|\\.)*")|
       * (?<!\\)(?<squote>'(?:[^\\'\r\n]|\\'|\\[^']|\\\\)*')|
       * (?<comment>(?:(?<!\$)#.*))|
       * (?:^\s*)(?<var>[A-Za-z_][\w\d_]*?(?==))|
       * (?<=(?<!\\)(?:(?:\\{2})+)|[^\\])(?<refvar>\$[a-zA-z0-9@#$*?][\w\d]*)|
       * (?<=(?<!\\)(?:(?:\\{2})+)|[^\\])(?:(?<varblock>(?<refvar>\${[A-Za-z0-9_]+)(?:[^}])*(?<varblock_end>}))|(?<varblock>(?<refvar>\$\([A-Za-z0-9_]+)(?:[^)])*(?<varblock_end>\))))
       * (?<keyword>\b[^\$]?(if|then|else|elif|fi|for|done|do|while|in|case|esac)\b)|
       * (?<command>\b[^\$]?(ls|read|echo|printf|du|df|who|cat|head|tail|jobs|rm|mkdir|rmdir|mv|cp|set|unset|export|tar|uname|wc)\b)|
       * (?<option>--?[\w\d]+)|
       * (?:\s+)(?<test>\[(?:"(?:(?:\\"|[^"])*")|[^\]])*\])|
       * (?:\s+)(?<backtick>`[^`]*`)
   */
    class BashHighlighter : SyntaxHighlighter
    {
        #region Required Constructors
        public BashHighlighter() 
            : base()
        {              
        }

        public BashHighlighter(Font defaultFont) : base(defaultFont)
        {                        
        }

        public BashHighlighter(string[] keywords, string[] commands, Font defaultFont)
            : base(keywords, commands, defaultFont)
        {                        
        }

        public BashHighlighter(string[] keywords, string[] commands)
            : base(keywords, commands)
        {
        }
        
        public BashHighlighter(HighlightRules highlightRules, Font defaultFont) 
            : base(highlightRules, defaultFont)
        {            
        }

        #endregion

        #region Overridden Abstract Methods
        protected override void SetDefaultRules()
        {
            this._highlightRules.AddRule("dquote",
                    new HighlightRule("(?<!\\\\)(?<dquote>\"(?:[^\\\\\"\r\n]|\\\\.)*\")", Color.FromArgb(0xE60000), HighlightRule.ColorType.Foreground),
                    new string[] { "backtick", "refvar", "varblock" });
            this._highlightRules.AddRule("squote", new HighlightRule("(?<!\\\\)(?<squote>'(?:[^\\\\'\r\n]|\\\\'|\\\\[^\']|\\\\\\\\)*')", Color.FromArgb(0xE60000), HighlightRule.ColorType.Foreground));
            this._highlightRules.AddRule("comment", new HighlightRule("(?<comment>(?:(?<!\\$)#.*))", Color.CornflowerBlue, new Font(this.DefaultFont, FontStyle.Regular)));
            this._highlightRules.AddRule("var", new HighlightRule("(?:^\\s*)(?<var>[A-Za-z_][\\w\\d_]*?(?==))", Color.DarkCyan, HighlightRule.ColorType.Foreground));
            
            //No Highlight Rule, But contains other groups
            this._highlightRules.AddRule("varblock", 
                new HighlightRule("(?<=(?<!\\\\)(?:(?:\\\\{2})+)|[^\\\\])(?:(?<varblock>(?<refvar>\\${[A-Za-z0-9_]+)(?:[^}])*(?<varblock_end>}))|(?<varblock>(?<refvar>\\$\\([A-Za-z0-9_]+)(?:[^)])*(?<varblock_end>\\))))"), 
                new string[] { "refvar" });

            this._highlightRules.AddRule("refvar", new HighlightRule("(?<=(?<!\\\\)(?:(?:\\\\{2})+)|[^\\\\])(?<refvar>\\$[a-zA-z0-9@#$*?][\\w\\d]*)", Color.BlueViolet, HighlightRule.ColorType.Foreground));            
            this._highlightRules.AddRule("keyword", new HighlightRule("(?<keyword>\\b[^\\$]?(" + this.Keywords + ")\\b)", Color.Brown, new Font(this.DefaultFont, FontStyle.Bold)));
            this._highlightRules.AddRule("command", new HighlightRule("(?<command>\\b[^\\$]?(" + this.Commands + ")\\b)", Color.Chocolate, new Font(this.DefaultFont, FontStyle.Bold)));
            this._highlightRules.AddRule("option", new HighlightRule("(?<option>--?[\\w\\d]+)", Color.DarkGoldenrod, HighlightRule.ColorType.Foreground));
            this._highlightRules.AddRule("test",
                    new HighlightRule("(?:\\s+)(?<test>\\[(?:\"(?:(?:\\\\\"|[^\"])*\")|[^\\]])*\\])", Color.PapayaWhip, HighlightRule.ColorType.Background),
                    new string[] { "keyword", "command", "dquote", "squote", "refvar", "varblock", "option" });
            this._highlightRules.AddRule("backtick",
                    new HighlightRule("(?:\\s+)(?<backtick>`[^`]*`)", Color.PapayaWhip, HighlightRule.ColorType.Background),
                    new string[] { "keyword", "command", "dquote", "squote", "refvar", "varblock", "option" });       

            //Simple Highlight Rule
            this._highlightRules.AddRule("varblock_end", new HighlightRule(Color.BlueViolet, HighlightRule.ColorType.Foreground));
        }

        protected override void SetDefaultKeywords()
        {
            this.Keywords = "if|then|else|elif|fi|for|done|do|while|in|case|esac|break|continue|function|return|in";
            this.Commands = "alias|apropos|awk|basename|bash|bc|bg|builtin|bzip2|cal|cat|cd|cfdisk|chgrp|chmod|chown|chroot|cksum|clear|cmp|comm|command|cp|cron|crontab|csplit|cut|date|dc|dd|ddrescue|declare|df|diff|diff3|dig|dir|dircolors|dirname|dirs|du|echo|egrep|eject|enable|env|ethtool|eval|exec|exit|expand|export|expr|false|fdformat|fdisk|fg|fgrep|file|find|fmt|fold|format|free|fsck|ftp|gawk|getopts|grep|groups|gzip|hash|head|history|hostname|id|ifconfig|import|install|join|kill|less|let|ln|local|locate|logname|logout|look|lpc|lpr|lprint|lprintd|lprintq|lprm|ls|lsof|make|man|mkdir|mkfifo|mkisofs|mknod|more|mount|mtools|mv|netstat|nice|nl|nohup|nslookup|open|op|passwd|paste|pathchk|ping|popd|pr|printcap|printenv|printf|ps|pushd|pwd|quota|quotacheck|quotactl|ram|rcp|read|readonly|renice|remsync|rm|rmdir|rsync|screen|scp|sdiff|sed|select|seq|set|sftp|shift|shopt|shutdown|sleep|sort|source|split|ssh|strace|su|sudo|sum|symlink|sync|tail|tar|tee|test|time|times|touch|top|traceroute|trap|tr|true|tsort|tty|type|ulimit|umask|umount|unalias|uname|unexpand|uniq|units|unset|unshar|useradd|usermod|users|uuencode|uudecode|v|vdir|vi|watch|wc|whereis|which|who|whoami|Wget|xargs|yes";
        }

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
                List<string> groupKeys = new List<string>();
                foreach (string key in this._highlightRules.Keys)
                    if (m.Groups[key].Success)
                    {
                        groupKeys.Add(key);
                        //break;
                    }
                // Highlight using the rule                                
                /*if (groupKey == "varblock")
                {
                    this._backupRtf.Select(m.Groups[groupKey].Index + index, m.Groups["refvar"].Length);
                    HighlightRule ho = this._highlightRules[groupKey].ConstructObject(this._backupRtf);
                    this._backupRtf.SelectionColor = ho.HighlightColor;
                    this._backupRtf.SelectionBackColor = ho.HighlightBackColor;
                    this._backupRtf.SelectionFont = ho.HighlightFont;
                    this._backupRtf.Select(m.Groups[groupKey].Index + index + m.Groups[groupKey].Length - 1, 1);
                    this._backupRtf.SelectionColor = ho.HighlightColor;
                    this._backupRtf.SelectionBackColor = ho.HighlightBackColor;
                    this._backupRtf.SelectionFont = ho.HighlightFont;
                }
                else
                {*/
                foreach (string groupKey in groupKeys)
                {
                    this._backupRtf.Select(m.Groups[groupKey].Index + index, m.Groups[groupKey].Length);
                    HighlightRule ho = this._highlightRules[groupKey].ConstructObject(this._backupRtf);
                    this._backupRtf.SelectionColor = ho.HighlightColor;
                    this._backupRtf.SelectionBackColor = ho.HighlightBackColor;
                    this._backupRtf.SelectionFont = ho.HighlightFont;
                    //}
                    // Initiate recursive highlight
                    if (this._highlightRules.RecursiveDependencies.ContainsKey(groupKey))
                        this.RecursiveHighlight(m.Groups[groupKey].Value, groupKey, m.Groups[groupKey].Index + index);
                }
            }
        }
        
        #endregion
    }
}
