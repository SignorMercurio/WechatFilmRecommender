# WechatFilmRecommender

Auto-replying film info in Wechat by crawling the website douban.

## What can it do?

* Send any message with the word '电影'.

* You'll receive a list of types of films. Choose one and send it back.

* Top 10 movies listed in douban in three order(heat, time, rating) will be given, from which you may select one.

* Specific info about the selected film will be shown.

## What do I need to run it?

* BS4(for BeautifulSoup)
* lxml
* Selenium(for webdriver)
* chromedriver.exe
* itchat

Note: This project runs Chrome, but other browsers like Firefox, PhantomJS, etc. is also applicable, and other drivers may also be necessary.

## How to run it?

Just modify the path of chromedriver.exe(see detail in the code) and run AutoReply.py.
