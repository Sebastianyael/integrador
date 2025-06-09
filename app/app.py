from flask import Flask , render_template
from flask_mysqldb import MySQL 

app = Flask(__name__)

app.config['MySQL_HOST'] = 'localhost'


@app.route('/')
def index():
    return render_template('login.html')


if(__name__ == '__main__'):
    app.run(debug = True)

