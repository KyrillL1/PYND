# Meme Engine

## Classes
MemeEngine(locationToSave) where locationToSave is the location to save all
new created memes.

## Description
The Directory takes a path to a picture, a quote text and a quote author as input
and generates a Meme out of it.

## Dependencies
PIL, os

## Example Usage

```python
import meme_engine as me
myMemeEngine = me.MemeEngine("./tmp")
myMemeEngine.make_meme("./coolPic.jpg", "What else would he say?", "Great Arthur")
```

or

```python
import meme_engine as me
myMemeEngine = me.MemeEngine("./temp")
myMemeEngine.make_meme("./anotherPicture.png", "Life is really simple, "+
                       "but we insist on making it complicated", "Confucius")
```
