# NOTE: This file was working to bring in the case line data straight from the DOH website. However, it timed out.

import os, datetime, time, json, csv, statistics
from csv import writer
import requests
import urllib.parse


from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

# from helpers import apology, login_required, lookup, usd # FROM CS50 FINANCE

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
# app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///covidfl.db")

# @app.route("/")
# @login_required
# def index():


# def datapull():
# Contact API
# Collier County URL for JSON (?)
url_2 = "https://opendata.arcgis.com/datasets/a7887f1940b34bf5a02c6f7f27a5cb2c_0.geojson?where=COUNTYNAME%20%3D%20'collier'"

url_1 = 'https://services1.arcgis.com/CY1LXxl9zlJeBuRZ/arcgis/rest/services/Florida_COVID19_Cases/FeatureServer/0/query?where=COUNTY%20%3D%20%27COLLIER%27&outFields=*&outSR=4326&f=json'
# Case Line Data =
url_3 = "https://services1.arcgis.com/CY1LXxl9zlJeBuRZ/arcgis/rest/services/Florida_COVID19_Case_Line_Data_NEW/FeatureServer/0/query?where=1%3D1&outFields=County,Age,Age_group,EDvisit,Hospitalized,Died,EventDate,ObjectId&returnGeometry=false&outSR=4326&f=json"
# All Case Line Data = 5104 rows
url_4 = "https://services1.arcgis.com/CY1LXxl9zlJeBuRZ/arcgis/rest/services/Florida_COVID19_Case_Line_Data_NEW/FeatureServer/0/query?where=1%3D1&outFields=*&f=json"
# All Case Line Data = 372 rows
url_5 = "https://services1.arcgis.com/CY1LXxl9zlJeBuRZ/arcgis/rest/services/Florida_COVID19_Case_Line_Data_NEW/FeatureServer/0/query?outFields=*&where=1%3D1"
# From Florida Covid Action https://floridacovidaction.com/library/
url_6 = "https://services2.arcgis.com/QTlu74VtgQxQNkN3/ArcGIS/rest/services/FCA_Florida_Daily_and_Cumulative_Case_and_Death_Counts/FeatureServer/0/query?outFields=*&where=1%3D1"
# Try offset #1
url_7 = "https://services1.arcgis.com/CY1LXxl9zlJeBuRZ/arcgis/rest/services/Florida_COVID19_Case_Line_Data_NEW/FeatureServer/0/query?where=1%3D1&outFields=County,Age,Age_group,EDvisit,Hospitalized,Died,EventDate,ObjectId&returnGeometry=false&outSR=4326&having=&resultOffset=0&f=json"
url_7_begin = "https://services1.arcgis.com/CY1LXxl9zlJeBuRZ/arcgis/rest/services/Florida_COVID19_Case_Line_Data_NEW/FeatureServer/0/query?where=1%3D1&outFields=County,Age,Age_group,EDvisit,Hospitalized,Died,EventDate,ObjectId&returnGeometry=false&outSR=4326&having=&resultOffset="
url_7_end = "&f=json"

# Working one is url_3 (/7/25/2020)
# url = url7
count = 0

## TO CONVERT FROM UNIX TIME (IN DATABASE) TO UTC:
case_date = datetime.datetime.fromtimestamp(int("1585872000000")/1000).strftime('%Y-%m-%d')
print(case_date)

# starting parameter to for the while loop
limit_check = True
# Starting line allows me to start pulling in later in the database. 150 would be 150 x 2000 or the 300,000th line.
starting_line = 200
i = starting_line

