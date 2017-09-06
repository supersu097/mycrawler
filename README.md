# mycrawler
 A series of crawlers written in py which make my life better  

## Overview
- `yinwang_blog_reminder.py`  
Know when Mr. Yinwang publish a blog in the very first place by the Email you set, which also depends on ur `cron` setting.

- `pediy_crawler.py`  
A crawler for the bbs of pediy's Android security forum,also you can modify the URL to crawl other forums.

- `v2ex_hot.py`  
Let you know what is the trend and what is the most popular and hottest.

- `zealer_tech.py`  
Know when zealer publishes a new video in [this](http://www.zealer.com:8080/list?cp=2) series.

## Recommanded&Tested Working Env
- Ubuntu 14.04|16.04 x64
- Python3

## Prerequisite 
Execute the command below to solve the dependency:  
`sudo pip3 install -r requirement.txt`  


## Configuration 
You must create a file named `config.py` in the directory of `core`with below fields.  

| Filed | Mandatory | Var Type | Desc |
| ----| ---- | ---- | ---- |
| sender | Y | String | E-mail address |
| receiver | Y | String or List with Strings | E-mail address |
| pwd | Y | String | E-mail's password |


## Usage
Once all steps above you have done,just run one of the scripts which show in this repo to wait lots of 1s to see what will happen.
### `yinwang_blog_reminder.py` 
- You'd better to resort to a small tool named `cron` to run this crawler.   
For more detailed,see this [commit message](https://github.com/supersu097/mycrawler/commit/57c4bcd49da88f1c5cda615995acd88013835ece).
Additionally, i also implemented making screenshot in order to backup it for the future thinking, coz as we all know that, Mr. Yinwang ... Below is how to use,

```
usage: yinwang_blog_reminder.py [-h] [-p]
tu
Help you push the screenshot to ur folk of this repo.

optional arguments:
  -h, --help  show this help message and exit
  -p, --push  Decide whether push the screenshot to github repo or not!
```
- Cron task example
```
@daily cd ~/mycrawler && python3 yinwang_blog_reminder.py -p
```

### `pediy_crawler.py`
```
usage: pediy_crawler.py [-h] -a

A crawler for the bbs of pediy's Android security forum,also you can modify
the url to crawl other forum.

optional arguments:
  -h, --help  show this help message and exit
  -a, --all   Get all threads and tagged threads of 优秀,精华 and 关注
```
### `v2ex_hot.py`
- Nothing special to emphasize, just utilize `cron` like below,
```
0 10,22 * * *	cd ~/mycrawler && python3 v2ex_hot.py
```

## Tips
### `pediy_crawler.py`
You can issue the command of `tail -f all.txt |grep your-keywords` to filter
what you wanna watch.One more thing, the text file of `all_tagged.txt` stores all of the threads with one of the tags mentioned in the usage above and the `all.txt` stores all of the threads in the forum which you specify. And the more important is the display of whole filtering result is dynamic.  
The final demo effect is shown as below:  
<img src="screenshot/keyword_filter.png" width="428" height="141">`
