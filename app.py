from flask import Flask, render_template, request, redirect
import database

app = Flask(__name__)

database.init_db()

@app.route("/")
def home():
    return render_template("home.html")


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


@app.route("/passenger_login", methods=["GET","POST"])
def passenger_login():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "passenger" and password == "1234":
            return redirect("/passenger_dashboard")

        return "Invalid login"

    return render_template("passenger_login.html")


@app.route("/driver_login", methods=["GET","POST"])
def driver_login():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "driver" and password == "1234":
            return redirect("/driver_dashboard")

        return "Invalid login"

    return render_template("driver_login.html")

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


@app.route("/book_ride", methods=["GET","POST"])
def book_ride():

    if request.method == "POST":
        pickup = request.form["pickup"]
        destination = request.form["destination"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        c.execute(
            "INSERT INTO rides (pickup, destination, status) VALUES (?, ?, ?)",
            (pickup, destination, "waiting")
        )

        conn.commit()
        conn.close()

        return "Ride Requested!"

    return render_template("book_ride.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
