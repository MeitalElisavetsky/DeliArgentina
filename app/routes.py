# Import necessary libraries
from flask import render_template
from bson import ObjectId  # Import ObjectId for creating MongoDB ObjectId
from app import app, mongo
from flask import request, redirect, url_for, jsonify



@app.route('/get_category_id')
def get_category_id():
    category_name = request.args.get('name')
    category = mongo.db.categories.find_one({'name': category_name})
    if category:
        return str(category['_id'])
    else:
        return None



@app.route('/')
def home():
    categories = mongo.db.categories.find()
    return render_template('home.html', categories=categories)


# Your existing route for displaying recipes
@app.route('/recipe/<recipe_id>')
def recipe(recipe_id):
    recipe = mongo.db.recipes.aggregate([
        {
            "$match": {"_id": ObjectId(recipe_id)}
        },
        {
            "$lookup": {
                "from": "categories",
                "localField": "category",
                "foreignField": "_id",
                "as": "category_info"
            }
        },
        {
            "$unwind": "$category_info"
        },
        {
            "$project": {
                "_id": 1,
                "name": 1,
                "description": 1,
                "ingredients": 1,
                "instructions": 1,
                "category_name": "$category_info.name"
            }
        }
    ]).next()

    return render_template('recipe.html', recipe=recipe)

# New route for displaying categories
@app.route('/category/<category_name>')
def category(category_name):
    # Find the category by name
    category = mongo.db.categories.find_one({"name": category_name})

    if category:
        # Get the category ID
        category_id = category["_id"]

        # Fetch the recipes for the specified category
        recipes = mongo.db.recipes.find({"category": category_id})
        return render_template('category.html', category_name=category_name, recipes=recipes)

    return "Category not found"



# Updated route for inserting recipes only if they don't exist
@app.route('/insert_sample_data')
def insert_sample_data():

    # Define the sample recipe details
    sample_recipe_data = {
        "name": "Sample Recipe",
        "description": "A delicious dessert",
        "ingredients": ['Ingredient 1', 'Ingredient 2'],
        "instructions": 'Step 1, Step 2, ...'
    }

    # Check if the sample recipe exists before inserting
    if not mongo.db.recipes.find_one({"name": sample_recipe_data["name"]}):
        # Get category ID for Desserts category (adjust as needed)
        desserts_id = mongo.db.categories.find_one({"name": "Desserts"})["_id"]

        # Insert sample recipe
        sample_recipe_data["category"] = desserts_id
        mongo.db.recipes.insert_one(sample_recipe_data)

        return "Sample data inserted successfully!"

    return "Sample recipe already exists in the database."


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    # Customize this part based on your MongoDB setup
    # You might want to search for recipes based on the recipe name or other criteria
    # For example, you can use a case-insensitive search on the recipe name
    recipes = mongo.db.recipes.find({"name": {"$regex": query, "$options": "i"}})
    return render_template('search_results.html', query=query, recipes=recipes)


# Updated route for handling search suggestions
@app.route('/search_suggestions', methods=['POST'])
def search_suggestions():
    user_input = request.form.get('input', '')

    # Customize this part based on your MongoDB setup
    # For example, you can fetch recipe names from your MongoDB
    recipes = mongo.db.recipes.find({}, {'name': 1})
    suggestions = [recipe['name'] for recipe in recipes]

    # Filter suggestions based on user input
    filtered_suggestions = [suggestion for suggestion in suggestions if user_input.lower() in suggestion.lower()]

    return jsonify({'suggestions': filtered_suggestions})



#Add your fucking recipe
@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        name = request.form['name']
        category_id = request.form['category_id']
        ingredients = request.form['ingredients'].split('\r\n')
        instructions = request.form['instructions']
        description = request.form['description']

        # Validate inputs and insert into MongoDB
        if not any(char.isdigit() or char in "!@#$%^&" for char in name):
            mongo.db.recipes.insert_one({
                'name': name,
                'category': ObjectId(category_id),  # Convert category_id to ObjectId
                'description': description,
                'ingredients': ingredients,
                'instructions': instructions
            })

            # Return a JSON response indicating success
            return redirect(url_for('home'))

    # If the request is not a POST or the validation fails, render the add_recipe template
    categories = mongo.db.categories.find()
    return render_template('add_recipe.html', categories=categories)


