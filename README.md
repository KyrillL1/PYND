# Meme Generator
(This is a Udacity Code Review Project)

## Description
This project offers online and offline functionality for creating memes.
It includes default pictures and text, but can also be chosen manually.

## Setting up
Install all dependencies of requirements.txt.

## Running

### Run Offline Application

If you want to get a random meme, run the below.
```bash
python3 meme.py
```

If you want to have a customized one, run this.
```bash
python3 meme.py --path './myPicture.jpg' --author 'Confucius'
        --body 'Life is really simple, but we insist on making it complicated'
```

### Run Flask Server

You can run the flask server with
```bash
python3 app.py
```

Navigate to http://localhost:5000 and enjoy the application.