while limit_check == True:
    url = url_7_begin + str(i * 2000) + url_7_end
    # print(url)
    response = requests.get(url)
    response.raise_for_status()
    data_loop = json.loads(response.text)
    if data_loop == response.json():
        # print(data_loop.keys())
        # print("Transfer Limit:")
        try:
            limit_check = data_loop['exceededTransferLimit']
        except:
            limit_check = False
        # print(data_loop['exceededTransferLimit'])
        # print(data_loop['features'])
        # print(type(data_loop['features']))
        # fieldnames = data_loop['features'][0]['attributes'].keys()
        # print(fieldnames)
        data_loop_list = data_loop['features']
        # print(type(data_loop_list))
        if i == starting_line:
            data_main = data_loop['features']
        else:
            for j in range(len(data_loop_list)):
                data_main.append(data_loop_list[j])
        # limit_check = data_loop['exceededTransferLimit']
        # print("*******************")
        # print("Data Main records: " + str(len(data_main)))
        print(data_main[-1]["attributes"]["ObjectId"])

    i += 1
    # print("*****************")

# Function to the summary statistics. Pass it the county name and the data.
def county_stats(data_main, county):
    all_age_list = list()
    hosp_age_list = list()
    died_age_list = list()
    case = 0
    hosp = 0
    died = 0
    exc = 0

    for i in range(len(data_main)):
        if data_main[i]['attributes']['County'] == county:
            case += 1
            try:
                if int(data_main[i]['attributes']['Age']) >= 0:
                    all_age_list.append(int(data_main[i]['attributes']['Age']))
            except:
                exc += 1
            if (data_main[i]['attributes']['Hospitalized'] == "yes" or data_main[i]['attributes']['Hospitalized'] == "YES" or data_main[i]['attributes']['Hospitalized'] == "Yes"):
                hosp += 1
                hosp_age_list.append(int(data_main[i]['attributes']['Age']))
            if (data_main[i]['attributes']['Died'] == "yes" or data_main[i]['attributes']['Died'] == "YES" or data_main[i]['attributes']['Died'] == "Yes"):
                died += 1
                died_age_list.append(int(data_main[i]['attributes']['Age']))

    print("County: " + county)
    print("Cases = " + str(case))
    print("Hospitalizations = " + str(hosp))
    print("Died = " + str(died))
    print("Median Age of all Cases: " + str(round(statistics.median(all_age_list))))
    print("Median Age of Hospitalizations " + str(round(statistics.median(hosp_age_list))))
    print("Median Age of Deaths " + str(round(statistics.median(died_age_list))))


# These call the function that will run the county-level statistics
print("******************************")
county_stats(data_main, 'Collier')
# print("******************************")
# county_stats(data_main, 'Lee')
# print("******************************")
# county_stats(data_main, 'Dade')
# print("******************************")
# county_stats(data_main, 'Broward')
# print("******************************")
# county_stats(data_main, 'Palm Beach')

# Below, I was starting to work on the process of writing this to a CSV.
test_keys = list(data_main[-1]['attributes'].keys())
test_values = list(data_main[-1]['attributes'].values())
print(test_keys)
print(test_values)



# TO DO
# THE DOH SYSTEM ISN'T LETTING ME PULL IN THE WHOLE DATABASE. I NEED TO WRITE TO A CSV AND RUN IT IN MULTIPLE PARTS.

#     county = data_list[i]["attributes"]["County"]
#     age = int(data_list[i]["attributes"]["Age"])
#     age_group = data_list[i]["attributes"]["Age_group"]
#     edvisit = data_list[i]["attributes"]["EDvisit"]
#     hosp = data_list[i]["attributes"]["Hospitalized"]
#     died = data_list[i]["attributes"]["Died"]
#     eventdate = datetime.datetime.fromtimestamp(int(data_list[i]["attributes"]["EventDate"])/1000).strftime('%Y-%m-%d')
#     objectid = int(data_list[i]["attributes"]["ObjectId"])
#     db.execute("INSERT INTO caseline (County, Age, Age_Group, EDVisit, Hospitalized, Died, EventDate, ObjectID) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (county, age, age_group, edvisit, hosp, died, eventdate, objectid))

# count the dicts in the dict

# for row in response:
#     count +=1
    # if (int(row['ObjectId']) % 10) == 0:
    #     print(row['ObjectId'])





