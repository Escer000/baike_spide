import urllib.request

class HtmlDownloader(object):
    def download(self,url):
        if url is None:
            return None

        res=urllib.request.urlopen(url)

        if res.status_code!=200:
            return None
        return res.read()