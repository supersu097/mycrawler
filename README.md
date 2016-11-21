# mycrawler
 A series of crawlers written in py which make my life more comfortable  

# Overview
- yinwang_blog_reminder.py 
Whatever Yinwang publish or delete one or more blog,you can always get to be known
by the Email you set.

# Prerequisite 
Execute the command below to solve the dependency:
`sudo pip install -r requirement.txt`  

# Configuration & Notice 
You need to create a file named `config.py` with three required fields of `sender` `receiver` and `pwd`.Their data type are all the String.And it's also important to know that not one of them can be dispensed with.The value of sender and receiver are the respective Email adress as their literal meaning representing. First of all,for the filed of sender,I use the Email sevice provider of 126.com as the sender.And all about the sender you should know is that you need to allow the POP3/SMTP/IMAP service in the system setting page and remember the URL of the SMTP server such as smtp.126.com.Next,about the field of receiver mentioned above,it is:  
```
A list of addresses to send this mail to. A bare string will be treated as a list with 1 address.
```
which means I think that if you have several friends that need to receive the message from you,the field of receiver's data type shoud be a List with String.Finally,the filed of pwd is an auth code for mail.126.com in this circumstance for me.

# Usage
Once all steps above you have done,just run one of the scripts which show in this repo to wait lots of 1s to see what will happen.For example:  
`python yinwang_blog_reminder.py`


