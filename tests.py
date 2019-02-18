from bs4 import BeautifulSoup
import unittest
import requests
import re


class ChangeHabraPagesTest(unittest.TestCase):

    def setUp(self):
        self.url = "http://localhost:8003/ru/"

    def test_right_change_words_on_page(self):
        response = requests.get("{}post/439856/".format(self.url))
        soup = BeautifulSoup(response.content, 'lxml')
        assert soup.find('span', {'class': 'post__title-text'}).text.strip() == "Яндекс™! Спасибо за Uber"
        assert soup.find('a', {'class': 'user-info__fullname'}).text.strip() == "Rustam™ Sultansoy"

    def test_should_return_page_with_digits_without_changes(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, "lxml")
        assert len(soup.find("span", {"class": "companies-rating__rating"}).text.strip()) == 7

    def test_should_change_word_with_marks_between_letters(self):
        response = requests.get("{}post/218855/".format(self.url))
        soup = BeautifulSoup(response.content, 'lxml')
        assert "Erlang™/OTP" in soup.find("span", {"class": "post__title-text"}).text

if __name__ == "__main__":
    unittest.main()