from urllib import parse
import requests, sys, pprint

class GDriveVideoDownloader():

  def __init__(self, id):

    self.id = id
    headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0',
               "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
               "Accept-Encoding" : "gzip, deflate, br",
               "Accept-Language" : "en-GB,en;q=0.5",
               "Connection" : "keep-alive",}
    self.session = requests.Session()
    self.session.headers.update(headers)
    self.parseQuery()

  def parseQuery(self):
    try:
      url = self.session.get("https://drive.google.com/get_video_info?docid="+self.id)
      self.query = dict(parse.parse_qsl(parse.urlsplit("?"+url.text).query))
    except Exception as err:
      raise Exception("Network connection not available")

    if self.query['status'] == "fail":
      raise Exception(self.query['reason'])

    self.title = self.query['title']
    self.iurl = self.query['iurl']
    self.url = self.parseUrl(self.query["fmt_stream_map"])
    self.fmt = self.parseFormat(self.query['fmt_list'])
    self.length = int(self.query["length_seconds"])

  def print(self):
    print("Title: "+self.title)
    print("Duration: "+self.lengthFormatted())
    print("Image url: "+self.iurl)
    print("Available Quality:")
    for q, u in self.url.items():
      print(self.fmt[str(q)]+" : "+q)

  def download(self, id, name=None):
    if name == None:
      name = self.title
    req = self.session.get(self.url[id], allow_redirects=True)
    open(name, "wb").write(req.content)

  def downloadFile(self, id, name=None):
    if name == None:
      name = self.title

    with self.session.get(self.url[id], stream=True, allow_redirects=True) as r:
      r.raise_for_status()
      #print(r.headers)
      with open(name, 'wb') as f:
        total_length = r.headers.get('content-length')

        if total_length is None: # no content length header
          f.write(r.content)
        else:
          dl = 0
          total_length = int(total_length)
          print("File Size: ", total_length, "bytes")
          try:
            for data in r.iter_content(chunk_size=1024):
                dl += len(data)
                f.write(data)
                done = int(100 * dl / total_length)
                sys.stdout.write("\r Downloading %d%%" % (done,))
                sys.stdout.flush()
            print("\nDownloaded")
          except KeyboardInterrupt as err:
            print("\nDownload Cancelled")

  def getTitle(self):
    return self.title

  def getDuration(self):
    return self.length

  def getImageURL(self):
    return self.iurl

  def getURL(self):
    return self.url

  def getFormat(self):
    return self.fmt

  def parseFormat(self, fmt_list):
    fmt = {}
    for f in fmt_list.split(","):
      ff = f.split("/")
      fmt[ff[0]] = ff[1]
    return fmt

  def parseUrl(self, fmt_stream_map):
    data = {}
    for d in fmt_stream_map.split(","):
      dd = d.split("|")
      data[dd[0]] = dd[1]
    return data

  def lengthFormatted(self):
    min, sec = divmod(self.length, 60)
    hour, min = divmod(min, 60)
    return "%d:%02d:%02d" % (hour, min, sec)