# print(count)
#                     # write the transaction to the database
#                     db.execute("INSERT INTO caseline (datetime, date, user_id, symbol, shares, price, txn_amount) VALUES (?, ?, ?, ?, ?, ?, ?)",
#                         (txn_time, txn_date, buy_user_id, symbol_dict["symbol"], int(buy_shares), usd_price, buy_amount))


# print(response.text)
# print(response.headers)
# https://services1.arcgis.com/CY1LXxl9zlJeBuRZ/arcgis/rest/services/Florida_COVID19_Cases/FeatureServer/0/query?where=COUNTY%20%3D%20%27COLLIER%27&outFields=*&outSR=4326&f=json
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#     except requests.RequestException:
#         return None

#     # Parse response
#     try:
#         Cases = response.json()
#         return {
#             "CasesAll": collier["CasesAll"],
#             "HospRes": collier["C_HospYes_Res"],
#             "HospNonRes": collier["C_HospYes_NonRes"],
#             "DeathsRes": collier["C_FLResDeaths"],
#             "DeathsNonRes": collier["C_NonResDeaths"],
#             "MedianAge": collier["MedianAge"]
#         }
#     except (KeyError, TypeError, ValueError):
#         return None

# collier_list = datapull()

# print(collier_list)

############################################################################################################################
# BELOW THIS IS THE CODE FOR CS50 FINANCE ... USE AS A BASE ################################################################
############################################################################################################################
# Make sure API key is set
# if not os.environ.get("API_KEY"):
#     raise RuntimeError("API_KEY not set")


# @app.route("/")
# @login_required
# def index():
#     """Show portfolio of stocks"""
#     # Initialize the portfolio list
#     portfolio_list = []

#     # Initialize the symbol_shares list, which will be used for  the table of symbols and sum of shares.
#     symbol_shares_list = []

#     # The user_id will be used to make sure the database pull is only for the logged in user.
#     index_user_id = session["user_id"]

#     # Database pull for symbol and sum of shares, filtered where the sum of shares are greater than 0
#     symbol_shares_list = db.execute("SELECT symbol, sum(shares) FROM txns WHERE user_id = :id GROUP BY symbol HAVING sum(shares) > 0",
#             id=index_user_id)
#     stocks_in_port = len(symbol_shares_list)

#     # Set up the components that will go in the HTML table.
#     stock_value = 0.0
#     if stocks_in_port > 0:
#         for i in range(stocks_in_port):
#             # Initialize the list as list of lists with None
#             portfolio_list.append([None] * 6)
#             # Data item #1 is symbol
#             portfolio_list[i][0] = symbol_shares_list[i]["symbol"]
#             # Data item #3 is sum of the shares
#             portfolio_list[i][2] = symbol_shares_list[i]["sum(shares)"]
#             # Use IEX lookup for #2, 4, and 5
#             iex_lookup = lookup(symbol_shares_list[i]["symbol"])
#             # Data item #2 is name of the stock
#             portfolio_list[i][1] = iex_lookup["name"]
#             # Data item #4 is name of the stock
#             portfolio_list[i][3] = usd(iex_lookup["price"])
#             # Data item #5 is the current value of the stock (price x current total shares)
#             portfolio_list[i][4] = iex_lookup["price"] * symbol_shares_list[i]["sum(shares)"]
#             # Data item #6 is the string representation of Data item #5 (current stock value)
#             portfolio_list[i][5] = usd(portfolio_list[i][4])
#             # This updates the total stock value with Data item #5 (current stock value)
#             stock_value = stock_value + float(portfolio_list[i][4])
#         # print(portfolio_list)
#         # print("Stocks total = " + usd(stock_value))

