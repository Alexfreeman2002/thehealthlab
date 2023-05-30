"""
Test file for the search.py module.

Compares the retrieved HTML of the target to the expected HTML within the
given txt file.

NOTE:
    -   The HTML within the text file needs to be manually updated if the structure
        of the target site changes.
    -   For the NHSWebCrawler case, to ensure the right HTML is compared, visit
        the page for the target condition within the health index and take these
        steps (Assumes you will be using Firefox):

        1.  Right-click on the brief condition description, and select 'Inspect
            (Element)'.
        2.  Go up the DOM tree of that element to find the parent article element.
        3.  Right-click on the article element, select 'Copy', then 'Inner HTML'.
        4.  Open search_expected_result.txt and paste the result.
        5.  Run the test as normal.
"""


from SearchDiseases import search
import unittest


def read_expected_result(file_path):
    """
        Reads the expected result from a file.

        Args:
            file_path (string): Path to the file containing the expected result.

        Returns:
            string: Contents of the file as a string.
        """
    with open(file_path, 'r') as file:
        return file.read()

    
class TestSearch(unittest.TestCase):
    def test_calculate_bmi(self):
        """Test case for searching and retrieving data from the NHS website."""
        url = 'https://www.nhs.uk/conditions/'
        nhs = search.NHSWebsiteCrawler(url)

        term = 'Headaches'
        expected_result_file = 'search_expected_result.txt'
        expected_result = read_expected_result(expected_result_file)

        # Perform the search and retrieve data from the website
        success, result = nhs.search_website(term)
        result = nhs.retrieve_data(term)

        # Ensures both variables are of the same time before comparison
        result = str(result)
        expected_result = str(expected_result)

        print(success, result, expected_result)

        # Compare the expected result with the actual result as strings
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    # Run the test cases
    unittest.main()
