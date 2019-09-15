from flask import Flask, render_template
from model import PokeClient
app = Flask(__name__)

poke_client = PokeClient()

@app.route('/')
def index():
    return render_template('index.html')

@app.route()
def pokemon_info(name):
    """
    Must show all the info for a pokemon identified by name

    Check the README for more detail
    """
    pass

@app.route()
def pokemon_with_ability(ability):
    """
    Must show a list of pokemon 

    Check the README for more detail
    """
    pass