#     # Database pull in order to get the cash from the logged in user
#     rows = db.execute("SELECT cash FROM users WHERE id = :id",
#               id=index_user_id)
#     cash = rows[0]["cash"]
#     # print("Cash total = " + usd(cash))
#     port_value = stock_value + cash
#     # print("Grand total = " + usd(port_value))
#     # Get the number of rows in the portfolio, which will be used in the index table
#     rows = len(portfolio_list)
#     # print("rows for portfolio = " + str(rows))
#     return render_template("index.html", portfolio_list=portfolio_list, stock_value=usd(stock_value), cash=usd(cash), port_value=usd(port_value), rows=rows)

# @app.route("/buy", methods=["GET", "POST"])
# @login_required
# def buy():
#     """Buy shares of stock"""
#     symbol_dict = []

#     if request.method == "POST":

#         # Ensure ticker was entered
#         if not request.form.get("symbol"):
#             return apology("must enter ticker", 403)

#         else:
#             buy_symbol = request.form.get("symbol").upper()

#         buy_shares = request.form.get("shares")

#         # Ensure number of shares was entered
#         if not request.form.get("shares"):
#             return apology("must enter # of shares", 403)

#         # Ensure number of shares is positive integer
#         elif ("." in buy_shares) == True or int(buy_shares) <= 0:
#             return apology("must enter a positive integer", 403)

#         # Lookup symbol via API
#         else:
#             # Lookup symbol
#             symbol_dict = lookup(buy_symbol)
#             # return apology("stopped point", 403)

#             # If symbol doesn't exist, then apology()
#             if symbol_dict == None:
#                 return apology("ticker doesn't exist; go back", 403)

#             # Else, lookup and submit variables to quoted.html
#             else:
#                 # print(symbol_dict["symbol"])
#                 # print(symbol_dict["name"])
#                 # print(symbol_dict["price"])
#                 usd_price = usd(symbol_dict["price"])
#                 # print(usd_price)

#                 buy_amount = -round(float(symbol_dict["price"]) * float(buy_shares),2)
#                 # print("Buy_amount = " + str(buy_amount))

#                 # Check to see if "amount" = shares x price <= cash (apology if not)
#                 # Get cash from users table
#                 buy_user_id = session["user_id"]
#                 rows = db.execute("SELECT cash FROM users WHERE id = :id",
#                           id=buy_user_id)
#                 cash_verify = rows[0]["cash"]
#                 # print("Current cash = $" + str(cash_verify))
#                 buy_time = datetime.datetime.now()
#                 txn_time = buy_time.strftime("%Y-%m-%d %H:%M:%S")
#                 txn_date = buy_time.strftime("%Y-%m-%d")
#                 # print(txn_time)
#                 # print(txn_date)

#                 if -buy_amount > cash_verify:
#                     return apology("you don't have enough cash; try again", 403)

#                 else:
#                     # write the transaction to the database
#                     db.execute("INSERT INTO txns (datetime, date, user_id, symbol, shares, price, txn_amount) VALUES (?, ?, ?, ?, ?, ?, ?)",
#                         (txn_time, txn_date, buy_user_id, symbol_dict["symbol"], int(buy_shares), usd_price, buy_amount))

#                     # update the cash portion (adds the buy_amount because that's a negative number, reducing cash)
#                     new_cash = cash_verify + buy_amount
#                     # print("New cash = " + str(new_cash))
#                     db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash=new_cash, id=buy_user_id)
#             # Redirect user to home page
#             return index()

#     # User reached route via GET (as by clicking a link or via redirect)
#     else:
#         return render_template("buy.html")

# @app.route("/history")
# @login_required
# def history():
#     """Show history of transactions"""
#     # History list will be used to pass into the history HTML template
#     history_list = []
#     txn_list = []
#     txn_list = db.execute("SELECT datetime, symbol, shares, price, txn_amount FROM txns WHERE user_id = :id",
#             id=session["user_id"])

