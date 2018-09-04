from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
    
    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_for_one_user(self):
        # Hanna has heard about a new to-do app.
        # She goes to check out it's homepage...
        self.browser.get(self.live_server_url)

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
        # "1: Finish transfer function assignments" as an item in a to-do list table:
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Finish transfer function assignments')

        # There is still a text box inviting her to add another item. She
        # enters "Shave Sammy and Clyde"...
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Shave Sammy and Clyde')
        inputbox.send_keys(Keys.ENTER)
        
        # The page updates again, and now shows both items on her list...
        self.wait_for_row_in_list_table('2: Shave Sammy and Clyde')
        self.wait_for_row_in_list_table('1: Finish transfer function assignments')

        # Satisfied, she goes back to sleep

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Hanna starts a new to-do list...
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Finish transfer function assignments')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Finish transfer function assignments')

        # She notices that her list has a unique URL...
        hanna_list_url = self.browser.current_url
        self.assertRegex(hanna_list_url, '/lists/.+')

        # Now a new user, Tony, comes along to the site.

        ## We use a new browser session to make sure that no information
        ## of Hanna's is coming through from cookies/cache, etc...
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Tony visits the home page. There is no sign of Hanna's list...
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Finish transfer function assignments', page_text)
        self.assertNotIn('Shave Sammy and Clyde', page_text)

        # Tony starts a new list by entering a new item...
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Tony gets his own unique URL...
        tony_list_url = self.browser.current_url
        self.assertRegex(tony_list_url, '/lists/.+')
        self.assertNotEqual(tony_list_url, hanna_list_url)

        # Again, there is no trace of Hanna's list...
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Finish transfer function assignments', page_text)
        self.assertIn('Buy milk', page_text)

        # Satisfied, they both go back to sleep.

    def test_layout_and_styling(self):
        # Hanna goes to the home page...
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # She notices the input box is nicely centered...
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
