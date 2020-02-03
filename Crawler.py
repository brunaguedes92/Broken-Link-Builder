from typing import List, Tuple
import requests
from bs4 import BeautifulSoup
import time


class Crawler:
    def __init__(self, domain: str, ignoreList: List[str]):
        """
        Domain should NOT have http:// in it or a / at the end
        """
        self.s = requests.session()
        self.domain = domain
        self.ignoreList = ignoreList
        self.visitedLinks = []

    def getHTMLFromURL(self, url: str) -> str:
        """
        Retrieve HTML from url that belongs to self.domain
        """
        try:
            if self.domain not in url:
                raise Exception("Cannot get links for external URL", url)
            response = self.s.get(url, timeout=2)
            status_code: int = response.status_code
            self.visitedLinks.append(url)

            if not status_code == 200:
                raise Exception("Status code", status_code, url)

            html: str = response.text

            return html
        except requests.exceptions.Timeout:
            print("Timeout on URL", url)
            print("Sleeping 5 seconds")
            time.sleep(5)
            pass
        except requests.exceptions.ConnectionError:
            print("Connection error on URL", url)
            pass

    def getLinksFromHTML(self, html: str) -> List[str]:
        """
        Returns list of links from HTML retrieved from requests and ignoring ignore phrases
        """
        try:
            soup = BeautifulSoup(html, "html.parser")
            # hrefs = [a['href'] for a in soup.find_all('a')]
            # return list(set(self.ignore(hrefs)))
            hrefs = []
            for a in soup.find_all('a'):
                if 'href' in a.attrs:
                    hrefs.append(a.attrs['href'])
            return list(set(self.ignore(hrefs)))
        except:
            print("html none")
            return []

    def getLinksFromURL(self, url: str) -> List[str]:
        """
        Returns list of links from a single URL by chaining methods
        """
        html = self.getHTMLFromURL(url)
        links = self.getLinksFromHTML(html)
        return links

    def getLinksFromURLs(self, urls: List[str]) -> List[str]:
        """
        Returns list of links from multiple URLs by using getLinksFromURL in list comprehension
        """
        return list(set([link for url in urls for link in self.getLinksFromURL(url)]))

    def ignore(self, links: List[str]) -> List[str]:
        """
        Ignore links that have phrases from ignore list and return new list
        """
        return [link for link in links if not any(ignorePhrase in link for ignorePhrase in self.ignoreList)]

    @staticmethod
    def filterIncompleteURLs(urls: List[str]) -> List[str]:
        """
        Return all URLs that don't start with HTTP or HTTPS
        """
        return [url for url in urls if not url.startswith("http://") and not url.startswith("https://")]

    def filterInternalURLs(self, urls: List[str]) -> List[str]:
        """
        Return all URLs that start with self.domain
        """
        urls = list(set(map(lambda x: self.domain+x if x.startswith("/") and not x.startswith("//") else x, urls)))
        return [url for url in urls if url.startswith("http://"+self.domain) or url.startswith("https://"+self.domain)]

    def filterExternalURLs(self, urls: List[str]) -> List[str]:
        """
        Return all URLs that don't start with self.domain
        """
        return [url for url in urls if self.domain not in url]

    def rebaseURLs(self, urls: List[str]) -> List[str]:
        """
        Take in a list of URLs and return them properly formatted.
        Links such as index.php?home will have the domain name added to the front.
        Links that start with / or // will be updated to also have the internal domian.
        """
        # result = []
        # for url in urls:
        #     if (url.startswith("/") or url.startswith("#")) and not url.startswith("//"):
        #         result.append("https://"+self.domain+url)
        #     else:
        #         result.append(url)

        new_urls = map(lambda url: "https://"+self.domain+url if (url.startswith("/") or url.startswith("#")) and not url.startswith("//") else url, urls)
        new_urls1 = map(lambda url: "https://"+self.domain+"/"+url if not(url.startswith("http://") or url.startswith("https://")) else url, new_urls)
        new_urls2 = map(lambda url: url.replace("//", "http://") if url.startswith("//") else url, new_urls1)
        real_new_urls = map(lambda url: "https://"+url if not url.startswith("http://") and not url.startswith("https://") and "." not in url else url, new_urls2)
        return list(set(real_new_urls))

    def getStatusOfURL(self, url: str) -> int:
        """
        Given a single URL, return the status code of that URL with requests (200 is success)
        """
        try:
            response = self.s.get(url, timeout=5)
            status_code: int = response.status_code
            print(url, status_code)
            return status_code
        except requests.exceptions.SSLError:
            print(url, status_code)
            return 403
        except requests.exceptions.Timeout:
            return 504

    def getStatusOfURLs(self, urls: List[str]) -> List[Tuple[str, int]]:
        """
        Given a list of URLs, get the status of each URL and return in a List of Tuples of statuses and urls
        """
        return [(url, self.getStatusOfURL(url)) for url in urls]
