from pymongo import MongoClient
from bson import ObjectId

def initialize_database ():
    client = MongoClient('mongodb:/localhost:27017')
    db = client['deli_argentina_db']

#Categories
    categories_data = [
        {"_id": {"$oid": "65e4ebc6d51a91baa0413c25"}, "name": "Appetizers"},
        {"_id": {"$oid": "65e4ebc6d51a91baa0413c26"}, "name": "Main Courses"},
        {"_id": {"$oid": "65e4ebc6d51a91baa0413c27"}, "name": "Desserts"},
        {"_id": {"$oid": "65e4ebc6d51a91baa0413c28"}, "name": "Holidays"},
        {"_id": {"$oid": "65e4ebc6d51a91baa0413c29"}, "name": "Vegetarian"}
    ]

#Recipes
    sample_recipes_data = [
        {
            "_id": ObjectId("65e4ed7ed51a91baa0413c2b"),
            "name": "Empanadas",
            "category": ObjectId("65e4ebc6d51a91baa0413c25"),
            "description": "Empanadas are savory turnovers filled with a variety of ingredients...",
            "ingredients": [
                "For the dough:",
                "3 cups all-purpose flour",
                # ... (other ingredients)
                "For sealing and brushing:",
                "1 egg, beaten (for egg wash)"
            ],
            "instructions": "Prepare the Dough:\n\nIn a large bowl, combine the flour and salt.\n..."
        },
        {
            "_id": ObjectId("65e4eee2d51a91baa0413c2c"),
            "name": "Provoleta",
            "category": ObjectId("65e4ebc6d51a91baa0413c25"),
            "description": "Provoleta is a popular melted cheese dish, usually made with provolone cheese...",
            "ingredients": [
                "1 round of Provolone cheese (about 8-10 ounces)",
                # ... (other ingredients)
                "Baguette slices or crusty bread, for serving"
            ],
            "instructions": "Preheat your oven to a high broil setting.\n\nPlace the provolone round in a cast-iron skillet..."
        },
        {
            "_id": ObjectId("65e71d40e1c2df54916560c5"),
            "name": "Humita en Chala (Corn Pudding in Corn Husks)",
            "category": ObjectId("65e4ebc6d51a91baa0413c25"),
            # ... (other fields)
            "instructions": "For the Filling:\r\n\r\nIn a large skillet, heat olive oil over medium heat..."
        },
        {
            "_id": ObjectId("65e7a72765e0bcbc6d3775e9"),
            "name": "El favorito de Ariel (Arroz con Atun)",
            "category": ObjectId("65e4ebc6d51a91baa0413c26"),
            # ... (other fields)
            "instructions": "Prepare the rice:\n\nIn a pot, add water and let it boil.\n..."
        }
    ]

#Adds categories if they don't exist
    
    for category_data in categories_data:
        if not db.categories.find_one({"name": category_data["name"]}):
            db.categories.insert_one(category_data)
            print(f"Category '{category_data['name']}' inserted successfully!")
#Adds recipes if they don't exist
            
    for recipe_data in sample_recipes_data:
        if not db.recipes.find_one({"name": recipe_data["name"]}):
            db.recipes.insert_one(recipe_data)
            print(f"Recipe '{recipe_data['name']}' inserted successfully!")             


if __name__ == "__main__":
    initialize_database()           