using System;
using System.Collections.Generic;
using System.Collections;
using System.ComponentModel;
using System.Data;

using System.Drawing;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Windows.Forms;

using NX.SyntaxHighlighter.Omega;

namespace NX_Syntax_Highlighter_Omega
{
    public partial class MainForm : Form
    {
        RichTextBox backupRTF = new RichTextBox();
        HighlightRules highlightRules = new HighlightRules();
        
        public MainForm()
        {
            InitializeComponent();            
        }

        private void buttonHighlight_Click(object sender, EventArgs e)
        {
            SyntaxHighlighter sh = new BashHighlighter();//new BashHighlighter(new string[] {"for", "if", "fi"}, new string[] {"echo"});
            //sh.GetRules().RemoveRule("squote");
            /*HighlightRules rules = sh.GetRules().EditRule("comment", HighlightRule.EditType.Color, Color.Gray).EditRule("var", HighlightRule.EditType.FontStyle, FontStyle.Underline);
            Dictionary<HighlightRule.EditType, object> updates = new Dictionary<HighlightRule.EditType, object>();
            updates.Add(HighlightRule.EditType.Color, Color.Green);
            updates.Add(HighlightRule.EditType.FontStyle, FontStyle.Bold);
            rules.EditRules(new string[] { "dquote", "squote" }, updates);            */
            sh.DefaultTextColor = Color.Black;
            this.richTextOutput.Rtf = sh.Highlight(this.textBoxInput.Text);
        }
    }
}
