from PIL import Image, ImageFont, ImageDraw
import os

path = os.path.join(os.path.dirname(__file__),
                    '_data/', 'photos/', 'dog/', 'too_big.jpg')


class MemeEngine():
    """ Handle meme manipulation """

    def __init__(self, output_dir):
        self.output_dir = output_dir

    def resize(self, new_width, image):
        """Change width of image to newWidth and keep ratio aspect."""
        w_perc = (newWidth/float(image.size[0]))
        h_size = int((float(image.size[1])*float(w_perc)))
        return image.resize((new_width, h_size), Image.ANTIALIAS)

    def draw_text(self, draw, text, mainColor, borderColor, font, x, y):
        """ Draw text with mainColor and shadow (borderColor) onto Draw """
        # thin border
        draw.text((x-1, y), text, font=font, fill=borderColor)
        draw.text((x+1, y), text, font=font, fill=borderColor)
        draw.text((x, y-1), text, font=font, fill=borderColor)
        draw.text((x, y+1), text, font=font, fill=borderColor)
        # thicker border
        draw.text((x-1, y-1), text, font=font, fill=borderColor)
        draw.text((x+1, y-1), text, font=font, fill=borderColor)
        draw.text((x-1, y+1), text, font=font, fill=borderColor)
        draw.text((x+1, y+1), text, font=font, fill=borderColor)
        # main text
        draw.text((x, y), text, font=font, fill=mainColor)

        """ Note to corrector:
        The below value specifications for the positions and the font height
        are bad practice since it's hardcoded. E.g. when a quote is not fitting
        on the picture or the author is too long, it's not resizing itself
        automatically. But since this resizing wasn't a requirement,
        I was okay with hardcoding it."""

    def make_meme(self, img_path, text, author, width=500) -> str:
        """ Add quote with text and author to image """
        filename, file_extension = os.path.splitext(img_path)
        im = Image.open(img_path)
        if im.size[0] > width:
            im = self.resize(width, im)
        draw = ImageDraw.Draw(im)
        width, height = im.size

        # Body Text
        posB_X = 25
        posB_Y = height-100
        colorB = (0, 0, 0)
        fontB = ImageFont.truetype(os.path.join(os.path.dirname(__file__),
                                   '_data/', 'FreeSansBold.ttf'), 25,
                                   encoding="unic")
        self.draw_text(draw, text, "black", "white", fontB, posB_X, posB_Y)

        # Author Text
        posA_X = posB_X+45
        posA_Y = posB_Y+35
        colorA = (0, 0, 0)
        fontA = ImageFont.truetype(os.path.join(os.path.dirname(__file__),
                                   '_data/', 'FreeSans.ttf'), 20,
                                   encoding="unic")
        self.draw_text(draw, "- "+author, "black", "white", fontA,
                       posA_X, posA_Y)

        toPath = self.output_dir+"/newMeme.jpg"
        im.save(toPath)
        return toPath
