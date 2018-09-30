import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """ Display users holdings"""

    if request.method == "POST":
        # Return user's ID
        user_id = session["user_id"]

        # Initialize the portfolio total value
        portfolio_value = float(0)

        # Return user's portfolio
        stocks = db.execute("SELECT * FROM portfolio WHERE id = :user_id", user_id=user_id)

        # Update the portfolio at render of index.html to show the current price of each stock
        for stock in stocks:
            symbol = stock["symbol"]
            shares = int(stock["number"])
            purchase_price = float(stock["purchase_price"])
            price = lookup(symbol)
            current_price = float(price["price"])
            name = price["name"]
            total = current_price * int(shares)
            portfolio_value = float(portfolio_value + shares * current_price)
            db.execute("UPDATE portfolio SET current_price = :current_price WHERE id = :user_id and symbol = :symbol",
                       current_price=current_price, user_id=user_id, symbol=symbol)
            db.execute("UPDATE portfolio SET name = :name WHERE id = :user_id and symbol = :symbol",
                       name=name, user_id=user_id, symbol=symbol)
            db.execute("UPDATE portfolio SET total = :total WHERE id = :user_id and symbol = :symbol",
                       total=total, user_id=user_id, symbol=symbol)

        # Return the users cash
        current_cash = db.execute("SELECT * FROM users WHERE id = :user_id", user_id=user_id)
        cash = float(current_cash[0]["cash"])

        # Return the total of their cash and the current portfolio value
        total = float(current_cash[0]["cash"]) + float(portfolio_value)

        # Return the entire portfolio with updated values
        updated_portfolio = db.execute("SELECT * FROM portfolio WHERE id = :user_id", user_id=user_id)

        # Render index.html
        return render_template("index.html", stocks=updated_portfolio, cash=cash, total=total)

    else:
        user_id = session["user_id"]
        rows = db.execute("SELECT * FROM portfolio WHERE id = :user_id", user_id=user_id)
        portfolio_value = 0
        for stocks in rows:
            symbol = stocks["symbol"]
            shares = int(stocks["number"])
            stock_info = lookup(symbol)
            current_price = float(stock_info["price"])
            total = current_price * shares
            db.execute("UPDATE portfolio SET current_price = :current_price AND total = :total WHERE id = :user_id AND symbol = :symbol",
                       current_price=current_price, total=total, user_id=user_id, symbol=symbol)
            portfolio_value = portfolio_value + total
        current_cash = db.execute("SELECT * FROM users WHERE id = :user_id", user_id=user_id)
        cash = float(current_cash[0]["cash"])
        total = cash + portfolio_value
        portfolio = db.execute("SELECT * FROM portfolio WHERE id = :user_id", user_id=user_id)
        return render_template("index.html", stocks=portfolio, cash=cash, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("buy.html")
    # User reached route via POST (as by submitting a form)
    else:
        symbol = request.form.get("symbol").upper()
        if not symbol:
            return apology("Please enter a stock symbol.", 400)
        stock = lookup(symbol)
        # Verify that user input a valid stock symbol
        if not stock:
            return apology("Invalid Symbol", 400)
        try:
            shares = int(request.form.get("shares"))
            if not shares:
                return apology("Please enter the number of shares you wish to purchase.", 400)
            # Verify the user input a valid integer for number of shares to purchase
            if shares < 1:
                return apology("Please enter a value greater than 0.", 400)
        except:
            return apology("Shares must be a positive integer.", 400)

        # Get user's available cash
        user_id = session["user_id"]
        cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=user_id)
        # Check that user has cash at all
        if not cash:
            return apology("Insufficient Funds.", 400)
        else:
            cash_avail = float(cash[0]["cash"])
            current_price = stock["price"]
            purchase_price = shares * current_price
            # Check that user has enough cash for proposed transaction
            if purchase_price > cash_avail:
                return apology("Insufficient Funds.", 400)
            else:
                # Update users db with new cash
                new_cash = cash_avail - purchase_price
                db.execute("UPDATE users SET cash = :new_cash WHERE id = :user_id", new_cash=new_cash, user_id=user_id)
                # Determine if user already owns this stock
                portfolio = db.execute("SELECT * FROM portfolio WHERE id = :user_id AND symbol = :symbol",
                                       user_id=user_id, symbol=symbol)
                if len(portfolio) == 0:
                    # User does not already own this stock, purchse needs to be apended to portfolio.db
                    name = stock["name"]
                    db.execute("INSERT INTO portfolio (id, symbol, number, current_price, name, total) VALUES (:user_id, :symbol, :number, :current_price, :name, :total)",
                               user_id=user_id, symbol=symbol, number=shares, current_price=current_price, name=name, total=purchase_price)
                else:
                    # User already owns this stock and portfolio.db needs to be modified
                    new_shares = shares + int(portfolio[0]["number"])
                    new_total = new_shares * current_price
                    db.execute("UPDATE portfolio SET number = :number AND total = :total AND current_price = :current_price WHERE id = :user_id AND symbol = :symbol",
                               number=new_shares, total=new_total, current_price=current_price, user_id=user_id, symbol=symbol)
                # Update transactions.db to reflect purchase
                date_time = datetime.datetime.now()
                db.execute("INSERT INTO transactions (user_id, date_time, symbol, number, price) VALUES (:user_id, :date_time, :symbol, :number, :price)",
                           user_id=user_id, date_time=date_time, symbol=symbol, number=shares, price=current_price)
                # Render index.html
                return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Return user_id
    user_id = session["user_id"]

    # Return transactions for user
    rows = db.execute("SELECT * FROM transactions WHERE user_id = :user_id", user_id=user_id)

    # Render history.html
    return render_template("history.html", stocks=rows)


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
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

    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("Please enter a stock symbol.", 400)
        else:
            # Pass stock symbol through lookup function
            symbol = request.form.get("symbol")
            rows = lookup(symbol)

            # Validate stock symbol
            if not rows:
                return apology("Invalid Symbol", 400)

            price = rows["price"]

            # Render quoted.html passing stock parameter through
            return render_template("quoted.html", stock=rows, price=price)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Missing username!", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("please confirm password", 400)

        # Validate password
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username is available
        if len(rows) != 0:
            return apology("This username is unavailable. Please try a new one", 400)

        # Generate hash of user-submitted password
        hash_pwd = generate_password_hash(request.form.get("password"))

        # Pass username and hash into users database
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                   username=request.form.get("username"), hash=hash_pwd)

        # Remember user and log them in
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page upon successful registration
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    user_id = session["user_id"]
    timestamp = datetime.datetime.now()

    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        shares_to_sell = int(request.form.get("shares"))
        shares = -shares_to_sell

        rows = db.execute("SELECT * FROM portfolio WHERE id = :user_id AND symbol = :symbol", user_id=user_id, symbol=symbol)
        if len(rows) == 0:
            return apology("You do not own this stock.", 400)
        else:
            # Get how many shares the user owns
            shares_owned = int(rows[0]["number"])
            # total = float(rows[0]["total"])

            if (shares_to_sell > shares_owned):
                return apology("You cannot sell more shares than you own.", 400)
            else:
                stock_info = lookup(symbol)
                current_price = float(stock_info["price"])
                purchase_price = current_price * shares_to_sell
                new_shares = shares_owned - shares_to_sell
                user_data = db.execute("SELECT * FROM users WHERE id = :user_id", user_id=user_id)
                cash = user_data[0]["cash"]
                new_cash = cash + purchase_price
                # Update portfolio for sale
                if new_shares == 0:
                    db.execute("DELETE FROM portfolio WHERE id = :user_id AND symbol = :symbol", user_id=user_id, symbol=symbol)
                else:
                    db.execute("UPDATE portfolio SET number = :new_shares WHERE id = :user_id AND symbol = :symbol",
                               new_shares=new_shares, user_id=user_id, symbol=symbol)
                # Update cash in users
                db.execute("UPDATE users SET cash = :new_cash WHERE id = :user_id", new_cash=new_cash, user_id=user_id)
                # Update transactions
                db.execute("INSERT INTO transactions (user_id, date_time, symbol, number, price) VALUES (:user_id, :date_time, :symbol, :number, :price)",
                           user_id=user_id, date_time=timestamp, symbol=symbol, number=shares, price=current_price)

                return redirect("/")
    else:
        stock = db.execute("SELECT * FROM portfolio WHERE id = :user_id", user_id=user_id)
        return render_template("sell.html", stocks=stock)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
