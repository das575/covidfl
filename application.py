from flask import Flask, render_template
from flask import Flask, jsonify, redirect, render_template, request, session
from flask_session import Session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from covidfl import covidfl
from covidfl_helpers import list_subtract, list_add2, list_add3, commas_place, pct

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# # Configure session to use filesystem (instead of signed cookies)
# app.config["SESSION_FILE_DIR"] = mkdtemp()
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

@app.route("/")
def index():
    # return 'Index!'
    # region_last_calcs = [['Region', 'Date', 'CasesAll', 'C_HospYes_Res', 'C_HospYes_NonRes', 'Deaths', 'T_negative', 'CasesAll_Chg', 'C_HospYes_Res_Chg', 'C_HospYes_NonRes_Chg', 'Deaths_Chg', 'T_negative_Chg'], ['Collier', '08/03/2020', 9811, 675, 12, 124, 50047, 77, 3, 0, 0, 447], ['Lee', '08/03/2020', 15799, 996, 17, 300, 94046, 125, 5, 0, 0, 508], ['South Florida', '08/03/2020', 34550, 2602, 27, 845, 229991, 324, 8, 0, 12, 1683], ['Tampa Bay Region', '08/03/2020', 30450, 1290, 12, 348, 197854, 332, 8, 0, 1, 2502], ['Orlando Region', '08/03/2020', 29927, 856, 41, 239, 228753, 228, 8, 0, 5, 1600], ['Jacksonville Region', '08/03/2020', 21830, 626, 15, 160, 177655, 165, 1, 0, 2, 1125], ['Rest of Florida', '08/03/2020', 331, 19, 0, 3, 3126, -3, 0, 0, 0, 20], ['State', '08/03/2020', 491884, 27366, 378, 7157, 3260914, 4752, 216, 4, 73, 27049], ['Collier', '08/02/2020', 9734, 672, 12, 124, 49600, 72, 4, 0, 0, 337], ['Lee', '08/02/2020', 15674, 991, 17, 300, 93538, 123, 10, 0, 0, 447], ['South Florida', '08/02/2020', 34226, 2594, 27, 833, 228308, 372, 9, 0, 0, 1951], ['Tampa Bay Region', '08/02/2020', 30118, 1282, 12, 347, 195352, 529, 9, 0, 6, 2872], ['Orlando Region', '08/02/2020', 29699, 848, 41, 234, 227153, 233, 9, 0, 2, 1717], ['Jacksonville Region', '08/02/2020', 21665, 625, 15, 158, 176530, 343, 0, 0, 1, 2389], ['Rest of Florida', '08/02/2020', 334, 19, 0, 3, 3106, 5, 0, 0, 0, 26], ['State', '08/02/2020', 487132, 27150, 374, 7084, 3233865, 7104, 178, 2, 62, 34450]]
    final_table = covidfl()
    # region_last_calcs = [['Region', 'Date', 'CasesAll', 'C_HospYes_Res', 'C_HospYes_NonRes', 'Deaths', 'T_negative', 'CasesAll_Chg', 'C_HospYes_Res_Chg', 'C_HospYes_NonRes_Chg', 'Deaths_Chg', 'T_negative_Chg'], ['Collier', '08/18/2020', 10977, 774, 15, 159, 55235, 59, 6, 0, 5, 389], ['Lee', '08/18/2020', 17495, 1229, 20, 384, 103744, 44, 17, 1, 9, 826], ['South Florida', '08/18/2020', 253643, 14470, 138, 4157, 1261713, 1517, 169, 1, 71, 8212], ['Tampa Bay Region', '08/18/2020', 53481, 3411, 36, 1060, 387058, 339, 27, 0, 15, 2215], ['Orlando Region', '08/18/2020', 59740, 3226, 63, 860, 401442, 375, 42, 0, 30, 2148], ['Jacksonville Region', '08/18/2020', 28857, 1013, 22, 280, 236617, 148, 21, 0, 11, 968]]
    region_last_calcs = final_table[0]
    region_table_calcs = final_table[1]
    date_max = final_table[2]
    print(date_max)
    rows = len(region_last_calcs) - 1
    columns = len(region_last_calcs[0])
    data_is_late = final_table[3]
    return render_template("index.html", region_last_calcs=region_last_calcs, region_table_calcs=region_table_calcs, rows=rows, date_max=date_max,data_is_late=data_is_late)

# @app.route('/Hello')
# def hello():
#     return "Hello World"

# @app.route('/members')
# def members():
#     return "Members"

# @app.route('/members/<name>/')
# def getMember(name):
#     return name