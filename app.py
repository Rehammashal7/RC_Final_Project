
import flask,json,hashlib
app = flask.Flask("")
from pathlib import Path
from flask import  redirect, request,session
from pet import Pet
import os
import uuid
import flask
from werkzeug.utils import secure_filename
app.secret_key = os.urandom(24)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

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

def get_next_user_id(users):
    if not users:
        return 1
    return max(user["id"] for user in users) + 1

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def NewUser(email, password):
    hashed = hash_password(password)
    
    file_path = Path("users.json")
    
    # If file doesn't exist, create an empty one
    if not file_path.exists():
        with open(file_path, "w") as f:
            json.dump([], f)

    # Load existing users
    with open(file_path, "r") as f:
        try:
            users = json.load(f)
        except json.JSONDecodeError:
            users = []

    # Check for duplicate emails
    for user in users:
        if user["email"] == email:
            return {"success": False, "message": "Email already exists"}

    # Generate next user ID
    next_id = max((user.get("id", 0) for user in users), default=0) + 1

    # Add new user with ID
    user_data = {
        "id": next_id,
        "email": email,
        "password": hashed
    }

    users.append(user_data)

    # Save updated user list
    with open(file_path, "w") as f:
        json.dump(users, f, indent=2)

    return {"success": True, "message": "User registered successfully"}


def save_pets(pets):
    with open("pets.json", "w") as f:
        json.dump(pets, f, indent=2)





@app.route("/signup", methods=["GET", "POST"])
def signup():
    if flask.request.method == "POST":
        print("Form submitted!")  # Basic check
        print("Form data:", flask.request.form)  # Show all form data
        data = flask.request.form
        data = flask.request.form
        email = data.get("email")  # Changed from "name" to "username"
        password = data.get("password")
      #  confirm_password = data.get("confirm_password")

        # Debug print statement - add this line
        print(f"Received signup request: {email}, {password}")

        # Validate inputs
        if not email or not password:
            return "Please enter both username and password", 400
            
        
        result = NewUser(email, password)
        if result["success"]:
            return redirect('/')
        else:
            return result["message"], 400
    else:
        return get_html("signup")




@app.route('/login', methods=["GET", "POST"])
def login():
    if flask.request.method == "GET":
        return get_html("login")  # Show the login form

    email = flask.request.form.get('email')
    password = flask.request.form.get('password')
    print(f"Received signup request: {email}, {password}")
    with open('users.json', 'r') as f:
        users = json.load(f)

    # Find user by email (case-insensitive)
    user = next((u for u in users if u.get('email', '').lower() == email.lower()), None)

    if not user:
        return get_html("login")

    if hash_password(password) == user['password']:
        print(f"Login success for: {email}")
        #   # or use redirect(url_for("homepage"))
        session["user_id"] = user["id"]
        session["username"] = user["name"]
        return redirect('/')
    else:
        print(f"Login success for: {email}")
        return get_html("login")




@app.route("/")
def homepage():
    pets = load_pets()
    html = get_html("index")

    # Pet cards
    pets_html = ""
    for pet in pets:
        pets_html += f"""
        <div class="card">
            <img src="{pet['image_url']}" alt="{pet['name']}">
            <div class="card-content">
                <h3>{pet['name']}</h3>
                <p>{pet.get('description', 'No description available.')}</p>
            </div>
            <div class="status-badge">Available</div>
            <a href="/pet?id={pet['id']}" class="action-btn"> → </a>
        </div>
        """
    html = html.replace("<!-- PETS_PLACEHOLDER -->", f'<div class="cards-containers">{pets_html}</div>')

    # Navbar links
    if "user_id" in session:
        navbar_links = '<a href="/logout">Logout</a>'
    else:
        navbar_links = '<a href="/signup">Sign Up</a><a href="/login">Login</a>'
    html = html.replace("<!-- NAVBAR_LINKS -->", navbar_links)

    return html


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect("/")


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

@app.route("/shelter-signup", methods=["GET", "POST"])
def shelter_signup():
    if flask.request.method == "POST":
        data = flask.request.form
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return "Please enter both email and password", 400

        

        file_path = Path("shelters.json")
        if not file_path.exists():
            file_path.write_text("[]")

        with open(file_path, "r") as f:
            try:
                shelters = json.load(f)
            except json.JSONDecodeError:
                shelters = []

        # Check if email already exists
        for s in shelters:
            if s["email"] == email:
                return "Shelter already registered", 400

        # Assign unique ID
        next_id = max((s.get("id", 0) for s in shelters), default=0) + 1

        new_shelter = {
            "id": next_id,
            "email": email,
            "password": password
        }

        shelters.append(new_shelter)
        with open(file_path, "w") as f:
            json.dump(shelters, f, indent=2)

        # Store shelter session
        flask.session["shelter_id"] = next_id
        return redirect("shelter-dashboard")

    return get_html("shelter-signup")
@app.route("/dashboard")
def dashboard():
    shelter_id = 1  # later: get from session
    pets = load_pets()
    my_pets = [pet for pet in pets if pet.get("shelter_id") == shelter_id]

    html = get_html("dashboard")
    pets_html = ""

    for pet in my_pets:
        pets_html += f"""
        <div class="dashboard-card" id="pet-{pet['id']}">
            <h3>{pet['name']}</h3>
            <img src="{pet['image_url']}" alt="Pet image">
            <p>Species: {pet['species']}</p>
            <p>Age: {pet['age']}</p>
            <p>About: {pet.get('about', '')}</p>
            <p>Status: {'Adopted' if pet['adopted'] else 'Available'}</p>

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