#     # Number of rows, to be used to assign values to the history table
#     rows = len(txn_list)
#     if rows > 0:
#         for i in range(rows):
#             history_list.append([None] * 6)
#             history_list[i][0] = txn_list[i]["datetime"]
#             iex_lookup = lookup(txn_list[i]["symbol"])
#             history_list[i][1] = iex_lookup["name"]
#             history_list[i][2] = txn_list[i]["symbol"]
#             history_list[i][3] = txn_list[i]["shares"]
#             history_list[i][4] = txn_list[i]["price"]
#             history_list[i][5] = usd(txn_list[i]["txn_amount"])
#     else:
#         return index()

#     return render_template("history.html", history_list=history_list, rows=rows)


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     """Log user in"""

#     # Forget any user_id
#     session.clear()

#     # User reached route via POST (as by submitting a form via POST)
#     if request.method == "POST":

#         # Ensure username was submitted
#         if not request.form.get("username"):
#             return apology("must provide username", 403)

#         # Ensure password was submitted
#         elif not request.form.get("password"):
#             return apology("must provide password", 403)

#         # Query database for username
#         rows = db.execute("SELECT * FROM users WHERE username = :username",
#                           username=request.form.get("username"))

#         # Ensure username exists and password is correct
#         if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
#             return apology("invalid username and/or password", 403)

#         # Remember which user has logged in
#         session["user_id"] = rows[0]["id"]

#         # Redirect user to home page
#         return redirect("/")

#     # User reached route via GET (as by clicking a link or via redirect)
#     else:
#         return render_template("login.html")

# @app.route("/logout")
# def logout():
#     """Log user out"""

#     # Forget any user_id
#     session.clear()

#     # Redirect user to login form
#     return redirect("/")

# @app.route("/quote", methods=["GET", "POST"])
# @login_required
# def quote():
#     """Get stock quote."""
#     symbol_dict = []

#     if request.method == "POST":

#         # Ensure ticker was entered
#         if not request.form.get("symbol"):
#             return apology("must enter ticker", 403)

#         # Lookup symbol via API
#         else:
#             quote_symbol = request.form.get("symbol").upper()
#             # Lookup symbol
#             symbol_dict = lookup(quote_symbol)
#             # print(symbol_dict["name"])
#             # return apology("stopped point", 403)

#             # If symbol doesn't exist, then apology()
#             if symbol_dict == None:
#                 return apology("ticker doesn't exist; go back", 403)

#             # Else, lookup and submit variables to quoted.html
#             else:
#                 usd_price = usd(float(symbol_dict["price"]))

#             # Redirect user to home page
#             return render_template("quoted.html", symbol_dict=symbol_dict, usd_price=usd_price)

#     # User reached route via GET (as by clicking a link or via redirect)
#     else:
#         return render_template("quote.html")


# @app.route("/register", methods=["GET", "POST"])
# def register():
#     """Register user"""
#     # User reached route via POST (as by submitting a form via POST)
#     if request.method == "POST":

#         # Ensure username was submitted
#         if not request.form.get("username"):
#             return apology("must create username", 403)

#         # Ensure password was submitted
#         elif not request.form.get("password"):
#             return apology("must create password", 403)

#         # Ensure confirmation was submitted
#         elif not request.form.get("confirmation"):
#             return apology("must confirm password", 403)

#         # Ensure passwords match
#         elif request.form.get("confirmation") != request.form.get("password"):
#             return apology("passwords don't match", 403)

#         # If database is empty, register new user

#         # Query database for username: need to check if username is unique
#         rows = db.execute("SELECT * FROM users WHERE username = :username",
#                           username=request.form.get("username"))

#         # Ensure username is unique
#         if len(rows) != 0:
#             return apology("Choose a different username", 403)

#         else:
#             # Hash password
#             username = request.form.get("username")
#             hashed_password = generate_password_hash(request.form.get("password"))

#             # INSERT username and hashed password into finance.db
#             db.execute("INSERT INTO users(username, hash) VALUES(:username, :hashed_password)", username=username, hashed_password=hashed_password)

