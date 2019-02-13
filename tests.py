from bs4 import BeautifulSoup
import unittest
import requests


class ChangeHabraPagesTest(unittest.TestCase):

    def test_right_change_words_on_page(self):
        article_page_url = "http://localhost:8003/ru/post/439856/"
        response = requests.get(article_page_url)
        soup = BeautifulSoup(response.content, 'lxml')
        assert soup.find('span', {'class': 'post__title-text'}).text.strip() == "Яндекс™! Спасибо за Uber"
        assert soup.find('a', {'class': 'user-info__fullname'}).text.strip() == "Rustam™ Sultansoy"

    def test_should_return_page_with_digits_without_changes(self):
        page_url = "http://localhost:8003/ru/"
        response = requests.get(page_url)
        soup = BeautifulSoup(response.content, "lxml")
        assert soup.find("span", {"class": "companies-rating__rating"}).text.strip() == "1743,00"


if __name__ == "__main__":
    unittest.main()