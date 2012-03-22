using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace NX.SyntaxHighlighter.Omega
{
    public interface IHighlighter
    {
        string Highlight(string inputText);
        void SetRules(HighlightRules hRules);
        HighlightRules GetRules();        
    }
}
