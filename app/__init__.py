from flask import Flask
from flask_pymongo import PyMongo
from bson import ObjectId
import os
from pymongo import MongoClient


app = Flask(__name__, static_url_path='/static')

app.config['MONGO_URI'] = "mongodb://mongodb:27017/deli_argentina_db"

mongo = PyMongo(app)

def initialize_database():
    # Categories
    categories = [
        {"name": "Appetizers", "_id": ObjectId("65e4ebc6d51a91baa0413c25")},
        {"name": "Main Courses", "_id": ObjectId("65e4ebc6d51a91baa0413c26")},
        {"name": "Desserts", "_id": ObjectId("65e4ebc6d51a91baa0413c27")},
        {"name": "Holidays", "_id": ObjectId("65e4ebc6d51a91baa0413c28")},
        {"name": "Vegetarian", "_id": ObjectId("65e4ebc6d51a91baa0413c29")}
    ]

    # Recipes
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
            "instructions": "Prepare the Dough:\n\nIn a large bowl, combine the flour and salt...\nEnjoy your homemade Argentine beef empanadas!"
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
            "instructions": "Preheat your oven to a high broil setting.\n\nPlace the provolone round in a cast-iron skillet or an ovenproof dish...\nServe the Provoleta immediately while it's hot, with slices of baguette or crusty bread for dipping."
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
            "instructions": "For the Filling:\r\n\r\nIn a large skillet, heat olive oil over medium heat. Add chopped onions and red bell pepper, cooking until softened...\nHumita en Chala is a delightful appetizer that captures the essence of Argentinean cuisine with its rich corn flavor and aromatic spices..."
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
            "instructions": "Prepare the rice:\n\nIn a pot, add water and let it boil...\nServe:\n\nFirst of all open your tuna and let the oil/water drain a bit, after that add your tuna to a bowl, a can of tuna, mayonnaise and half a lemon's juice, stir and enjoy! (You can even add boiled eggs but Ariel doesn't like it much)"
        }
    ]

    # Check if categories and recipes exist, create them if not
    for category in categories:
        existing_category = mongo.db.categories.find_one({"name": category["name"]})
        if not existing_category:
            mongo.db.categories.insert_one(category)

    for recipe in recipes:
        existing_recipe = mongo.db.recipes.find_one({"name": recipe["name"]})
        if not existing_recipe:
            mongo.db.recipes.insert_one(recipe)

# Initialize the database when the application starts
initialize_database()

from app import routes
