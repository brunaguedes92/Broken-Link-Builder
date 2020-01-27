from Crawler import Crawler

ignore = ['#','mailto','tag']
c = Crawler("www.gov.br", ignore)
urls = c.getLinksFromURL("https://www.gov.br/")
# for url in urls:
#     print(url)

rebasedURLS = c.rebaseURLs(urls)
filteredInternalURLS = c.filterInternalURLs(rebasedURLS)
more_urls = c.getLinksFromURLs(filteredInternalURLS)

print (more_urls)
all_links = list(set(urls + more_urls))
for link in all_links:
    print(link)

url_status_tuple = c.getStatusOfURLs(c.rebaseURLs(all_links))
errors = [x for x in url_status_tuple if not x[1] == 200]
print(errors)
