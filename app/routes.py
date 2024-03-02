# Import necessary libraries
from flask import render_template
from bson import ObjectId  # Import ObjectId for creating MongoDB ObjectId
from app import app, mongo
from flask import request, redirect, url_for


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

