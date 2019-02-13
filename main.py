from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import requests
import string
import re
import html
from bs4 import BeautifulSoup
from bs4.element import Comment

PORT = 8003


class Handler(BaseHTTPRequestHandler):

    habr_url = "https://habr.com"
    not_needed_tags = ('style', 'script', 'head', 'title', 'meta', '[document]',)
    mimetypes = {
        'jpg': 'image/jpg',
        'ico': 'image/ico',
        'gif': 'image/gif',
        'png': 'image/png',
        'js': 'application/javascript',
        'css': 'text/css',
        'woff2': 'text/css',
        'svg': 'image/svg+xml'
    }
    punctuation = string.punctuation + "»«"
    table = str.maketrans({key: None for key in punctuation})

    def _get_mimetype(self):
        path = self.path
        if "?" in self.path:
            path = self.path.split("?")[0]
        path_format = path.split("/")[-1]
        if path_format:
            return self.mimetypes.get(path_format.split(".")[-1])
        return 'text/html'

    def _sentence_filtering(self, elem):
        return elem.parent.name not in self.not_needed_tags and not isinstance(elem, Comment)

    def _check_word_length_and_replace(self, word):
        clear_word = str(word).translate(self.table)
        letters = re.findall("[a-zA-ZА-Яа-я]+", word)
        if len(clear_word) == 6 and letters:
            new_word = clear_word + "™"
            word = word.replace(clear_word, new_word)
        return word

    def do_GET(self) -> None:
        response = requests.get(self.habr_url + self.path)
        self.send_response(response.status_code)
        self.send_header('Content-type', self._get_mimetype())
        self.end_headers()
        if self._get_mimetype() == 'text/html':
            soup = BeautifulSoup(response.content, 'lxml')
            text = soup.find_all(text=True)
            for el in soup.select('a[href^="https://habr.com"]'):
                el['href'] = el['href'].replace(self.habr_url, 'http://localhost:%s' % PORT)
            for sentence in text:
                if self._sentence_filtering(sentence):
                    new_sentence = " ".join(map(self._check_word_length_and_replace, sentence.__str__().split()))
                    sentence.replace_with(new_sentence)
            self.wfile.write(bytes(html.unescape(soup.prettify(formatter='html')), 'utf-8'))
            return
        self.wfile.write(response.content)
        return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass


if __name__ == '__main__':
    server = ThreadedHTTPServer(('localhost', PORT), Handler)
    print("Starting server, use <Ctrl-C> to stop")
    server.serve_forever()