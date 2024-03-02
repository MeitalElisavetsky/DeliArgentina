from app import app, mongo  # Import the 'mongo' object from the 'app' package
from bson import ObjectId  # Import ObjectId for creating MongoDB ObjectId

# Insert categories
category_ids = []
category_ids.append(mongo.db.categories.insert_one({ "name": "Appetizers" }).inserted_id)
category_ids.append(mongo.db.categories.insert_one({ "name": "Main Courses" }).inserted_id)
category_ids.append(mongo.db.categories.insert_one({ "name": "Desserts" }).inserted_id)
category_ids.append(mongo.db.categories.insert_one({ "name": "Holidays" }).inserted_id)
category_ids.append(mongo.db.categories.insert_one({ "name": "Vegetarian" }).inserted_id)

# Insert recipes
mongo.db.recipes.insert_one({
    "name": "Sample Recipe",
    "category": category_ids[2],  # Use the ID of the "Desserts" category
    "description": "A delicious dessert",
    "ingredients": ['Ingredient 1', 'Ingredient 2'],
    "instructions": 'Step 1, Step 2, ...'
})

if __name__ == '__main__':
    app.run(debug=True)
