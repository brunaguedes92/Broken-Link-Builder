# Purpose
The purpose of this free tool is to enable Marketers to easily find broken links for Broken Link Building.

## Full Post
A full blog post explaining this Crawler and the motivations [can be found on my website here](http://acostanza.com/2018/03/15/broken-link-building-automation-python-marketers/).

## Installation
To install locally, type the following into terminal:

```
git clone https://github.com/adcostanza/Broken-Link-Builder
virtualenv env
source ./env/bin/activate
pip install -r requirements.txt
```

## Example usage
As seen in `Example.py`:
```
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
```

## Warning
Using this tool on a website you do not own may violate the Terms of Service of that website and may result in you being banned from that website or at worst legal action. Use at your own discretion and preferably only on websites you own or owned by your clients.
