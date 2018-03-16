from Crawler import Crawler

ignore = ['#','mailto','tag']
c = Crawler("acostanza.com", ignore)
urls = c.getLinksFromURL("http://www.acostanza.com")
for url in urls:
    print(url)

more_urls = c.getLinksFromURLs(c.filterInternalURLs(c.rebaseURLs(urls)))

all_links = list(set(urls + more_urls))
for link in all_links:
    print(link)

url_status_tuple = c.getStatusOfURLs(c.rebaseURLs(all_links))
errors = [x for x in url_status_tuple if not x[1] == 200]
print(errors)
