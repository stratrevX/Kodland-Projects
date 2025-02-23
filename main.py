from flask import Flask
import string
app = Flask(__name__)

@app.route('/')
def home_page():
    return ' <a href="/random_key">Click for a random key.</a>'

@app.route('/random_fact')
def random_fact():
    import random
    facts = [
        'More than 50% realized their dependence on social medias in 2018',
        'The first computer virus was created in 1983',
        'The first computer mouse was created in 1964',
        'The first computer was created in 1943',
    ]
    return random.choice(facts)

@app.route('/random_key')
def random_key():
    return '<p>Your random key is: ' + key_generator() + '</p>'

def key_generator():
    import random
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation
    key = ''.join(random.choices(chars, k = 16))
    return key

app.run(debug = True)