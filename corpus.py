from os import path


class Corpus:
    def __init__(self):
        self.dictionaries = []

        self._load_glove()
        self._load_custom()

    def validate_token(self, token):
        """
        Check is a token is a known word.

        :param token: The token (case insensitive)
        :return: True iff it's a known token
        """
        token = token.lower()
        for dictionary in self.dictionaries:
            if token in dictionary:
                return True
        return False

    def _load_glove(self):
        """
        Load GloVe corpus.
        """
        dict_glove = set()
        with open(path.join('data', 'glove.txt'), encoding="utf-8") as f:
            for line in f:
                dict_glove.add(line.strip())
        self.dictionaries.append(dict_glove)

    def _load_custom(self):
        """
        Load custom dictionary in dict.txt.
        """
        dict_custom = set()
        with open('dict.txt', encoding="utf-8") as f:
            for line in f:
                if not line.startswith('#'):
                    dict_custom.add(line.strip().lower())
        self.dictionaries.append(dict_custom)
