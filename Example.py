from Crawler import Crawler

import os

ignore = ['#','mailto','tag','itmss://']
c = Crawler(os.environ.get('DOMAIN'), ignore)
urls = c.getLinksFromURL(os.environ.get('URL'))

rebasedURLS = c.rebaseURLs(urls)
filteredInternalURLS = c.filterInternalURLs(rebasedURLS)
more_urls = c.getLinksFromURLs(filteredInternalURLS)

all_links = c.rebaseURLs(list(set(urls + more_urls)))

url_status_tuple = c.getStatusOfURLs(all_links)
errors = [x for x in url_status_tuple if not x[1] == 200]
print(errors)
