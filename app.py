from flask import Flask, render_template, request,redirect
import database
from auth import auth


app = Flask(__name__)

database.init_db()

app.register_blueprint(auth)

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/passenger_dashboard")
def passenger_dashboard():

    ride = database.get_latest_ride()

    return render_template(
        "passenger_dashboard.html",
        ride=ride
    )

@app.route("/request_ride", methods=["POST"])
def request_ride():

    pickup = request.form["pickup"]
    destination = request.form["destination"]

    # save ride to database
    database.add_ride(pickup, destination)
  
    return redirect("/passenger_dashboard")


@app.route("/passenger_register")
def passenger_register():
    return render_template("passenger_register.html")

@app.route("/driver_login")
def driver_login():
    return render_template("driver_login.html")


@app.route("/driver_dashboard")
def driver_dashboard():

    waiting_rides = database.get_waiting_rides()
    accepted_rides = database.get_all_rides()

    return render_template(
        "driver_dashboard.html",
        waiting_rides=waiting_rides,
        accepted_rides=accepted_rides
    )


@app.route("/ride_status")
def ride_status():

    waiting_rides = database.get_waiting_rides()
    accepted_rides = database.get_all_rides()

    return render_template(
        "passenger_status.html",
        waiting_rides=waiting_rides,
        accepted_rides=accepted_rides
    )


@app.route("/accept_ride/<int:ride_id>")
def accept_ride(ride_id):

    database.accept_ride(ride_id)

    return redirect("/driver_dashboard")

if __name__ == "__main__":
        app.run(host="0.0.0.0", port=5000)