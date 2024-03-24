from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from bson import ObjectId
from pymongo import MongoClient
from datetime import datetime
import os
import bcrypt
from db import *


app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Connect to MongoDB
mongodb_uri = os.getenv('MONGO_URI', 'mongodb://root:root@mongodb:27017/')

client = MongoClient(mongodb_uri)

db = client['deli_argentina_db']

categories = db['categories']

recipes = db['recipes']

users = db['users']




#Add sample data
if categories.count_documents({}) == 0:
    # Categories
    categories = [
        {"name": "Appetizers", "_id": ObjectId("65e4ebc6d51a91baa0413c25")},
        {"name": "Main Courses", "_id": ObjectId("65e4ebc6d51a91baa0413c26")},
        {"name": "Desserts", "_id": ObjectId("65e4ebc6d51a91baa0413c27")},
        {"name": "Holidays", "_id": ObjectId("65e4ebc6d51a91baa0413c28")},
        {"name": "Vegetarian", "_id": ObjectId("65e4ebc6d51a91baa0413c29")}
    ]

    insert_categories = db.categories.insert_many(categories)

    # Recipes
if recipes.count_documents({}) == 0:
    recipes = [
        {
            "_id": ObjectId("65e4ed7ed51a91baa0413c2b"),
            "name": "Empanadas",
            "category": ObjectId("65e4ebc6d51a91baa0413c25"),
            "description": "Empanadas are savory turnovers filled with a variety of ingredients...",
            "ingredients": [
                "For the dough:",
                "3 cups all-purpose flour",
                "1/2 cup unsalted butter, chilled and diced",
                "1/2 cup lard or shortening, chilled and diced",
                "1 teaspoon salt",
                "1/2 - 3/4 cup cold water",
                "For the filling:",
                "1 pound ground beef",
                "1 large onion, finely chopped",
                "2 hard-boiled eggs, chopped",
                "1/2 cup green olives, pitted and chopped",
                "2 tablespoons raisins (optional)",
                "2 teaspoons ground cumin",
                "1 teaspoon paprika",
                "Salt and pepper, to taste",
                "For sealing and brushing:",
                "1 egg, beaten (for egg wash)"
            ],
            "instructions": "Prepare the Dough:\n\nIn a large bowl, combine the flour and salt...\nEnjoy your homemade Argentine beef empanadas!",
            "added_by": "meityARG",
            "date_added": "21/08/2022"
        },
        {
            "_id": ObjectId("65e4eee2d51a91baa0413c2c"),
            "name": "Provoleta",
            "category": ObjectId("65e4ebc6d51a91baa0413c25"),
            "description": "Provoleta is a popular melted cheese dish, usually made with provolone cheese...",
            "ingredients": [
                "1 round of Provolone cheese (about 8-10 ounces)",
                "1 tablespoon olive oil",
                "1 teaspoon dried oregano",
                "1 teaspoon red pepper flakes (optional, for some heat)",
                "2 cloves garlic, minced",
                "Freshly ground black pepper, to taste",
                "Baguette slices or crusty bread, for serving"
            ],
            "instructions": "Preheat your oven to a high broil setting.\n\nPlace the provolone round in a cast-iron skillet or an ovenproof dish...\nServe the Provoleta immediately while it's hot, with slices of baguette or crusty bread for dipping.",
            "added_by": "meityARG",
            "date_added": "21/08/2022"
        },
        {
            "_id": ObjectId("65e71d40e1c2df54916560c5"),
            "name": "Humita en Chala (Corn Pudding in Corn Husks)",
            "category": ObjectId("65e4ebc6d51a91baa0413c25"),
            "description": "Humita en Chala is a traditional Argentinean appetizer that showcases the country's love for corn...",
            "ingredients": [
                "4 cups fresh corn kernels (about 6-8 ears)",
                "1 onion, finely chopped",
                "1 red bell pepper, finely diced",
                "2 tablespoons olive oil",
                "1 teaspoon paprika",
                "1 teaspoon cumin",
                "Salt and pepper to taste",
                "1/2 cup milk",
                "1/2 cup grated Parmesan cheese",
                "1/4 cup fresh basil, chopped",
                "For the Corn Husks:",
                "Dried corn husks, soaked in warm water for about 1 hour"
            ],
            "instructions": "For the Filling:\r\n\r\nIn a large skillet, heat olive oil over medium heat. Add chopped onions and red bell pepper, cooking until softened...\nHumita en Chala is a delightful appetizer that captures the essence of Argentinean cuisine with its rich corn flavor and aromatic spices...",
            "added_by": "meityARG",
            "date_added": "21/08/2022"
        },
        {
            "_id": ObjectId("65e7a72765e0bcbc6d3775e9"),
            "name": "El favorito de Ariel (Arroz con Atun)",
            "category": ObjectId("65e4ebc6d51a91baa0413c26"),
            "description": "Ariel's favorite dish, the easiest one to make but the hardest to master for him to love it...",
            "ingredients": [
                "A kilo of rice",
                "A can of tuna",
                "Two spoons of mayonnaise",
                "Half a lemon's juice"
            ],
            "instructions": "Prepare the rice:\n\nIn a pot, add water and let it boil...\nServe:\n\nFirst of all open your tuna and let the oil/water drain a bit, after that add your tuna to a bowl, a can of tuna, mayonnaise and half a lemon's juice, stir and enjoy! (You can even add boiled eggs but Ariel doesn't like it much)",
            "added_by": "meityARG",
            "date_added": "06/03/2022"
        }
    ]

    insert_recipes = db.recipes.insert_many(recipes)

