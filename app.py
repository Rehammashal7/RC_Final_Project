
import flask,json,hashlib
app = flask.Flask("")
from pathlib import Path
from flask import  redirect

def get_html(page_name):
    html_file = open(page_name + ".html")
    content=html_file.read()
    html_file.close()
    return content


def load_pets():
    petsdb=open("pets.json")
    pets=petsdb.read()
    petsdb.close()
    pets=json.loads(pets)
    return pets




@app.route("/")
def homepage():
    pets = load_pets()
    html = get_html("index")

    # Build the HTML block for pets
    pets_html = ""
    for pet in pets:
        pets_html += f"""
        <div class="pet">
            <h2>{pet['name']}</h2>
            <img src="{pet['image_url']}" alt="{pet['name']}" width="150">
        </div>
        """

    # Replace a placeholder in the HTML file
    html = html.replace("<!-- PETS_PLACEHOLDER -->", pets_html)
    return html



