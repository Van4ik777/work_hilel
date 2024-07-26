import string
from random import random
import pandas as pd

from flask import Flask

app = Flask(__name__)

@app.route("/generate_password")
def generate_password():
    """
    from 10 to 20 chars
    upper and lower case
    """
    # string
    # ascii_lowercase
    # ascii_uppercase
    # int
    # special symbols
    # return password
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    digits = string.digits
    special_chars = string.punctuation
    password = ''.join(random.choice(lower) + random.choice(upper) + random.choice(digits) + random.choice(special_chars) for _ in range(random.randint(10, 20)))

    return f'<h1>{password}</h1>'

@app.route("/calculate_average")
def calculate_average():
    """
    csv file with students
    1.calculate average high
    2.calculate average weight
    csv - use lib
    *pandas - use pandas for calculating
    """
    file = pd.read_csv('hw.csv')
    height = file['Height(Inches)'].mean()
    weight = file['Weight(Pounds)'].mean()

    return f'<h1>{height} {weight}</h1>'

if __name__ == '__main__':
    app.run(
        port=5000, debug=True
    )