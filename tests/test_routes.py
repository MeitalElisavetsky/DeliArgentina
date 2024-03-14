import pytest
from flask import url_for
from app import app, mongo
from pymongo import MongoClient
import os

@pytest.fixture(scope='module')
def mongodb():
    test_mongodb_uri = os.getenv('TEST_MONGODB_URI', 'mongodb://mongodb:27017/test_deli_argentina_db')
    client = MongoClient(test_mongodb_uri, serverSelectionTimeoutMS=5000)
    test_db = client["test_deli_argentina_db"]
    yield test_db
    client.drop_database("test_deli_argentina_db")


@pytest.fixture
def client(mongodb):
    app.config['TESTING'] = True
    app.config['MONGO_URI'] = 'mongodb://mongodb:27017/test_deli_argentina_db'

    # Setup: Insert some sample data into the test database
    mongo.db.categories.insert_one({'name': 'Test Category'})
    mongo.db.recipes.insert_one({
        'name': 'Test Recipe',
        'category': mongo.db.categories.find_one({'name': 'Test Category'})['_id'],
        'description': 'Test Description',
        'ingredients': ['Ingredient 1', 'Ingredient 2'],
        'instructions': 'Step 1, Step 2, ...'
    })

    yield client

    # Teardown: Remove test data from the database
    mongo.db.categories.delete_many({'name': 'Test Category'})
    mongo.db.recipes.delete_many({'name': 'Test Recipe'})


def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'<!-- home.html -->' in response.data  # Adjust based on the actual content


def test_recipe_route(client):
    recipe_id = str(mongo.db.recipes.find_one({'name': 'Test Recipe'})['_id'])
    response = client.get(f'/recipe/{recipe_id}')
    assert response.status_code == 200
    assert b'Test Recipe' in response.data


def test_category_route(client):
    response = client.get('/category/Test%20Category')
    assert response.status_code == 200
    assert b'Test Category' in response.data


def test_add_recipe_route(client):
    response = client.get('/add_recipe')
    assert response.status_code == 200
    assert b'Add Recipe' in response.data

    # Test adding a new recipe
    data = {
        'name': 'New Recipe',
        'category_id': str(mongo.db.categories.find_one({'name': 'Test Category'})['_id']),
        'description': 'New Description',
        'ingredients': 'Ingredient 1\r\nIngredient 2',
        'instructions': 'New Instructions'
    }
    response = client.post('/add_recipe', data=data)
    assert response.status_code == 302  # Redirects to home page after successful addition

    # Verify that the new recipe exists in the database
    new_recipe = mongo.db.recipes.find_one({'name': 'New Recipe'})
    assert new_recipe is not None

    # Teardown: Remove the test recipe from the database
    mongo.db.recipes.delete_many({'name': 'New Recipe'})



def test_search_route(client):
    response = client.get('/search?query=Test')
    assert response.status_code == 200
    assert b'Test Recipe' in response.data


def test_search_suggestions_route(client):
    response = client.post('/search_suggestions', data={'input': 'Test'})
    assert response.status_code == 200
    assert b'Test Recipe' in response.data


# Modify the assertion in the test
def test_get_category_id_route(client):
    response = client.get('/get_category_id?name=Test%20Category')
    assert response.status_code == 200
    
    # Get the category ID based on the response content
    category_id = str(mongo.db.categories.find_one({'name': 'Test Category'})['_id'])

    # Assert that the category ID is in the response data
    assert category_id.encode() in response.data

def test_add_recipe_route_invalid_input(client):
    response = client.post('/add_recipe', data={'name': '123Recipe', 'category_id': 'invalid_id'})
    assert response.status_code == 400  # Validation fails, should stay on the same page

def test_category_route_not_found(client):
    response = client.get('/category/NonExistentCategory')
    assert response.status_code == 200
    assert b'Category not found' in response.data

def test_add_recipe_existing_recipe(client):
    data = {
        'name': 'Test Recipe',
        'category_id': str(mongo.db.categories.find_one({'name': 'Test Category'})['_id']),
        'description': 'Test Description',
        'ingredients': 'Ingredient 1\r\nIngredient 2',
        'instructions': 'Test Instructions'
    }
    response = client.post('/add_recipe', data=data)
    assert response.status_code == 302  # Validation fails, should stay on the same page

def test_search_route_empty_query(client):
    response = client.get('/search?query=')
    assert response.status_code == 302  # Redirects to home page for empty query

def test_search_route_special_characters(client):
    response = client.get('/search?query=!@#')
    assert response.status_code == 200
    assert b'No Results' in response.data  # Assuming you have a template for no results

def test_search_route_case_insensitive(client):
    response_upper = client.get('/search?query=TEST')
    response_lower = client.get('/search?query=test')
    assert response_upper.data == response_lower.data  # Case-insensitive search

def test_search_suggestions_response_format(client):
    response = client.post('/search_suggestions', data={'input': 'Test'})
    assert response.status_code == 200
    assert 'application/json' in response.content_type
    assert 'suggestions' in response.get_json()
