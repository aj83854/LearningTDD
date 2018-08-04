from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
    
    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Hanna has heard about a new to-do app.
        # She goes to check out it's homepage...
        self.browser.get('http://127.0.0.1:8000')

        # She notices the page title and header mention to-do lists...
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')
        
        # She is immediately invited to enter a to-do item...

        # She types "Finish transfer function assignments" into a text box...

        # When she hits enter, the page updates, and now the page lists 
        # "1: Finish transfer function assignments" as an item in a to-do list...

        # There is still a text box inviting her to add another item. She
        # enters "Shave Sammy and Clyde"...

        # The page updates again, and now shows both items on her list...

        # Hanna wonders whether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.

        # She visits that URL - her to-do list is still there.

        # Satisfied, she goes back to sleep

if __name__ == '__main__':
    unittest.main(warnings='ignore')
