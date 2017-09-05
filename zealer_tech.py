#!/usr/bin/env python3
# coding=utf-8
from core import helper
from core import html
from bs4 import BeautifulSoup

zealer_tech = 'http://www.zealer.com:8080/list?cp=2'
first_aTag=html.first_a_tag_extract(zealer_tech, 'li.series_item a', pageType='special')

soup = BeautifulSoup(""""<a class="series_itemImg" href="/post/2095" target="_blank"><div class="show_img global_play">
<img src="http://img0.zealer.com/e4/8c/e0/95b6c2943f311c997b0f5d6329.jpg"/> <span class="list_cover"></span>
<span class="left_line"></span> <span class="right_line"></span> <span class="list_play">播放</span></div>
<p class="series_subTitle">「科技相对论」对话小米：智能家居的未来</p></a>""",'html5lib')
tag = soup.a.p.get_text()


