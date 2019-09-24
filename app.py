from flask import Flask, request
from flask_pymongo import PyMongo
from bson.json_util import dumps

# Set up the Flask 'app' variable
app = Flask(__name__)

# Tell Flask how to find our database
app.config['MONGO_URI'] = 'mongodb://localhost:27017/test_db'
mongo = PyMongo(app)
db = mongo.db

@app.route('/users', methods=['GET'])
def get_all_users():
    """Display all users in JSON form."""
    # Find all users
    users_list = db.users.find({})

    # Make JSON containing list of all users (for easier use in HTML)
    users_json = dumps(users_list)

    # Render some HTML containing the list of all users
    return """
    <a href="/new_user">New User</a>
    <br><br>
    <a href="/delete_user">Delete User</a>
    <br><br>
    <a href="/delete_all">Delete All Users</a>
    <br><br>
    <a href="/update_user">Update User</a>
    <br><br>
    Users: {}
    """.format(users_json)


@app.route('/delete_user')
def delete_user_form():
    """Display an HTML form for user deletion."""

    return """
    <form action='/delete_user' method='POST'>
        Username: <input name='delete_username' type='text'/>
        <button type='submit'>Delete</button>
    </form>
    """

@app.route('/delete_all')
def delete_all_user_confirmation():
    """Display an HTML form for user deletion."""

    return """
    <form action='/delete_all_users' method='POST'>
        <span>Do you want to delete all users?
        <button type='submit'>Delete All</button>
    </form>
    """

@app.route('/update_user')
def update_user_form():
    """Display an HTML form for user deletion."""

    return """
    <form action='/update_user' method='POST'>
        <span>username of user you want to update: </span>
        <input name='old_username' type='text'/>
        <br></br>
        <span>Update user with this information</span>
        Username: <input name='new_username' type='text'/>
        Password: <input name='new_password' type='password'/>
        Bio: <textarea name='new_bio'></textarea>
        <button type='submit'>Submit</button>
    </form>

    """

@app.route('/update_user', methods=['POST'])
def update_user():
    """update user."""

    # Make the new user JSON from form data
    old_user = {
      "username": request.form.get('old_username')
    }

    new_user = { "$set":{
        "username": request.form.get('new_username'),
        "password": request.form.get('new_password'),
        "bio": request.form.get('new_bio'),
        }
    }

    # Insert into PyMongo database
    db.users.update_one(old_user, new_user)

    # Render some HTML
    return """
    User updated successfully!
    <a href="/users">Back to Home</a>
    """

@app.route('/delete_user', methods=['POST'])
def delete_user():
    """Create a new user."""

    # Make the new user JSON from form data
    delete_user = {
      "username": request.form.get('delete_username')
    }

    # Insert into PyMongo database
    db.users.remove(delete_user)

    # Render some HTML
    return """
    User deleted successfully!
    <a href="/users">Back to Home</a>
    """

@app.route('/delete_all_users', methods=['POST'])
def delete_all():
    """delete all  user."""

    # Insert into PyMongo database
    db.users.delete_many({})

    # Render some HTML
    return """
    User deleted successfully!
    <a href="/users">Back to Home</a>
    """

@app.route('/new_user')
def new_user_form():
    """Display an HTML form for user creation."""

    return """
    <form action='/users' method='POST'>
        Username: <input name='username' type='text'/>
        Password: <input name='password' type='password'/>
        Bio: <textarea name='bio'></textarea>
        <button type='submit'>Submit</button>
    </form>
    """

@app.route('/users', methods=['POST'])
def create_user():
    """Create a new user."""

    # Make the new user JSON from form data
    new_user = {
      "username": request.form.get('username'),
      "password": request.form.get('password'),
      "bio": request.form.get('bio'),
    }

    # Insert into PyMongo database
    db.users.insert_one(new_user)

    # Render some HTML
    return """
    User created successfully!
    <a href="/users">Back to Home</a>
    """

if __name__ == '__main__':
    app.run(debug=True)
