
import flask,json,hashlib
from models.user import User
from Requests import AdoptionRequest, save_request_to_json
from pathlib import Path
from flask import  redirect, request,session,jsonify
from pet import Pet
import os
from werkzeug.utils import secure_filename
from models.shelter import Shelter
from models.entity import Entity
from datetime import timedelta



app = flask.Flask("")
app.secret_key = "my-secret-123"
app.permanent_session_lifetime = timedelta(days=7)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}


def get_html2(page_name):
    html_file = open( "templates/"+ page_name + ".html")
    content = html_file.read()
    html_file.close()
    return content

def get_html(page_name):
    html_file = open( page_name + ".html")
    content = html_file.read()
    html_file.close()
    return content


def load_pets():
    petsdb=open("pets.json")
    pets=petsdb.read()
    petsdb.close()
    pets=json.loads(pets)
    return pets



def save_pets(pets):
    with open("pets.json", "w") as f:
        json.dump(pets, f, indent=2)



@app.route("/")
def homepage():
    pets = load_pets()
    html = get_html2("index")

    # Pet cards
    pets_html = ""
    for pet in pets:
        pets_html += f'''<div class="card" data-species="{pet['species']}">
            <img src="{pet['image_url']}" alt="{pet['name']}">
            <div class="card-content">
                <h3>{pet['name']}</h3>
                <p>{pet.get('about', 'No description available.')}</p>
            </div>
            <div class="status-badge">Available</div>
            <a href="/pet?id={pet['id']}" class="action-btn"> → </a>
        </div>'''

    html = html.replace("<!-- PETS_PLACEHOLDER -->", f'<div class="cards-containers">{pets_html}</div>')

    # Navbar links
    if "user_id" in session:
        navbar_links =''' 
        <a href="/my-requests">My Requests</a>
        <a href="/logout">Logout</a>
        '''
    else:
        navbar_links = '<a href="/signup">Sign Up</a><a href="/login">Login</a>'
    html = html.replace("<!-- NAVBAR_LINKS -->", navbar_links)

    return html


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        data = request.form

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        role = data.get("role")

        if not email or not password or not username:
            return "Please complete all fields.", 400

        if len(password) < 8:
            return "Password must be at least 8 characters.", 400

        if role == "shelter":
            shelter = Shelter(username, email, password)
            shelter.save()
        else:
            user = User(username, email, password)
            user.save()

        return redirect("/")

    return get_html2("signup")









@app.route('/login', methods=["GET", "POST"])
def login():
    if flask.request.method == "GET":
        return get_html2("login")  # Show the login form

    email = flask.request.form.get('email')
    password = flask.request.form.get('password')
    print(f"Received login request: {email}, {password}")

    if not email or not password:
        return flask.jsonify({"status": "fail", "message": "Missing email or password"}), 400

    with open('users.json', 'r') as f:
        users = json.load(f)

    with open('shelters.json', 'r') as f:
        shelters = json.load(f)

    user = next((u for u in users if u.get('email', '').lower() == email.lower()), None)
    if user and Entity.verify_password(password, user['password']):
        session.permanent = True
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["role"] = "user"
        return flask.jsonify({"status": "success", "role": "user", "id": user["id"], "name": user["username"]})

    shelter = next((s for s in shelters if s.get('email', '').lower() == email.lower()), None)
    if shelter and Entity.verify_password(password, shelter['password']):
        session.permanent = True
        session["shelter_id"] = shelter["id"]
        session["username"] = shelter["name"]
        session["role"] = "shelter"
        return flask.jsonify({"status": "success", "role": "shelter", "id": shelter["id"], "name": shelter["name"]})

    return flask.jsonify({"status": "fail", "message": "Invalid email or password"}), 401










@app.route('/logout')
def logout():
    session.clear()
    return redirect("/login")



@app.route("/pet")
def petDetails():
    pet_id = flask.request.args.get("id")
    if not pet_id:
        return "Pet ID not provided", 400

    pets = load_pets()
    pet = next((p for p in pets if str(p["id"]) == pet_id), None)

    if not pet:
        return "Pet not found", 404

    html = get_html("pet")
    html = html.replace("<!-- PET_NAME -->", pet["name"])
    html = html.replace("<!-- PET_IMAGE -->", pet["image_url"])
    html = html.replace("<!-- PET_SPECIES -->", pet["species"])
    html = html.replace("<!-- PET_AGE -->", str(pet["age"]))
    html = html.replace("<!-- PET_STATUS -->", "Adopted" if pet["adopted"] else "Available")
    html = html.replace("<!-- PET_ABOUT -->", pet.get("about", "No information available."))
    html = html.replace("<!-- PET_ID -->", str(pet["id"]))
    return html


@app.route("/adopt")
def adopt_form():
    pet_id = flask.request.args.get("id")
    pets = load_pets()
    pet = next((p for p in pets if str(p["id"]) == pet_id), None)

    if not pet:
        return "Pet not found", 404

    html = get_html("adopt")
    html = html.replace("<!-- PET_NAME -->", pet["name"])
    return html


    
