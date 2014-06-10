# !/usr/bin/env python
# -*-coding:UTF-8-*-

import Queue
import threading
import urllib2
from readability.readability import Document


class GetFullText(threading.Thread):
    """ Thread grab full html text """

    def __init__(self, queue, out_queue, timeout):
        threading.Thread.__init__(self)
        self.queue = queue
        self.out_queue = out_queue
        self.timeout = timeout

    def run(self):
        while True:
            # grab url from queue
            url = self.queue.get()

            try:
                # timeout 
                html = urllib2.urlopen(url, timeout=self.timeout).read()
                readable_article = Document(html).summary()
                # put result in queue, so main program will process it.
                self.out_queue.put((url, readable_article))
            except IOError:
                pass

            self.queue.task_done()


if __name__ == "__main__":
    # Test
    queue = Queue.Queue()
    out_queue = Queue.Queue()

    for i in xrange(5):
        t = GetFullText(queue, out_queue, 10)
        t.setDaemon(True)
        t.start()

    urls = ["http://www.baidu.com", "http://www.google.com",
            "http://www.cppblog.com", "http://www.twitter.com"]

    # put url in threads pool
    for _url in urls:
        queue.put(_url)

    # wait threads
    queue.join()

    while not out_queue.empty():
        _url, content = out_queue.get()
        print _url, content[:50]
        print
