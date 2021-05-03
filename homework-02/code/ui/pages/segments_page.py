import allure
from ui.pages.base_page import BasePage
from ui.locators.pages_locators import SegmentPageLocators
from selenium.webdriver.support import expected_conditions as EC


class SegmentPage(BasePage):
    url = 'https://target.my.com/segments/segments_list'
    locators = SegmentPageLocators()

    @allure.step('Creation new segment')
    def create_segment(self, name):
        self.wait(10).until(EC.element_to_be_clickable(self.locators.COUNT_SEGMENTS))

        # Chose a right locator
        if self.find(self.locators.COUNT_SEGMENTS, 10).text == '0':
            create_locator = self.locators.CREATE_SEGMENT
        else:
            create_locator = self.locators.CREATE_NEW_SEGMENT

        self.click(create_locator)
        self.click(self.locators.SEGMENT_CHECKBOX)
        self.click(self.locators.ADD_SEGMENT)
        self.insert(name, self.locators.SEGMENT_NAME)
        self.click(self.locators.CREATE_NEW_SEGMENT)
        created_segment = self.find((self.locators.SEGMENT_LIST_TEMPLATE[0],
                                     self.locators.SEGMENT_LIST_TEMPLATE[1].format(name)))

        return created_segment.text

    @allure.step('Deletion segment')
    def delete_segment(self, name):
        # Create new segment
        segment_name = self.create_segment(name)
        assert name == segment_name
        segment_locator = (self.locators.SEGMENT_LIST_TEMPLATE[0], self.locators.SEGMENT_LIST_TEMPLATE[1].format(name))
        segment = self.find(segment_locator)

        # Delete created segment
        row = segment.find_element_by_xpath('../..')
        row_id = row.get_attribute('data-row-id')  # Get id of created segment
        delete_locator = (self.locators.DELETE_SEGMENT_TEMPLATE[0],
                          self.locators.DELETE_SEGMENT_TEMPLATE[1].format(row_id))
        self.click(delete_locator)
        self.click(self.locators.SUBMIT_DELETION)

        return EC.invisibility_of_element_located(segment_locator)