from flask import Blueprint, render_template, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
import database

auth = Blueprint("auth", __name__)

# Passenger Register
@auth.route("/passenger/register", methods=["GET","POST"])
def passenger_register():

    if request.method == "POST":

        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        conn = database.connect()
        cur = conn.cursor()

        cur.execute(
        "INSERT INTO passengers(username,password) VALUES(?,?)",
        (username,password)
        )

        conn.commit()
        conn.close()

        return redirect("/passenger/login")

    return render_template("passenger_register.html")


# Passenger Login
@auth.route("/passenger/login", methods=["GET","POST"])
def passenger_login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = database.connect()
        cur = conn.cursor()

        cur.execute(
        "SELECT password FROM passengers WHERE username=?",
        (username,)
        )

        user = cur.fetchone()

        if user and check_password_hash(user[0],password):
            return "Passenger Logged In"

    return render_template("passenger_login.html")


# Driver Register
@auth.route("/driver/register", methods=["GET","POST"])
def driver_register():

    if request.method == "POST":

        username = request.form["username"]
        password = generate_password_hash(request.form["password"])
        car = request.form["car"]
        plate = request.form["plate"]

        conn = database.connect()
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO drivers(username,password,car,plate)
        VALUES(?,?,?,?)
        """,(username,password,car,plate))

        conn.commit()
        conn.close()

        return redirect("/driver/login")

    return render_template("driver_register.html")


# Driver Login
@auth.route("/driver/login", methods=["GET","POST"])
def driver_login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = database.connect()
        cur = conn.cursor()

        cur.execute(
        "SELECT password FROM drivers WHERE username=?",
        (username,)
        )

        user = cur.fetchone()

        if user and check_password_hash(user[0],password):
            return "Driver Logged In"

    return render_template("driver_login.html")