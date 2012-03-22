namespace NX_Syntax_Highlighter_Omega
{
    partial class MainForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(MainForm));
            this.richTextOutput = new System.Windows.Forms.RichTextBox();
            this.buttonHighlight = new System.Windows.Forms.Button();
            this.textBoxInput = new System.Windows.Forms.RichTextBox();
            this.SuspendLayout();
            // 
            // richTextOutput
            // 
            this.richTextOutput.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom)
                        | System.Windows.Forms.AnchorStyles.Left)
                        | System.Windows.Forms.AnchorStyles.Right)));
            this.richTextOutput.DetectUrls = false;
            this.richTextOutput.Location = new System.Drawing.Point(467, 91);
            this.richTextOutput.Name = "richTextOutput";
            this.richTextOutput.Size = new System.Drawing.Size(672, 362);
            this.richTextOutput.TabIndex = 0;
            this.richTextOutput.Text = "";
            this.richTextOutput.WordWrap = false;
            // 
            // buttonHighlight
            // 
            this.buttonHighlight.Location = new System.Drawing.Point(24, 62);
            this.buttonHighlight.Name = "buttonHighlight";
            this.buttonHighlight.Size = new System.Drawing.Size(75, 23);
            this.buttonHighlight.TabIndex = 2;
            this.buttonHighlight.Text = "Highlight";
            this.buttonHighlight.UseVisualStyleBackColor = true;
            this.buttonHighlight.Click += new System.EventHandler(this.buttonHighlight_Click);
            // 
            // textBoxInput
            // 
            this.textBoxInput.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom)
                        | System.Windows.Forms.AnchorStyles.Left)));
            this.textBoxInput.BackColor = System.Drawing.Color.White;
            this.textBoxInput.DetectUrls = false;
            this.textBoxInput.Location = new System.Drawing.Point(24, 91);
            this.textBoxInput.Name = "textBoxInput";
            this.textBoxInput.Size = new System.Drawing.Size(423, 362);
            this.textBoxInput.TabIndex = 3;
            this.textBoxInput.Text = resources.GetString("textBoxInput.Text");
            this.textBoxInput.WordWrap = false;
            // 
            // MainForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1170, 479);
            this.Controls.Add(this.textBoxInput);
            this.Controls.Add(this.buttonHighlight);
            this.Controls.Add(this.richTextOutput);
            this.Name = "MainForm";
            this.Text = "Form1";
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.RichTextBox richTextOutput;
        private System.Windows.Forms.Button buttonHighlight;
        private System.Windows.Forms.RichTextBox textBoxInput;
    }
}