@app.route("/dashboard")
def dashboard():
    shelter_id = session.get("shelter_id")
    print("Session shelter_id:", shelter_id)
    
    #  Debug print


    pets = load_pets()
    my_pets = [pet for pet in pets if pet.get("shelter_id") == shelter_id]

    html = get_html2("dashboard")
    pets_html = ""

    if not my_pets:
        pets_html = "<p style='text-align:center; margin-top:20px;'>No pets found for your shelter. Add one using the button above!</p>"
    else:
        for pet in my_pets:
            pets_html += f"""
            <div class="dashboard-card" id="pet-{pet['id']}">
                <h3>{pet['name']}</h3>
                <img src="{pet['image_url']}" alt="Pet image">
                <p>Species: {pet['species']}</p>
                <p>Age: {pet['age']}</p>
                <p>About: {pet.get('about', '')}</p>
                <p>Status: {'Adopted' if pet.get('adopted') else 'Available'}</p>

                <div class="dashboard-actions">
                    <a href="/edit_pet?id={pet['id']}" class="btn edit-btn">✏️ Edit</a>
                    <a href="/delete_pet?id={pet['id']}" class="btn delete-btn">🗑️ Delete</a>
                </div>
            </div>
            """

    html = html.replace("<!-- PETS_PLACEHOLDER -->", pets_html)
    return html





@app.route("/add-pet", methods=["GET", "POST"])
def add_pet():
    if flask.request.method == "POST":
        data = flask.request.form

        #  Handle uploaded image
        file = flask.request.files.get("image")
        if file and file.filename:
            filename = secure_filename(file.filename)
            file_path = os.path.join("static", "images", filename)
            file.save(file_path)
            image_url = "/" + file_path.replace("\\", "/")  # make it web-friendly
        else:
            image_url = "/static/images/default.jpg"  # fallback image

        #  Safe age conversion
        age_raw = data.get("age")
        if not age_raw or not age_raw.isdigit():
            return "Invalid age provided", 400
        age = int(age_raw)

        #  Get shelter ID from session
        shelter_id = 1
        if not shelter_id:
            return "You must be logged in as a shelter to add a pet", 403

        pets = load_pets()
        next_id = max((pet.get("id") or 0 for pet in pets), default=0) + 1        #  Create pet object
        pet = Pet(
            id=next_id,
            name=data.get("name"),
            species=data.get("species"),
            age=age,
            image_url=image_url,
            adopted=False,
            shelter_id=shelter_id,
            about=data.get("about", "")
        )

        #  Save
       
        pets.append(pet.to_dict())
        save_pets(pets)

        return redirect("/dashboard")

    return get_html("add_pet")

@app.route("/edit_pet", methods=["GET", "POST"])
def edit_pet():
    pets = load_pets()

    if flask.request.method == "GET":
        pet_id = int(flask.request.args.get("id"))
        pet = next((p for p in pets if p["id"] == pet_id), None)
        if not pet:
            return "Pet not found", 404

        html = get_html("edit_pet")  # Reads the raw HTML template

        adopted_options = """
            <option value="false" {avail}>Available</option>
            <option value="true" {adopted}>Adopted</option>
        """.format(
            avail="selected" if not pet["adopted"] else "",
            adopted="selected" if pet["adopted"] else ""
        )

        html = html.replace("__ID__", str(pet["id"]))
        html = html.replace("__NAME__", pet["name"])
        html = html.replace("__SPECIES__", pet["species"])
        html = html.replace("__AGE__", str(pet["age"]))
        html = html.replace("__ABOUT__", pet.get("about", ""))
        html = html.replace("__ADOPTED_OPTIONS__", adopted_options)

        return html

    elif flask.request.method == "POST":
        form = flask.request.form
        pet_id = int(form["id"])

        for pet in pets:
            if pet["id"] == pet_id:
                pet["name"] = form["name"]
                pet["species"] = form["species"]
                pet["age"] = int(form["age"])
                pet["about"] = form.get("about", "")
                pet["adopted"] = form.get("adopted") == "true"

                file = flask.request.files.get("image")
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    path = os.path.join("static", "images", filename)
                    file.save(path)
                    pet["image_url"] = "/" + path.replace("\\", "/")

                save_pets(pets)
                break

        return redirect("/dashboard")

@app.route("/delete_pet")
def delete_pet():
    pet_id = flask.request.args.get("id")

    if not pet_id:
        return "Pet ID is required", 400

    pets = load_pets()
    updated_pets = [pet for pet in pets if str(pet["id"]) != pet_id]

    save_pets(updated_pets)

    return redirect("/dashboard")


@app.route("/get-session-user")
def get_session_user():
    if "user_id" in session:
        return {"user_id": session["user_id"]}
    return {"user_id": None}

@app.route("/submit-adoption", methods=["POST"])
def submit_adoption():
    full_name = request.form.get("full_name")
    email = request.form.get("email")
    message = request.form.get("reason")
    pet_id = request.form.get("pet_id")  
    user_id = request.form.get("user_id")

    adoption_request = AdoptionRequest(
        user_id=user_id,
        pet_id=pet_id,
        email=email,
        message=message
    )

    save_request_to_json(adoption_request)
    return "Adoption request submitted!"

@app.route("/my-requests")
def my_requests():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")

    with open("requests.json") as f:
        requests_data = json.load(f)

    with open("pets.json") as f:
        pets_data = json.load(f)
        pets_dict = {str(pet["id"]): pet for pet in pets_data}

    my_requests = [r for r in requests_data if str(r["user_id"]) == str(user_id)]

    cards_html = ""
    for r in my_requests:
        pet = pets_dict.get(str(r["pet_id"]), {"name": "Unknown", "species": "", "image_url": ""})
        status = r.get("status", "Pending")
        cards_html += f"""
        <div class="request-card">
            <h3>{pet['name']} ({pet['species']})</h3>
            <img src="{pet.get('image_url', '')}" alt="Pet image" />
            <p><strong>Message:</strong> {r['message']}</p>
            <p><strong>Date:</strong> {r['timestamp'].split('T')[0]}</p>
            <p>Status: <span class="status {status}">{status}</span></p>
        </div>
        """

    html = get_html2("requests")  # Load the HTML template
    html = html.replace("<!-- REQUEST_CARDS_PLACEHOLDER -->", cards_html)
    return html




