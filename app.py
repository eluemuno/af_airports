import json, os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, session, render_template, redirect, url_for, flash
from sqlalchemy import Column, Integer, String, Float, ForeignKey

app = Flask(__name__)
app.secret_key = secret_key
basedir = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'af_population.db')
app.config['TEMPLATES_AUTO_RELOAD'] = True
db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        country = request.form['country_name']
        dimension = request.form['dimension']
        if dimension == 'Airports':
            data_port = Airports.query.filter_by(country=country).all()
            if data_port:
                return render_template('result.html', data=data_port)
            else:
                return render_template('nodata.html')
        elif dimension == 'Population':
            data_population = Population.query.filter_by(country_name=country).all()
            if data_population:
                return render_template('result.html', data=data_population)
            else:
                return render_template('nodata.html')
        else:
            return render_template('index.html')
    else:
        return render_template('index.html')


@app.route('/add_airport', methods=['GET', 'POST'])
def add_record():
    if request.method == 'POST':
        icao_code = request.form['icaoCode']
        iata_code = request.form['iataCode']
        name = request.form['airportName']
        airport_size = request.form['airportSize']
        municipality = request.form['municipality']
        country = request.form['country']
        test = Airports.query.filter_by(country=country, iata_code=iata_code).first()
        if test:
            return render_template('exists.html')
        else:
            new_airport = Airports(
                icao_code=request.form['icaoCode'],
                iata_code=request.form['iataCode'],
                name=request.form['airportName'],
                airport_size=request.form['airportSize'],
                municipality=request.form['municipality'],
                country=request.form['country']
            )
        db.session.add(new_airport)
        db.session.commit()
        return render_template('acknowledge.html')
    else:
        return render_template('add_airport.html')


@app.route('/update_airport', methods=['GET', 'POST'])
def update_record():
    if request.method == 'POST':
        country = request.form['country']
        icao_code = request.form['icaoCode']
        test = Airports.query.filter_by(country=country, icao_code=icao_code).first()
        if test:
            test.icao_code = request.form['icaoCode']
            test.iata_code = request.form['iataCode']
            test.name = request.form['airportName']
            test.airport_size = request.form['airportSize']
            test.airport_size = request.form['airportSize']
            test.municipality = request.form['municipality']
            test.country = request.form['country']
            db.session.commit()
            return render_template('acknowledge.html')
        else:
            return render_template('nodata.html')
    else:
        return render_template('update_airport.html')


@app.route('/delete_airport', methods=['GET', 'POST'])
def delete_record():
    if request.method == 'POST':
        country = request.form['country']
        icao_code = request.form['icaoCode']
        airport = Airports.query.filter_by(country=country, icao_code=icao_code).first()
        if airport:
            db.session.delete(airport)
            db.session.commit()
            return render_template('acknowledge.html')
        else:
            return render_template('nodata.html')
    else:
        return render_template('delete_airport.html')


class Population(db.Model):
    __tablename__ = "population"
    id = Column(Integer, primary_key=True)
    country_name = Column(String)
    year = Column(String)
    population_count = Column(Integer)


class Countries(db.Model):
    __tablename__ = "countries"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    country_id = Column(String, unique=True)


class Airports(db.Model):
    __tablename__ = "airports"
    id = Column(Integer, primary_key=True)
    icao_code = Column(String)
    iata_code = Column(String)
    name = Column(String)
    airport_size = Column(String)
    municipality = Column(String)
    country = Column(String)


if __name__ == '__main__':
    app.run()
