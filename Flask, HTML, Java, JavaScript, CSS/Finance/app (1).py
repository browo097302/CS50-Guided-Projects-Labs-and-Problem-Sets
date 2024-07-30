import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    portfolio = db.execute("SELECT symbol, SUM(shares) AS shares, price FROM purchases WHERE user_id = ? GROUP BY symbol", user_id)
    cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    cash = cash_db[0]["cash"]



    return render_template("index.html", data = portfolio, cash = cash)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")
        if not symbol:
            return apology("invalid symbol")

        if not shares.isdigit() or int(shares) <= 0:
            return apology("please enter positive, non fractional number shares")
        shares = int(shares)
        stock = lookup(symbol)
        if stock == None:
            return apology("invalid symbol")

        price = stock["price"]
        total_cost = int(shares) * price

        user_id = session["user_id"]
        cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        cash = cash_db[0]["cash"]


        if total_cost > cash:
            return apology("insufficient funds")


        db.execute("UPDATE users SET cash = cash - :total_cost WHERE id = :user_id", total_cost = total_cost,  user_id=session["user_id"])
        db.execute("INSERT INTO purchases (user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)", user_id = session["user_id"], symbol=symbol, shares=shares, price=price)



        return redirect("/")
    else:
        return render_template("buy.html")




@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    user_id = session["user_id"]
    history = db.execute("SELECT id, symbol, shares, price, timestamp FROM purchases WHERE user_id = ?", (user_id,))
    return render_template("history.html", data = history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "GET":
        return render_template("quote.html")
    else:
        symbol = request.form.get("symbol").upper()

        if not symbol:
            return apology("invalid symbol")

        stock = lookup(symbol)
        if stock == None:
            return apology("invalid symbol")

        return render_template("quoted.html", symbol = stock["symbol"], price = stock["price"] )




@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()

    if request.method == "POST":

        if not request.form.get("password"):
            return apology("password invalid", 400)

        elif not request.form.get("username"):
            return apology("username invalid", 400)

        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 400)

        row = db.execute("SELECT username FROM users WHERE username = ?", request.form.get("username"))

        if len(row) != 0:
            return apology("this username has already been taken", 400)
        db.execute('INSERT INTO users (username, hash) VALUES (?,?)', request.form.get("username"), generate_password_hash(request.form.get("password")))

        row = db.execute('SELECT * FROM users WHERE username = ?', request.form.get("username"))

        session['user id'] = row[0]["id"]

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():

    if request.method == "POST":

        amount = request.form.get("amount")

        if int(amount) < 0:
             return apology("must be more than 0")

        user_id = session["user_id"]
        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        current_cash = cash[0]["cash"]
        new_cash = int(amount) + current_cash
        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash, user_id)
        return redirect("/")
    else:
        return render_template("add.html")






@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":

        user_id = session["user_id"]
        symbols = db.execute("SELECT symbol FROM purchases WHERE user_id = ? GROUP BY shares HAVING SUM(shares) > 0", user_id)
        return render_template("sell.html", symbols = [row["symbol"] for row in symbols])
    else:
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        if not symbol:
            return apology("invalid symbol")
        if int(shares) < 0:
                    return apology("please enter positive number of shares")
        stock = lookup(symbol.upper())

        if stock == None:
            return apology("invalid symbol")
        user_id = session["user_id"]
        search = db.execute("SELECT symbol, SUM(shares) AS shares, price FROM purchases WHERE user_id = ? AND symbol = ? GROUP BY symbol HAVING shares > 0", user_id, symbol)
        if len(search) == 0:
            return apology("stock not owned")

        current_shares = db.execute("SELECT SUM(shares) AS shares FROM purchases WHERE user_id = ? AND symbol = ?", user_id, symbol)
        current_holding = current_shares[0]["shares"]
        if int(current_holding) < int(shares):
            return apology("stock not owned")

        price = stock["price"]
        sale_value = int(shares) * price
        user_id = session["user_id"]
        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        cash_amount = cash[0]["cash"]
        new_balance = cash_amount + sale_value
        shares = -int(shares)

        db.execute("INSERT INTO  purchases (user_id, symbol, shares, price) VALUES (?,?,?,?)", user_id, symbol, shares, price)
        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_balance, user_id)


        return redirect("/")



