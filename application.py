from flask import Flask, request, send_from_directory
import urllib.request
import os.path
import json
import nltk

from validator import Validator


def initialize():
    nltk.download('punkt')

    urllib.request.urlretrieve(
        'https://gist.githubusercontent.com/yangyuan/4925d9764f26c2da723c622dbbc42c4a/raw/fe9d7fb6ecbf8b47a26f1b5456d987ef78d55d63/glove.6B.txt',
        os.path.join('data', 'glove.txt'))


app = Flask(__name__)
initialize()


@app.route('/')
def root():
    """
    Default to `index.html`
    """
    return send_from_directory('www', 'index.html')


@app.route('/<path:path>')
def default(path):
    """
    Default to `www` folder
    """
    return send_from_directory('www', path)


@app.route('/api/validate', methods=['POST'])
def validate():
    """
    Validate a Swagger file.
    :return: a list of errors.
    """
    content = request.json
    tmp = Validator()
    tmp.validate(content)
    return json.dumps(tmp.refined_errors())


@app.route('/api/fetch', methods=['POST'])
def fetch():
    """
    Fetch Json from a URL. Could be a url to a raw Swagger file or a github page of a Swagger file.
    :return:
    """
    content = request.json
    url = content['url']

    # https://github.com/Azure/azure-rest-api-specs/blob/master/specification/cognitiveservices/data-plane/Face/stable/v1.0/Face.json
    # >>
    # https://raw.githubusercontent.com/Azure/azure-rest-api-specs/master/specification/cognitiveservices/data-plane/Face/stable/v1.0/Face.json

    if url.startswith('https://github.com/'):
        url = url.replace('github.com', 'raw.githubusercontent.com', 1)
        url = url.replace('blob/', '', 1)

    contents = urllib.request.urlopen(url).read()
    return contents


if __name__ == "__main__":
    app.run()
