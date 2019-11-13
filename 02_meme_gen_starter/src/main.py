import os
import random
import quote_engine as qe
import meme_generator as me
import sys
import argparse


def generate_meme(path=None, body=None, author=None):
    """ Generate a meme given an path and a quote """
    img = None
    quote = None

    if path is None:
        images = "./_data/photos/dog/"
        imgs = []
        for root, dirs, files in os.walk(images):
            imgs = [os.path.join(root, name) for name in files]

        img = random.choice(imgs)
    else:
        img = path
    if body is None:
        quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                       './_data/DogQuotes/DogQuotesDOCX.docx',
                       './_data/DogQuotes/DogQuotesPDF.pdf',
                       './_data/DogQuotes/DogQuotesCSV.csv']
        quotes = []
        for f in quote_files:
            quotes.extend(qe.Ingestor().parse(f))

        quote = random.choice(quotes)
    else:
        if author is None:
            raise Exception('Author Required if Body is Used')
        quote = qe.QuoteModel(body, author)

    meme = me.MemeEngine('./tmp')
    path = meme.make_meme(img, quote.body, quote.author)
    return path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""Generate memes using a
                                     picture, quote and and author.""")
    parser.add_argument('--path', help="""an image path. If no path is
                        specified, it will randomly select a dog picture.""")
    parser.add_argument('--body', help="""a string quote body. If no body is
                        specified it will randomly select a dog quote.""")
    parser.add_argument('--author', help="""a string quote author. If no author
                        is specified, it will randomly select a dog author.
                        \nNote! If you specified a body, an author is
                        required too. If you specified no body, the author will
                        be skipped.""")
    args = parser.parse_args()
    print(generate_meme(args.path, args.body, args.author))
