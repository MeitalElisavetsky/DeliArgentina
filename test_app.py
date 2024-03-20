import pytest
from pymongo import MongoClient
from app import app, db
from bson import ObjectId
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
    users = test_db['users']

    yield test_db

    # Teardown: Clean up the testing database after tests
    test_db.client.drop_database(test_db)



def test_signup(test_app, test_db):
    # Test signing up with a new username
    response = test_app.post('/signup', data={'username': 'testuser', 'password': 'test'}, follow_redirects=True)

    assert response.status_code == 200  # Check if the signup was successful

    new_user = db.users.find_one({'username': 'testuser'})
    assert new_user is not None

def test_login(test_app, test_db):
    # Test logging in with correct credentials
    response = test_app.post('/login', data={'username': 'testuser', 'password': 'test'}, follow_redirects=True)
    assert response.status_code == 200



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

def test_add_recipe_logged_in(test_app, test_db):
    # Test adding a recipe
    data = {
        'name': 'Test Recipe',
        'category_id': '65e4ebc6d51a91baa0413c25',
        'description': 'Test Description',
        'ingredients': 'Ingredient 1\r\nIngredient 2',
        'instructions': 'Test Instructions'
    }

    # Send POST request to add the recipe
    response = test_app.post('/add_recipe', data=data, follow_redirects=True)
    assert response.status_code == 200  # Now it should follow redirect to home page

    # Verify that the new recipe exists in the database
    new_recipe = db.recipes.find_one({'name': 'Test Recipe'})
    assert new_recipe is not None

    db.recipes.delete_many({'name': 'Test Recipe'})
    db.users.delete_many({'username': 'testuser'})

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
