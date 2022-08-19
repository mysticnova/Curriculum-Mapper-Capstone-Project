from flask import Flask, render_template
import neo4jTest

app = Flask(__name__)

'''flask app test'''

@app.route('/')
def index():
    return render_template('test.html')

@app.route('/test', methods=['POST', 'GET'])
def test():
    data = neo4jTest.search_by_label('Outcome')
    return data