#             # Get id for the new user
#             rows = db.execute("SELECT id FROM users WHERE username=:username", username=username)

#             # Remember which user has logged in
#             session["user_id"] = rows[0]["id"]

#             # Redirect user to home page
#             return index()

#     # User reached route via GET (as by clicking a link or via redirect)
#     else:
#         return render_template("register.html")

# @app.route("/sell", methods=["GET", "POST"])
# @login_required
# def sell():
#     """Sell shares of stock"""

#     # Get the symbol and shares

#     if request.method == "POST":
#         sell_user_id = session["user_id"]

#         # Ensure ticker was entered
#         if not request.form.get("symbol"):
#             return apology("must enter ticker", 403)

#         sell_symbol = request.form.get("symbol").upper()
#         sell_shares = request.form.get("shares")

#         # Ensure number of shares was entered
#         if not request.form.get("shares"):
#             return apology("must enter # of shares", 403)

#         # Ensure number of shares is positive integer
#         elif ("." in sell_shares) == True or int(sell_shares) <= 0:
#             return apology("must enter a positive integer", 403)

#         else:
#             # Query the database for total shares of that symbol owned by that user.
#             rows = db.execute("SELECT user_id, symbol, sum(shares) FROM txns WHERE (symbol = :symbol AND user_id = :id) GROUP BY symbol",
#                 symbol=sell_symbol, id=sell_user_id)
#             # Confirm that the account owns the symbol
#             if rows == []:
#                 return apology("you don't own that stock; try again", 403)

#             # Confirm that the account owns at least that number of shares
#             current_shares = rows[0]["sum(shares)"]
#             if int(sell_shares) > int(current_shares):
#                 return apology("you don't have that many shares; try again", 403)
#             else:
#                 # Lookup symbol via API to get current price and sell value
#                 # Lookup symbol
#                 symbol_dict = lookup(sell_symbol)

#                 # If symbol doesn't exist, then apology()
#                 if symbol_dict == None:
#                     return apology("ticker doesn't exist; go back", 403)

#                 # Else, lookup and submit variables to quoted.html
#                 else:
#                     # print(symbol_dict["symbol"])
#                     # print(symbol_dict["name"])
#                     # print(symbol_dict["price"])
#                     usd_price = usd(float(symbol_dict["price"]))
#                     # print(usd_price)

#                     sell_amount = round(float(symbol_dict["price"]) * float(sell_shares),2)
#                     # print("Sell amount = " + str(sell_amount))

#                     sell_time = datetime.datetime.now()
#                     txn_time = sell_time.strftime("%Y-%m-%d %H:%M:%S")
#                     txn_date = sell_time.strftime("%Y-%m-%d")

#     # INSERT INTO the txns table

#                     # write the transaction to the database
#                     db.execute("INSERT INTO txns (datetime, date, user_id, symbol, shares, price, txn_amount) VALUES (?, ?, ?, ?, ?, ?, ?)",
#                         (txn_time, txn_date, sell_user_id, symbol_dict["symbol"], -int(sell_shares), usd_price, sell_amount))

#                     # Query users database to get current cash and then update the cash portion
#                     users = db.execute("SELECT cash FROM users WHERE id = :id", id=sell_user_id)
#                     cash_verify = users[0]["cash"]
#                     # Sets the new cash amount, taking the database pull and adding the sell amount (which will be a positive number)
#                     new_cash = cash_verify + sell_amount
#                     # print("New cash = " + str(new_cash))
#                     db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash=new_cash, id=sell_user_id)
#             # Redirect user to home page
#             return index()

#     # User reached route via GET (as by clicking a link or via redirect)
#     else:
#         return render_template("sell.html")

# def errorhandler(e):
#     """Handle error"""
#     if not isinstance(e, HTTPException):
#         e = InternalServerError()
#     return apology(e.name, e.code)


# # Listen for errors
# for code in default_exceptions:
#     app.errorhandler(code)(errorhandler)
