# mycrawler
 A series of crawlers written in py which make my life more comfortable  

# Overview
- yinwang_blog_reminder.py &emsp;&emsp;&emsp; the func as the filename says  

# Usage & Notice
1. Use the command below to solve the dependency,especially that you can  
still use the `pip` to install the `Virtualenv` to run this project which means  
you get an isolated virtual environment to avoid some issues,and also means that  
you can run the `pip` command without gaining the root privilage with the prefix  
of `sudo`.  
`sudo pip install -r requirement.txt`  

2. You need to create a file named `config.py` with three required fields of  
`sender` `receiver` and `pwd`.Their data type are all the String.It's important  
to know that not one of them can be dispensed with.The value of `sender` and  
`receiver` are the respective Email adress as their literal meaning that the var  
name represents. For the filed of sender,I use the Email sevice provider of 126.com   
as the sender.All about the sender you should know is that you need to allow the  
POP3/SMTP/IMAP service in the system setting page and remember the URL of the SMTP   
server such as smtp.126.com.Next,the filed of pwd is a auth code for mail.126.com    
in this circumstance.  
And notice that the `receiver` is "A list of addresses to send this mail to.  
A bare string will be treated as a list with 1 address" which means that if you  
have several friends that need to receive the message from you,the field of    
receiver's data type shoud be a List with String data type.  

3. Once all steps above you have done,just run this command below to wait  
lots of 1s to see what will happen.  
`python yinwang_blog_reminder.py`


