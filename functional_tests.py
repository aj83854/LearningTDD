from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
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
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
        
        # She is immediately invited to enter a to-do item...
        inputbox = self.browser.find_element_by_id('id_new_item')
        
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        
        # She types "Finish transfer function assignments" into a text box...
        inputbox.send_keys('Finish transfer function assignments')

        # When she hits enter, the page updates, and now the page lists 
        # "1: Finish transfer function assignments" as an item in a to-do list.
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Finish transfer function assignments' for row in rows)
        )

        # There is still a text box inviting her to add another item. She
        # enters "Shave Sammy and Clyde"...
        self.fail('Finish your tests!!')
        # The page updates again, and now shows both items on her list...

        # Hanna wonders whether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.

        # She visits that URL - her to-do list is still there.

        # Satisfied, she goes back to sleep

if __name__ == '__main__':
    unittest.main(warnings='ignore')
