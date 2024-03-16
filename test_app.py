import pytest
from pymongo import MongoClient
from app import app, db
import os


@pytest.fixture(scope='session')
def test_app():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(scope='session')
def test_db():
    # Create a separate testing database
    mongodb_uri = os.getenv('MONGO_URI', 'mongodb://mongodb@mongodb:27017/')

    client = MongoClient(mongodb_uri)

    test_db = client['test_deli_argentina_db']
    
    # Use the testing database for the tests
    app.config['DB'] = test_db

    # Perform any setup needed for the testing database
    categories = test_db['categories']
    recipes = test_db['recipes']

    # Add test data if needed
    # For example:
    # categories.insert_one({"name": "Test Category"})

    yield test_db

    # Teardown: Clean up the testing database after tests
    test_db.client.drop_database(test_db)


def test_category_page(test_app):
    # Test accessing the category page
    response = test_app.get('/category/Appetizers')
    assert response.status_code == 200
    assert b'Appetizers' in response.data


def test_search(test_app):
    # Test searching for recipes
    response = test_app.get('/search?query=Empanadas')
    assert response.status_code == 200
    assert b'Empanadas' in response.data


def test_add_recipe_page(test_app):
    # Test accessing the add recipe page
    response = test_app.get('/add_recipe')
    assert response.status_code == 200
    assert b'Add Recipe' in response.data


def test_add_recipe(test_app, test_db):
    response = test_app.get('/add_recipe')
    assert response.status_code == 200
    assert b'Add Recipe' in response.data
    # Test adding a recipe
    data = {
        'name': 'Test Recipe',
        'category_id': '65e4ebc6d51a91baa0413c25',  # ID of an existing category
        'description': 'Test Description',
        'ingredients': 'Ingredient 1\r\nIngredient 2',
        'instructions': 'Test Instructions'
    }
    response = test_app.post('/add_recipe', data=data)
    assert response.status_code == 302  # Redirects to home page after successful addition

    # Verify that the new recipe exists in the database
    new_recipe = db.recipes.find_one({'name': 'Test Recipe'})
    assert new_recipe is not None

    # Teardown: Remove the test recipe from the database
    db.recipes.delete_many({'name': 'Test Recipe'})


def test_invalid_recipe_name(test_app):
    # Test adding a recipe with an invalid name
    data = {
        'name': 'Test Recipe!',
        'category_id': '65e4ebc6d51a91baa0413c25',  # ID of an existing category
        'description': 'Test Description',
        'ingredients': 'Ingredient 1\r\nIngredient 2',
        'instructions': 'Test Instructions'
    }
    response = test_app.post('/add_recipe', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b'No numbers or special characters allowed' in response.data
