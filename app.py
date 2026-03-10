from flask import Flask, render_template, request, redirect
import database

app = Flask(__name__)

database.init_db()

@app.route("/")
def home():
    return render_template("home.html")


# PASSENGER LOGIN
@app.route("/passenger_login")
def passenger_login():
    return render_template("passenger_login.html")


# DRIVER LOGIN
@app.route("/driver_login")
def driver_login():
    return render_template("driver_login.html")


# PASSENGER DASHBOARD
@app.route("/passenger_dashboard")
def passenger_dashboard():
    ride = database.get_latest_ride()

    return render_template(
        "passenger_dashboard.html",
        ride=ride
    )


# REQUEST RIDE
@app.route("/request_ride", methods=["POST"])
def request_ride():

    pickup = request.form["pickup"]
    destination = request.form["destination"]

    database.add_ride(pickup, destination)

    return redirect("/passenger_dashboard")


# DRIVER DASHBOARD
@app.route("/driver_dashboard")
def driver_dashboard():

    waiting_rides = database.get_waiting_rides()
    accepted_rides = database.get_all_rides()

    return render_template(
        "driver_dashboard.html",
        waiting_rides=waiting_rides,
        accepted_rides=accepted_rides
    )


# ACCEPT RIDE
@app.route("/accept_ride/<int:ride_id>")
def accept_ride(ride_id):

    database.accept_ride(ride_id)

    return redirect("/driver_dashboard")


# PASSENGER STATUS
@app.route("/ride_status")
def ride_status():

    waiting_rides = database.get_waiting_rides()
    accepted_rides = database.get_all_rides()

    return render_template(
        "passenger_status.html",
        waiting_rides=waiting_rides,
        accepted_rides=accepted_rides
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
