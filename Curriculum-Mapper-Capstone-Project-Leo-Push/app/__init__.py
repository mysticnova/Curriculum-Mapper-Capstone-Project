from flask import Flask

# create the application object
app = Flask(__name__)

from app import routes, neo4jDB