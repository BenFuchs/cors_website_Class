from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

con = sqlite3.connect("garage.db", check_same_thread=False)
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS cars('Color', 'Model', 'Brand')")
app = Flask(__name__)
CORS(app)

@app.route("/", methods=['post'])
def add_Car():
    new_car = request.get_json()
    print(new_car['Color'])
    cColor = new_car['Color']
    cModel = new_car['Model']
    cBrand = new_car['Brand']
    cur.execute("INSERT INTO cars Values(?, ?, ?)", (cColor, cModel, cBrand))
    con.commit()
    return new_car

from flask import jsonify

@app.route("/showCars")
def show_all_cars():
    cur.execute("SELECT ROWID, * FROM cars")
    temp = cur.fetchall()
    
    car_list = []
    for i in temp:
        car = {
            'rowid': i[0],
            'Color': i[1],
            'Model': i[2],
            'Brand': i[3]
        }
        car_list.append(car)
    
    return jsonify(car_list)

@app.route("/delCar/<int:car_id>", methods=["delete"])
def del_Car(car_id):
   cur.execute("DELETE FROM cars WHERE ROWID = ?", (car_id,))
   con.commit()
   return jsonify({"message": "Car deleted successfully"})

@app.route("/updCar/<int:car_id>", methods=["put"])
def update_car(car_id):
    data = request.get_json()
    if "Color" in data and "Model" in data and "Brand" in data:
        nColor = data["Color"]
        nModel = data["Model"]
        nBrand = data["Brand"]

    cur.execute("UPDATE cars SET Color = ?, Model = ?, Brand = ? WHERE ROWID = ?", (nColor, nModel, nBrand, car_id))
    con.commit()
    return jsonify({"message": "Car updated"})