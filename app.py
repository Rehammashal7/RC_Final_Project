
import flask,json,hashlib
app = flask.Flask("")
from pathlib import Path
from flask import  redirect, request

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
        return redirect('/')
    else:
        print(f"Login success for: {email}")
        return get_html("login")


@app.route("/")
def homepage():
    pets = load_pets()
    html = get_html("index")

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
    return html

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

 