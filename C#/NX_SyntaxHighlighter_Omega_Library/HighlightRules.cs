using System;
using System.Collections.Generic;
using System.Text;
using System.Drawing;
using System.Text.RegularExpressions;

namespace NX.SyntaxHighlighter.Omega
{
    public class HighlightRules
    {
        #region Private Data
        /// <summary>
        /// Rules and Dependencies of syntax highlighter
        /// </summary>
        private Dictionary<String, HighlightRule> _highlightRules = new Dictionary<string, HighlightRule>();
        private Dictionary<String, string[]> _highlightDependencies = new Dictionary<string, string[]>();
        #endregion

        #region Overloaded [] Operator
        public HighlightRule this[string key]
        {
            get { return this._highlightRules[key]; }
            set { this._highlightRules[key] = value; }
        }
        #endregion

        #region Properties
        public int Count
        {
            get { return this._highlightRules.Count; }
        }

        public Dictionary<String, HighlightRule>.KeyCollection Keys
        {
            get { return this._highlightRules.Keys; }
        }

        public Dictionary<String, HighlightRule>.ValueCollection Rules
        {
            get { return this._highlightRules.Values; }
        }

        public Dictionary<String, string[]> RecursiveDependencies 
        { 
            get { return this._highlightDependencies; } 
        }
        #endregion

        #region Constructors

        /// <summary>
        /// Basic Constructor
        /// </summary>
        public HighlightRules()
        {
            this._highlightRules = new Dictionary<string, HighlightRule>();
        }

        /// <summary>
        /// Construct object using another HighlightRules object
        /// </summary>
        /// <param name="hr">Object of type HighlightRules</param>
        public HighlightRules( HighlightRules hr )
        {
            this._highlightRules = hr._highlightRules;
        }

        /// <summary>
        /// Construct object using a Dictionary<string, HighlightRule> object
        /// </summary>
        /// <param name="highlightRules">Object of type Dictionary<string, HighlightRule></param>
        public HighlightRules(Dictionary<string, HighlightRule> highlightRules)
        {
            this._highlightRules = highlightRules;
        }

        #endregion

        #region Rule Add/Remove Methods
        /// <summary>
        /// Adds a rule to the current object
        /// </summary>
        /// <param name="key">Key to associate the rule with</param>
        /// <param name="rule">HighlightRule object</param>
        public void AddRule(string key, HighlightRule rule)
        {            
            this._highlightRules.Add(key, rule);            
        }

        /// <summary>
        /// Adds a rule to the current object with recursive dependencies
        /// </summary>
        /// <param name="key">Key to associate the rule with</param>
        /// <param name="rule">HighlightRule object</param>
        /// <param name="dependencies">A string array containing the keys of other rules. [CAUTION!]: DO NOT USE THE CURRENT GROUP NAME.</param>
        public void AddRule(string key, HighlightRule rule, string[] dependencies)
        {
            this._highlightRules.Add(key, rule);
            this._highlightDependencies.Add(key, dependencies);
        }

        /// <summary>
        /// Sets the value of an existing rule.
        /// </summary>
        /// <param name="key">Key of an existing rule</param>
        /// <param name="rule">HighlightRule object</param>
        /// <param name="dependencies">A string array containing the keys of other rules. [CAUTION!]: DO NOT USE THE CURRENT GROUP NAME.</param>
        public void SetRule(string key, HighlightRule rule, string[] dependencies)
        {
            if (this._highlightRules.ContainsKey(key) && this._highlightDependencies.ContainsKey(key))
            {
                this._highlightRules[key] = rule;
                this._highlightDependencies[key] = dependencies;
            }
            else
                throw new KeyNotFoundException("The key `" + key + "` was not found.");
        }

        /// <summary>
        /// Removes the rule from the current object
        /// </summary>
        /// <param name="key">Key of an existing rule</param>
        public void RemoveRule(string key)
        {
            // Remove Rule
            this._highlightRules.Remove(key);

            //Remove Dependency Target, if any
            Dictionary<string, string[]> newEntries = new Dictionary<string, string[]>();            
            foreach (string k in this._highlightDependencies.Keys)
            {
                bool remove = false;
                List<string> dependList = new List<string>();
                foreach(string s in this._highlightDependencies[k])
                {
                    if (s == key)
                        remove = true;
                    else
                        dependList.Add(s);
                }
                if (remove)
                    newEntries.Add(k, dependList.ToArray());//.ToArray();
            }
            foreach(KeyValuePair<string, string[]> kv in newEntries)            
                this._highlightDependencies[kv.Key] = kv.Value;
            
            // Remove Dependecy Source, if present
            if (this._highlightDependencies.ContainsKey(key) == true)
                this._highlightDependencies.Remove(key);
        }

