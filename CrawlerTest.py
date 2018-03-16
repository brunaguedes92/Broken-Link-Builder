import unittest
from Crawler import Crawler

class CrawlerTest(unittest.TestCase):
    def setUp(self):
        """Called before each test"""
        self.ignore = ["tag", "respond"]
        self.c = Crawler("acostanza.com", self.ignore)

    def test_getLinksFromURL_DoesntHaveIgnoreListItems(self):
        urls = self.c.getLinksFromURL("http://acostanza.com")
        self.assertTrue(len(urls) > 0)
        for url in urls:
            for ig in self.ignore:
                if ig in url:
                    self.fail('{} is in {} but is on ignore list'.format(ig, url))

        # Only visited the base link
        self.assertEqual(1, len(self.c.visitedLinks))

    def test_getLinksFromMultipleURLs_DoesntHaveIgnoreListItems_AndHasMoreURLsThanSingleURL(self):
        urls = self.c.getLinksFromURLs(["http://acostanza.com", "http://acostanza.com/page/2/"])
        self.assertTrue(len(urls) > 0)
        for url in urls:
            for ig in self.ignore:
                if ig in url:
                    self.fail('{} is in {} but is on ignore list'.format(ig, url))

        urls_singleInitial = self.c.getLinksFromURL("http://acostanza.com")
        self.assertTrue(len(urls) > len(urls_singleInitial))

        # Visited both base links and then the initial link one more time
        self.assertEqual(3, len(self.c.visitedLinks))

    def test_getURLsTwoLevelsDeep(self):
        urls = self.c.getLinksFromURL("http://acostanza.com")
        more_urls = self.c.getLinksFromURLs(self.c.filterInternalURLs(urls))
        self.assertTrue(len(more_urls) > len(urls))

        check_links = list(set(urls + more_urls))
        url_status_tuple = self.c.getStatusOfURLs(check_links)
        errors = [x for x in url_status_tuple if not x[1] == 200]
        print(errors)

    def test_internalLinksAreInternal(self):
        urls = ["http://acostanza.com", "http://google.com"]
        filtered = self.c.filterInternalURLs(urls)
        self.assertEqual(filtered, [urls[0]])

    def test_externalLinksAreExternal(self):
        urls = ["http://acostanza.com", "http://google.com"]
        filtered = self.c.filterExternalURLs(urls)
        self.assertEqual(filtered, [urls[1]])

    def test_incompleteLinksAreIncomplete(self):
        urls = ["http://acostanza.com", "/subreddit"]
        filtered = Crawler.filterIncompleteURLs(urls)
        self.assertEqual(filtered, [urls[1]])

    def test_getStatusOfURL200(self):
        status = self.c.getStatusOfURL("http://acostanza.com")
        self.assertEqual(200, status)

    def test_getStatusofURL404(self):
        status = self.c.getStatusOfURL("http://acostanza.com/potato")
        self.assertEqual(404, status)

    def tearDown(self):
        """Just for reference"""
        self.c.s.close()
        self.c.visitedLinks = []


if __name__ == '__main__':
    unittest.main()