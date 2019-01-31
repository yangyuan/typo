import nltk
import re

from corpus import Corpus


class Validator:
    def __init__(self):
        self.errors = []
        self.terms = set()
        self.corpus = Corpus()

    def validate(self, obj):
        self.errors = []
        self.terms = set()
        self._extract_terms(obj)
        self._validate([], obj)

    def refined_errors(self):
        """
        Remove typo candidates which is known in URL templates.
        """
        errs = []
        for err in self.errors:
            if err['typo'].lower() not in self.terms:
                errs.append(err)
        return errs

    def _extract_terms(self, obj):
        """
        Get terms from URL templates.
        """
        terms = set()
        if 'paths' in obj:
            for path in obj['paths']:
                segs = re.split('[/{}]', path)
                for seg in segs:
                    terms.add(seg.lower())
        self.terms = terms

    def _validate(self, path, obj):
        """
        Validate an Json object.
        """
        if isinstance(obj, str):
            if path[-1] != "pattern":
                self._validate_string(path, obj)
        elif isinstance(obj, dict):
            for key, value in obj.items():
                new_path = path.copy()
                new_path.append('%s' % key)
                self._validate_string(new_path, key, True)
                self._validate(new_path, value)
        elif isinstance(obj, list):
            for index, value in enumerate(obj):
                new_path = path.copy()
                new_path.append('%d' % index)
                self._validate(new_path, value)
        elif isinstance(obj, bool):
            pass
        elif isinstance(obj, int):
            pass
        elif isinstance(obj, float):
            pass
        elif isinstance(obj, type(None)):
            pass
        else:
            print(type(obj))
            raise Exception()

    def _validate_string(self, path, value, value_is_key=False):
        """
        Validate an string object.
        """
        value = re.sub('[/$#{}._|*=\-]', ' ', value)

        tokens = nltk.tokenize.word_tokenize(value)
        for raw_token in tokens:
            if raw_token.startswith("'"):
                raw_token = raw_token[1:]
            if self.corpus.validate_token(raw_token):
                continue
            sub_tokens = Validator.camel_case_split(raw_token)
            ret = True
            for sub_token in sub_tokens:
                ret = ret and self.corpus.validate_token(sub_token)

            if not ret:
                self.errors.append({
                    "isKey": value_is_key,
                    "path": path,
                    "typo": raw_token,
                })

    @staticmethod
    def camel_case_split(identifier):
        """
        CamelCase to Camel Case
        lowerCamelCase to lower Camel Case
        lowerCamelCase0 to lower Camel Case 0
        """
        matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z0-9])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
        return [m.group(0) for m in matches]
