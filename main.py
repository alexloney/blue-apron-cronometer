import re
import time
import logging
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from http.server import HTTPServer, BaseHTTPRequestHandler
from selenium.webdriver.chrome.options import Options

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        match = re.match(r'.*(https?://(www\.)?blueapron\.com.*)$', self.path)
        if not match:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes('Could not find Blue Apron in URL', 'utf-8'))
            return
        
        print(match.groups(1)[0])
        driver.get(match.groups(1)[0])
        driver.implicitly_wait(10)

        title_element = driver.find_element(by=By.CLASS_NAME, value='ba-recipe-title__main')
        page_title = title_element.text

        ingredients = []
        elements = driver.find_elements(by=By.CLASS_NAME, value='ba-info-list')

        for element in elements:
            for li in element.find_elements(by=By.TAG_NAME, value='li'):
                ingredients.append(li.text)

        self.send_response(200)
        self.end_headers()

        self.wfile.write(bytes('<!DOCTYPE html>\r\n', 'utf-8'))
        self.wfile.write(bytes('<html lang="en-US">\r\n', 'utf-8'))
        self.wfile.write(bytes('<head>\r\n', 'utf-8'))
        self.wfile.write(bytes('<title>' + page_title + '</title>\r\n', 'utf-8'))
        self.wfile.write(bytes('<script type="application/ld+json">\r\n', 'utf-8'))
        self.wfile.write(bytes('{\r\n', 'utf-8'))
        self.wfile.write(bytes('"@context": "https://schema.org",\r\n', 'utf-8'))
        self.wfile.write(bytes('"@graph": [\r\n', 'utf-8'))
        self.wfile.write(bytes('{\r\n', 'utf-8'))
        self.wfile.write(bytes('"@context": "https://schema.org/",\r\n', 'utf-8'))
        self.wfile.write(bytes('"@type": "Recipe",\r\n', 'utf-8'))
        self.wfile.write(bytes('"name": "' + page_title + '",\r\n', 'utf-8'))
        self.wfile.write(bytes('"recipeYield": "2 servings",\r\n', 'utf-8'))
        self.wfile.write(bytes('"recipeIngredient": [\r\n', 'utf-8'))
        first = True
        for item in ingredients:
            if first:
                first = False
            else:
                self.wfile.write(bytes(',', 'utf-8'))
            self.wfile.write(bytes('"' + item + '"', 'utf-8'))
        self.wfile.write(bytes(']\r\n', 'utf-8'))
        self.wfile.write(bytes('}\r\n', 'utf-8'))
        self.wfile.write(bytes(']\r\n', 'utf-8'))
        self.wfile.write(bytes('}\r\n', 'utf-8'))
        self.wfile.write(bytes('</script>\r\n', 'utf-8'))
        self.wfile.write(bytes('</head>\r\n', 'utf-8'))
        self.wfile.write(bytes('<body>\r\n', 'utf-8'))
        
        for item in ingredients:
            self.wfile.write(bytes(item + '\r\n', 'utf-8'))

        self.wfile.write(bytes('</body>\r\n', 'utf-8'))
        self.wfile.write(bytes('</html>\r\n', 'utf-8'))


def set_chrome_options() -> Options:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options

if __name__ == '__main__':
    try:
        driver = webdriver.Chrome(options=set_chrome_options())
        
        stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True)

        httpd = HTTPServer(('0.0.0.0', 10000), MyHandler)
        httpd.serve_forever()
    finally:
        driver.close()
