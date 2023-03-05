from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import select

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db=SQLAlchemy(app)
#db.init_app(app)

class Data(db.Model):
    __tablename__ = "data"

    id = db.Column(db.Integer, primary_key=True)
    rna_id = db.Column(db.String(30), nullable=True) 
    rna_id_ex = db.Column(db.String(30), nullable=True)
    gestion = db.Column(db.String(20), nullable=True)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/assos')
def assos():
    datas = Data.query.limit(30).all()
    return render_template('assos.html', datas=datas)


@app.route('/dashboard')
def dashboard():
    datas = Data.query.all()

    # Préparer les données pour le graphique Chart.js
    gestion_count = {}
    for d in datas:
        if d.gestion in gestion_count:
            gestion_count[d.gestion] += 1
        else:
            gestion_count[d.gestion] = 1

    gestion_values = list(gestion_count.values())
    gestion_labels = list(gestion_count.keys())
    data = {
        'values': gestion_values,
        'labels': gestion_labels
    }
    return render_template('dashboard.html', graph_data=json.dumps(data))



@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)
if __name__ == '__main__':
    app.run()  

