# Import necessary libraries
from flask import render_template
from bson import ObjectId  # Import ObjectId for creating MongoDB ObjectId
from app import app, mongo


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
    # You need to fetch the recipes for the specified category and pass them to the template
    recipes = mongo.db.recipes.find({"category_info.name": category_name})
    return render_template('category.html', category_name=category_name, recipes=recipes)

# Updated route for inserting categories and recipes
@app.route('/insert_sample_data')
def insert_sample_data():
    # Check if categories exist before inserting
    if not mongo.db.categories.find_one({"name": "Appetizers"}):
        mongo.db.categories.insert_one({"name": "Appetizers"})

    if not mongo.db.categories.find_one({"name": "Main Courses"}):
        mongo.db.categories.insert_one({"name": "Main Courses"})

    if not mongo.db.categories.find_one({"name": "Desserts"}):
        mongo.db.categories.insert_one({"name": "Desserts"})

    if not mongo.db.categories.find_one({"name": "Holidays"}):
        mongo.db.categories.insert_one({"name": "Holidays"})

    if not mongo.db.categories.find_one({"name": "Vegetarian"}):
        mongo.db.categories.insert_one({"name": "Vegetarian"})

    # Insert recipes only if they don't exist
    if not mongo.db.recipes.find_one({"name": "Sample Recipe"}):
        # Get category IDs
        appetizers_id = mongo.db.categories.find_one({"name": "Appetizers"})["_id"]
        desserts_id = mongo.db.categories.find_one({"name": "Desserts"})["_id"]

        # Insert sample recipe
        mongo.db.recipes.insert_one({
            "name": "Sample Recipe",
            "category": desserts_id,
            "description": "A delicious dessert",
            "ingredients": ['Ingredient 1', 'Ingredient 2'],
            "instructions": 'Step 1, Step 2, ...'
        })

    return "Sample data inserted successfully!"

