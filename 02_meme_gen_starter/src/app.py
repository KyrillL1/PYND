import random
import os
import sys
import requests
from urllib.parse import urlparse
from flask import Flask, render_template, abort, request, make_response
import quote_engine as qe
import meme_generator as me
from functools import wraps, update_wrapper
from datetime import datetime

app = Flask(__name__, static_folder='./tmp')
meme = me.MemeEngine('./tmp')


def setup():
    """ Load all resources """

    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv']

    quotes = []
    for f in quote_files:
        quotes.extend(qe.Ingestor().parse(f))

    images_path = "./_data/photos/dog/"

    imgs = []
    for root, dirs, files in os.walk(images_path):
        imgs = [os.path.join(root, name) for name in files]

    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """ Generate a random meme """

    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """ User input for meme information """
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """ Create a user defined meme """

    image_url = request.form.get('image_url')
    parsed = urlparse(image_url)
    image_name = os.path.basename(parsed.path)
    resp = requests.get(image_url)
    tmpPath = "./tmp/"+image_name
    with open(tmpPath, 'wb') as out_file:
        out_file.write(resp.content)
    out_file.close()
    path = meme.make_meme(tmpPath, request.form['body'],
                          request.form['author'])
    os.remove(tmpPath)
    return render_template('meme.html', path=path)


@app.after_request
def after_request(response):
    """ Prevent all browsers from caching. """
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


if __name__ == "__main__":
    app.run()
