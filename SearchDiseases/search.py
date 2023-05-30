"""
Web Crawler Search

This module provides all the necessary classes and functions to retrieve data
from a target website through the method of web scraping using the requests 
and BeautifulSoup modules.
"""


import requests
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod


class WebsiteCrawler(ABC):
    """
    Abstract Parent class to create a web crawler object to request, contain 
    and manage the target url, HTML content, and its list of matches to the 
    given term.

    Args:
        ABC (ABC): an Abstract Base Class

    Methods:
        __init__(self, url):
            Class initialization for abstract WebsiteCrawler.

        search_website(self, term):
            Abstract method to search through the target website. Can be implemented
              in its child classes.

        retrieve_data(self, term):
            Abstract method to retrieve the target data from the target website. 
            Can be implemented in its child classes.

        make_soup(html):
            Parses the given HTML document and returns a BeautifulSoup object.

        make_request(self):
            Makes a request to the assigned URL and returns the retrieved 
            HTML content.

        __str__(self):
            Returns a string representation of the instance. Can be implemented
            in the child classes.
    """

    def __init__(self, url):
        """Class initialisation for abstract WebsiteCrawler

        Args:
            url (string): string form of the url to the target site
        """
        self._url = url
        self._content = self.make_soup(self.make_request())
        self.matches = []

    @property
    def url(self):
        """
        Getter method for the URL property.

        Returns:
            string: The URL of the target site.
        """
        return self._url

    @property
    def content(self):
        """
        Getter method for the content property.

        Returns:
            BeautifulSoup: The parsed HTML content of the target site.
        """
        return self._content

    @url.setter
    def url(self, url):
        """
        Setter method for the URL property.

        Args:
            url (string): The URL to assign.

        """
        self._url = url

    @content.setter
    def content(self, content):
        """
        Setter method for the content property.

        Args:
            content (string): The HTML content to assign.

        Notes:
            The content will be automatically parsed using the make_soup method before assigning.
        """
        # automatically parse the HTML before assigning
        self._content = self.make_soup(content)

    @abstractmethod
    def search_website(self, term):
        """
        Abstract method to search through the target website. Can be
        written in its child classes.

        Args:
            term (string): the string form of the search term given by the user
        """
        pass

    @abstractmethod
    def retrieve_data(self, term):
        """
        Abstract method to retrieve the target data from the target website.
        Can be written in its child classes.

        Args:
            term (string): the string form of the search term given by the user
        """
        pass

    @staticmethod
    def make_soup(html):
        """
        Parses the given HTML document and returns a BeautifulSoup object.

        Args:
            html (bytes): bytes representation of the HTML doc to parse

        Raises:
            Exception: returns error message with the error type.

        Returns:
            BeautifulSoup: An object representing the parsed HTML document.
        """
        try:
            return BeautifulSoup(html, "html.parser")
        except Exception as e:
            raise Exception(f"An error occurred: {str(e)}")

    def make_request(self):
        """
        Makes a request to the assigned url and returns the retrieved HTML content.

        Returns:
            bytes: The content of the response.

        Raises:
            ValueError: If no URL is assigned.
            Exception: If an error occurs while retrieving data from the URL.
        """
        if not self.url:
            raise ValueError('No URL assigned.')

        response = requests.get(self.url)

        if response.status_code == 200: # if successful
            return response.content
        else:
            raise Exception(f"Error: Unable to retrieve data from {self.url}.")

    def __str__(self):
        """
        string: A string representation of the instance. Can be written in the
        child classes.
        """
        pass


class NHSWebsiteCrawler(WebsiteCrawler):
    """
    A child class of the WebsiteCrawler to specifically request and extract 
    data from the NHS website.

    Args:
        WebsiteCrawler (WebsiteCrawler): The parent class of this class

    Methods:
        __init__(self, url):
            Class initialization for NHSWebsiteCrawler.

        search_website(self, term):
            Searches the NHS website for the specified term.

        retrieve_data(self, term):
            Retrieves the target data from the NHS website based on the specified term.

        __str__(self):
            Returns a string representation of the instance.
    """
    def __init__(self, url):
        super().__init__(url)

    def search_website(self, term):
        """
        Searches the website for the specified term.

        Parameters:
            term (string): The term to search for.

        Returns:
            tuple: contains the link (<a>) text (str), and its url (str).

        Raises:
            ValueError: If the search term is invalid.
        """
        if term[0] == ' ':
            raise ValueError('Invalid search term. Mis-input URL?')

        first_char = term[0].upper()

        parent_container = self.content.find(id=first_char).parent
        links = parent_container.select("ul li a")

        for link in links:
            self.matches.append([link.text.strip(), link['href']])

        for match in self.matches:
            if term[0].upper()+term[1:] == match[0]:
                return True, match[0]

        return False, self.matches

    def retrieve_data(self, term):
        """
        Retrieves data related to the specified term from the website.

        Parameters:
            term (string): The term to retrieve data for.

        Returns:
            BeautifulSoup: An object representing the retrieved article.

        Modifies:
            - Updates the URL of the crawler instance.
            - Updates the content of the crawler instance.

        Notes:
            This method assumes that the search_website method has been called before retrieving the data.
        """
        for match in self.matches:
            if term[0].upper()+term[1:] == match[0]:
                self.url = 'https://www.nhs.uk' + match[1]
                self.content = self.make_request()

        # Remove all classes
        for element in self.content.find_all(class_=True):
            element['class'] = []

        # The core content 
        article = self.content.find('article')

        # Remove unnecessary data within html tags
        for element in article.find_all():
            element.attrs = {}
        article.get_text(strip=True)

        # Remove unwanted svg elements
        for svg in article.find_all('svg'):
            svg.decompose()

        # Remove unwanted nav element
        nav = article.find('nav')
        if nav:
            nav.decompose()

        # Remove unwanted video elements
        video = article.find('video')
        if video:
            video.decompose()

        return article

    def __str__(self):
        """
        Returns a string representation of the NHSWebsiteCrawler instance.

        Returns:
            string: A string representation of the instance.
        """
        return ' | '.join(str(match) for match in self.matches)


if __name__ == '__main__':
    url = 'https://www.nhs.uk/conditions/'
    nhs = NHSWebsiteCrawler(url)

    term = 'Headaches'
    success, result = nhs.search_website(term)
    html_result = nhs.retrieve_data(term)

    print(success)
    print(html_result)
