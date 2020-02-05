from Crawler import Crawler

import os

ignore = ['#','mailto','tag','itmss://']
c = Crawler(os.environ.get('DOMAIN'), ignore)
urls = c.getLinksFromURL(os.environ.get('URL'))

rebasedURLS = c.rebaseURLs(urls)
filteredInternalURLS = c.filterInternalURLs(rebasedURLS)

#more_urls = c.getLinksFromURLs(filteredInternalURLS)

#all_links = c.rebaseURLs(list(set(urls + more_urls)))

#urls2 = c.getLinksFromURLs(all_links)
#all_links2 = c.rebaseURLs(urls2)

url_status_tuple = c.getStatusOfURLs(filteredInternalURLS)

errors = [x for x in url_status_tuple if not x[1] == 200]
print(errors)
