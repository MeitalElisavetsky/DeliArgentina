from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from flask import request
from bson import ObjectId
import bcrypt
import os

# Connect to MongoDB
mongodb_uri = os.getenv('MONGO_URI', 'mongodb://root:root@mongodb:27017/')

client = MongoClient(mongodb_uri)

db = client['deli_argentina_db']

categories = db['categories']

recipes = db['recipes']

users = db['users']




users.create_index([('username', 1)], unique=True)


# Function to add a new user with hashed password
def add_user(username, password):
    user_data = {'username': username, 'password': password}
    try:
        users.insert_one(user_data)
        return True  # Return True if user is added successfully
    except DuplicateKeyError:
        # Handle exception if username is not unique
        return False

# Function to retrieve a user by username
def get_user_by_username(username):
    return users.find_one({'username': username}, {'password': 1})


def get_category_id():
    category_name = request.args.get('name')
    category = db.categories.find_one({'name': category_name})
    if category:
        return str(category['_id'])
    else:
        return None
    

def get_recipe_by_id(recipe_id):
    # Perform aggregation to get recipe details including category name
    recipe = db.recipes.aggregate([
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

    return recipe


def get_category_and_recipes(category_name):
    # Find the category by name
    category = db.categories.find_one({"name": category_name})

    if category:
        # Get the category ID
        category_id = category["_id"]

        # Fetch the recipes for the specified category
        recipes = db.recipes.find({"category": category_id})
        return category, recipes

    return None, None

def search_recipes(query):
    # Use a case-insensitive regex to find recipes containing the query as a substring
    regex_pattern = f".*{query}.*"
    recipes_cursor = db.recipes.find({"name": {"$regex": regex_pattern, "$options": "i"}})

    # Extract matching recipes
    matching_recipes = [recipe for recipe in recipes_cursor if query in recipe["name"].lower()]

    return matching_recipes


def get_recipe_names():
    # Retrieve recipe names from the database
    recipes = db.recipes.find({}, {'name': 1})
    recipe_names = [recipe['name'] for recipe in recipes]
    return recipe_names


def db_add_recipe(name, category_id, description, ingredients, instructions):
    # Validate inputs
    if any(char in "!@#$%^&*" for char in name):
        return False, "Recipe name cannot contain special characters"

    # Insert into MongoDB
    db.recipes.insert_one({
        'name': name,
        'category': ObjectId(category_id),
        'description': description,
        'ingredients': ingredients,
        'instructions': instructions
    })

    return True, "Recipe added successfully"