from flask import Flask

server = Flask(__name__)
server.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

from flaskdashapp import routes