#Sign up route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # This function will check if the user exists in the database
        if get_user_by_username(username):
            return render_template('signup.html', error='Username already exists')
        
        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user_data = {'username': username, 'password': hashed_password}

        try:
            db.users.insert_one(user_data)
            return redirect(url_for('login'))
        except Exception as e:
            print(e)
            return render_template('signup.html', error='Error creating user')
    return render_template('signup.html')


#Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = get_user_by_username(username)

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')  # This line is now correctly indented

    
#User Logout
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


# Home page
@app.route('/')
def home():
    categories = db.categories.find()
    if 'username' in session:
        return render_template('home.html', categories=categories)
    else:
        return render_template('home.html', categories=categories, show_login=True)  # Render the login option



# Displaying recipes
@app.route('/recipe/<recipe_id>')
def recipe(recipe_id):
    # Call the function from db.py to get recipe details
    recipe = get_recipe_by_id(recipe_id)

    return render_template('recipe.html', recipe=recipe)


# Display categories
@app.route('/category/<category_name>')
def category(category_name):
    # Call the function from db.py to get category and recipes
    category, recipes = get_category_and_recipes(category_name)

    if category:
        return render_template('category.html', category_name=category_name, recipes=recipes)
    else:
        return "Category not found"


#Search Bar function
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').lower()

    if not query.strip():
        return redirect(url_for('home'))

    # Call the function from db.py to search for recipes
    matching_recipes = search_recipes(query)

    if not matching_recipes:
        return render_template('no_results.html', query=query)
    else:
        return render_template('search_results.html', query=query, recipes=matching_recipes)


#Add your recipe
@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if 'username' not in session:
        flash('You need to sign in first to add a recipe.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        category_id = request.form['category_id']
        ingredients = request.form['ingredients'].split('\r\n')
        instructions = request.form['instructions']
        description = request.form['description']
        added_by = session['username']

        date_added = datetime.now().strftime("%d/%m/%Y")


        # Call the function from db.py to add the recipe
        success, message = db_add_recipe(name, category_id, description, ingredients, instructions, added_by, date_added)

        if success:
            return redirect(url_for('home'))
        else:
            return render_template('add_recipe.html', error=message)

    # If the request is not a POST, render the add_recipe template
    categories = db.categories.find()
    return render_template('add_recipe.html', categories=categories)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

