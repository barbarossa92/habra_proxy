from bs4 import BeautifulSoup
import unittest
import requests


class ChangeHabraPagesTest(unittest.TestCase):

    def test_right_change_words_on_page(self):
        article_page_url = "http://localhost:8003/ru/post/439856/"
        response = requests.get(article_page_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        assert soup.find('span', {'class': 'post__title-text'}).text.strip() == "Яндекс™! Спасибо за Uber"
        assert soup.find('a', {'class': 'user-info__fullname'}).text.strip() == "Rustam™ Sultansoy"


if __name__ == "__main__":
    unittest.main()