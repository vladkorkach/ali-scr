import re
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class AliScr:

    driver = None   #   link to driver
    cookies = None   #   cookies
    timeout_default = 3   #    timeout
    ali_login_frame = "alibaba-login-box"   #    login box frame id
    ali_login_frame_id = "fm-login-id"   #    login input id
    ali_login_frame_pwd = "fm-login-password"   #    login input for pwd
    ali_popup_close_id = "close-layer"   #   close button id
    ali_search_input = ".//*[@id='search-key']"   #   xpath search_input
    ali_regional_setting = "//a[@id='switcher-info']"   #   xpath regional_setting
    ali_country_setting = "//div[contains(@class, 'country-selector')]"   #   xpath for country_setting
    ali_country_setting_set = "//span[contains(@class, 'css_{}')]"   #   xpath set country_setting
    ali_currency_setting = "//div[@class='switcher-currency-c']"   #   xpath currency_setting
    ali_currency_setting_set = "//a[@data-currency='{}']"   #   xpath set currency_setting
    ali_regional_setting_save = "//button[@data-role='save']"   #   xpath save regional_setting
    xpath_get_item = "//h3[@class='icon-hotproduct']//a[contains(@class, 'history-item')]"   #   xpath item
    login_url = "https://login.aliexpress.com/"   #   ali login url
    en_loc = "https://www.aliexpress.com/country/gb-united-kingdom.html"   #   link to main page
    WEB_URL_REGEX = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"   #   regexp for link

    def __init__(self, user, pwd):
        self.user = user
        self.passwd = pwd

    def _check_ad(self):
        try:
            items = self.driver.find_element_by_class_name(self.ali_popup_close_id)
            if items is not None:
                items.click()
        except NoSuchElementException:
            print('No AD popup found!')

    def login(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.login_url)
        self.driver.switch_to.frame(self.ali_login_frame)
        self.driver.find_element_by_id(self.ali_login_frame_id).send_keys(self.user)
        self.driver.find_element_by_id(self.ali_login_frame_pwd).send_keys(self.passwd)
        self.driver.find_element_by_id(self.ali_login_frame_pwd).submit()
        time.sleep(self.timeout_default)
        self.cookies = self.driver.get_cookies()
        self.driver.switch_to.default_content()
        time.sleep(self.timeout_default)
        self.driver.close()

    def change(self, itch={'country': '', 'currency': ''}):
        self.driver = webdriver.Chrome()
        self.driver.get(self.en_loc)

        for cookie in self.cookies:
            self.driver.add_cookie(cookie)

        self._check_ad()

        rs_item = self.driver.find_element_by_xpath(self.ali_regional_setting)
        rs_item.click()

        time.sleep(self.timeout_default)

        cs_item = self.driver.find_element_by_xpath(self.ali_country_setting)
        cs_item.click()
        time.sleep(self.timeout_default)
        set_country = cs_item.find_element_by_xpath(self.ali_country_setting_set.format(itch.get('country', None)))
        set_country.click()
        time.sleep(self.timeout_default)

        cs_item = self.driver.find_element_by_xpath(self.ali_currency_setting)
        cs_item.click()
        time.sleep(self.timeout_default)
        set_currency = cs_item.find_element_by_xpath(self.ali_currency_setting_set.format(itch.get('currency', None)))
        set_currency.click()
        time.sleep(self.timeout_default)

        save_item = rs_item.find_element_by_xpath(self.ali_regional_setting_save)
        save_item.click()

        self.cookies = self.driver.get_cookies()

        time.sleep(self.timeout_default)

        self.driver.close()

    def search(self, search_phrase):
        self.driver = webdriver.Chrome()
        self.driver.get(self.en_loc)

        for cookie in self.cookies:
            self.driver.add_cookie(cookie)

        self._check_ad()

        search_item = self.driver.find_element_by_xpath(self.ali_search_input)
        search_item.send_keys(search_phrase)
        search_item.submit()

        item = self.driver.find_element_by_xpath(self.xpath_get_item)
        item.click()
        link = item.get_attribute('href')

        # self.driver.close()

        return re.findall(self.WEB_URL_REGEX, link)


if __name__ == '__main__':

    login = ""
    pwd = ""
    search_str = "Boys Bicycle"
    settings_items_change = dict(
        country='uk',
        currency='GBP'
    )

    i = AliScr(login, pwd)
    i.login()
    i.change(settings_items_change)
    link = i.search(search_str)

    print(link)
