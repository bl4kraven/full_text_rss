##这是什么##

full_text_rss是Python写的全文RSS输出程序，可以作为CGI程序运行在HTTP服务器下。主要参考了[fivefilters的全文RSS PHP实现](http://fivefilters.org/content-only/)和[feedcache库](http://www.doughellmann.com/articles/pythonmagazine/features/feedcache/index.html#persistent-storage-with-shelve)实现

##依赖Python库##

* [feedparser](http://pypi.python.org/pypi/feedparser/)

        sudo pip install feedparser

* [Readability-lxml 0.2.5 ](http://pypi.python.org/pypi/readability-lxml)

        sudo apt-get install libxml2-dev libxslt1-dev
        sudo apt-get install python-dev
        sudo pip install readability-lxml

##使用##

放入Apache根目录下，设置目录可以运行CGI即可。

API如下：

        http://yourserverhost/index.cgi?url=feedurl

