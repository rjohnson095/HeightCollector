# -------------------------------------------------------------------------
# Program which uses the Flask framework and PostgreSQL database
# to create an online app (rjdatacollector.herokuapp.com).
#
# The app collects the user's email and height and stores the info
# in a database. The user is then emailed automatically with the
# average height of all users so far and the number users being calculated.
#
# Ryley Johnson
# -------------------------------------------------------------------------

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy.sql import func


app=Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:Panther06!@localhost/height_collector'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://tbkiutqxzauyis:d1d6a87a8cf43b15a803f80abaa360e464ec2ccb954de13639e257cfdda44886@ec2-35-175-155-248.compute-1.amazonaws.com:5432/d36cn2mo012c79?sslmode=require'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db=SQLAlchemy(app)

class Data(db.Model):
    __tablename__="data"
    id=db.Column(db.Integer, primary_key=True)
    email_=db.Column(db.String(120),unique=True)
    height_=db.Column(db.Integer)

    def __init__(self,email_,height_):
        self.email_= email_
        self.height_= height_





@app.route("/")
def index():
        return render_template("index.html")

@app.route("/success", methods=['Post'])
def success():
    if request.method == 'POST':
        email=request.form["email_name"]
        height=request.form["height_name"]
        if db.session.query(Data).filter(Data.email_==email).count() == 0:
            data =Data(email,height)
            db.session.add(data)
            db.session.commit()
            average_height = db.session.query(func.avg(Data.height_)).scalar()
            average_height = round(average_height,1)
            count = db.session.query(Data.height_).count()
            send_email(email,height, average_height, count)
            return render_template("success.html")
    return render_template('index.html', text="Seems like we've received your email address already.")




if __name__ == '__main__':
    app.debug=True
    app.run()
