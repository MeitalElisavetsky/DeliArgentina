from app import app, mongo  # Import the 'mongo' object from the 'app' package
from bson import ObjectId  # Import ObjectId for creating MongoDB ObjectId

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)