        #endregion

        #region Rule Editing Methods
        /// <summary>
        /// Edit an existing rule
        /// </summary>
        /// <param name="key">Key of an existing rule</param>
        /// <param name="type">Type of edit</param>
        /// <param name="newValue">New value of parameter</param>
        /// <returns>Self</returns>
        public HighlightRules EditRule(string key, HighlightRule.EditType type, object newValue)
        {
            if (type == HighlightRule.EditType.Dependencies)
            {
                if (this._highlightDependencies.ContainsKey(key))
                {
                    if (newValue == null)
                        this._highlightDependencies.Remove(key);
                    else
                        this._highlightDependencies[key] = newValue as string[];
                }
                else if(newValue != null)
                    this._highlightDependencies.Add(key, newValue as string[]);
            }
            else
                this._highlightRules[key] = this._highlightRules[key].GetModifiedObject(type, newValue);
            
            return this;
        }

        /// <summary>
        /// Edit an existing rule
        /// </summary>
        /// <param name="keys">Array of existing keys</param>
        /// <param name="type">Type of edit</param>
        /// <param name="newValue">New value of parameter</param>
        /// <returns>Self</returns>
        public HighlightRules EditRules(string[] keys, HighlightRule.EditType type, object newValue)
        {
            foreach (string key in keys)
            {
                if (type == HighlightRule.EditType.Dependencies)
                {
                    if (this._highlightDependencies.ContainsKey(key))
                    {
                        if (newValue == null)
                            this._highlightDependencies.Remove(key);
                        else
                            this._highlightDependencies[key] = newValue as string[];
                    }
                    else if (newValue != null)
                        this._highlightDependencies.Add(key, newValue as string[]);
                }
                else
                    this._highlightRules[key] = this._highlightRules[key].GetModifiedObject(type, newValue);
            }
            return this;
        }

        /// <summary>
        /// /// Edit an existing rule
        /// </summary>
        /// <param name="keys">Array of existing keys</param>
        /// <param name="updates">Object of type Dictionary<HighlightRule.EditType, object> having the updates</param>        
        /// <returns>Self</returns>        
        public HighlightRules EditRules(string[] keys, Dictionary<HighlightRule.EditType, object> updates)
        {
            foreach (string key in keys)
            {
                foreach (HighlightRule.EditType type in updates.Keys)
                {
                    object newValue = updates[type];
                    if (type == HighlightRule.EditType.Dependencies)
                    {
                        if (this._highlightDependencies.ContainsKey(key))
                        {
                            if (newValue == null)
                                this._highlightDependencies.Remove(key);
                            else
                                this._highlightDependencies[key] = newValue as string[];
                        }
                        else if (newValue != null)
                            this._highlightDependencies.Add(key, newValue as string[]);
                    }
                    else
                        this._highlightRules[key] = this._highlightRules[key].GetModifiedObject(type, newValue);
                }
            }
            return this;
        }

        /// <summary>
        /// /// Edit an existing rule
        /// </summary>
        /// <param name="key">Key of an existing rule</param>
        /// <param name="updates">Object of type Dictionary<HighlightRule.EditType, object> having the updates</param>        
        /// <returns>Self</returns>     
        public HighlightRules EditRule(string key, Dictionary<HighlightRule.EditType, object> updates)
        {

            foreach (HighlightRule.EditType type in updates.Keys)
            {
                object newValue = updates[type];
                if (type == HighlightRule.EditType.Dependencies)
                {
                    if (this._highlightDependencies.ContainsKey(key))
                    {
                        if (newValue == null)
                            this._highlightDependencies.Remove(key);
                        else
                            this._highlightDependencies[key] = newValue as string[];
                    }
                    else if (newValue != null)
                        this._highlightDependencies.Add(key, newValue as string[]);
                }
                else
                    this._highlightRules[key] = this._highlightRules[key].GetModifiedObject(type, newValue);
            }            
            return this;
        }
        #endregion        
    }
}
