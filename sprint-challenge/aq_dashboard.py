"""OpenAQ Air Quality Dashboard with Flask."""
# All the imports that we'll need
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import openaq

# Initiating our App with Flask SqlAlchemy
APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)

# The variables and function for Part 2 of the SC
OAQ = openaq.OpenAQ()
LAstatus, LAbody = OAQ.measurements(city='Los Angeles', parameter='pm25')
def part1(X):
    LAresults = X['results']
    values = []
    for i in LAresults: 
        ivalue = i.get('value')
        idate = i.get('date')
        iutc = idate.get('utc')
        values.append((ivalue, iutc))
    return values

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return f"<id={self.id}, datetime={self.datetime}, value={self.value}>"
        # '<DateTime: %r ::::: Value: %r>' % (self.datetime, self.value)


@APP.route('/')
def root():
    """Base view."""
    # res = str(part1(LAbody))
    tenplus = Record.query.filter(Record.value>=10).all()
    output=''
    for rec in tenplus:
        output += 'datetime = '+ rec.datetime
        output += ", "
        output += 'value = '+ str(rec.value)
        output += '</br>'

    return output #f'The potentially risky values are: {tenplus}'  <== This will give the correct out put in the shell :-/

@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # TODO Get data from OpenAQ, make Record objects with it, and add to db
    OAQ_items = LAbody['results']
    for x in OAQ_items: 
        xvalue = x.get('value')
        xdate = x.get('date')
        xutc = xdate.get('utc')
        db_item = (Record(datetime=xutc, value=xvalue))
        DB.session.add(db_item)    
    DB.session.commit()
    return 'Data refreshed!'