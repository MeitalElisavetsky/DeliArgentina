from flask import Flask, render_template
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

# Connection to MongoDB
client = MongoClient('mongodb://localhost:27017/')  # Update connection string if necessary
db = client['DeliArgentina']  # Use the name of your database
categories_collection = db['categories']
recipes_collection = db['recipes']

# Custom Jinja filter to convert ObjectId to string
@app.template_filter('str')
def stringify(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    return obj

# Test data
categories_data = [
    {"Category_name": "Apetizers"},
    {"Category_name": "Main Courses"},
    {"Category_name": "Desserts"},
    {"Category_name": "Holiday Favorites"},
    {"Category_name": "Vegetarian"},
]

# Insert categories if they don't exist
for category in categories_data:
    existing_category = categories_collection.find_one({"Category_name": category["Category_name"]})
    if not existing_category:
        categories_collection.insert_one(category)

recipes_data = [
    {"Recipe_name": "Empanadas", "Category_name": "Apetizers", "Description": "Delicious empanadas...", "Ingredients_needed": ["...", "..."], "Instructions": "...", "Picture": "empanadas.jpg"},
    {"Recipe_name": "Dulce de Leche", "Category_name": "Desserts", "Description": "Traditional Argentine sweet...", "Ingredients_needed": ["...", "..."], "Instructions": "...", "Picture": "dulce_de_leche.jpg"},
    # Add more recipes if needed
]

# Insert recipes if they don't exist
for recipe in recipes_data:
    existing_recipe = recipes_collection.find_one({"Recipe_name": recipe["Recipe_name"]})
    if not existing_recipe:
        recipes_collection.insert_one(recipe)

# Routes
@app.route('/')
def index():
    categories = categories_collection.find()
    return render_template('index.html', categories=categories)

@app.route('/categories')
def category_list():
    categories = categories_collection.find({}, {'_id': 0, 'Category_name': 1})
    return render_template('categories.html', categories=categories)

# Routes
# Routes
@app.route('/category/<category_name>')
def category(category_name):
    # Convert category_name to lowercase to match the stored data
    lowercase_category_name = category_name.lower()
    
    # Fetch recipes based on the selected category
    recipes = recipes_collection.find({'Category_name': lowercase_category_name})
    
    # Debugging: print the recipes to the console
    print(f"Category Name: {lowercase_category_name}")
    print("Recipes:")
    for recipe in recipes:
        print(recipe)
    
    # Debugging: check if recipes are empty
    num_recipes = recipes.count_documents({})
    print(f"Number of recipes: {num_recipes}")
    
    return render_template('category.html', category_name=category_name, recipes=recipes)


@app.route('/recipe/<recipe_id>')
def recipe(recipe_id):
    recipe = recipes_collection.find_one({'_id': ObjectId(recipe_id)})
    return render_template('recipe.html', recipe=recipe)

if __name__ == '__main__':
    app.run(debug=True)
