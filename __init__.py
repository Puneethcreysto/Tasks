from flask import Flask, request, jsonify

app = Flask(__name__)

#employee = [
    # {"emp_id": 1, "name": "sathyan", "phone": "", "DOB": 65, "email":},
    # {"emp_id": 2, "name": "Australia", "phone": "Canberra", "area": 7617930},
    # {"emp_id": 3, "name": "Egypt", "phone": "Cairo", "area": 1010408},
    # {"emp_id": 4, "name": "USA", "phone": "WDC", "area": 1010405}
]


def _find_next_id():
    return max(country["id"] for country in countries) + 1



# @app.route('/', methods = ['GET'])
# def get_countries():
#     if(request.method == 'GET'):
#         return jsonify(countries)



    
# @app.route('/', methods = ['POST'])
# def add_country():
#     if(request.method == 'POST'):
#         try:
#             if request.is_json:
#                 country = request.get_json()
#                 country["id"] = _find_next_id()
#                 countries.append(country)
#                 return country, 201
#         except:
#             return {"error": "Request must be JSON"}, 415


@app.post("/countries")
def add_country():
    if request.is_json:
        country = request.get_json()
        country["id"] = _find_next_id()
        countries.append(country)
        return country, 201
    return {"error": "Request must be JSON"}, 415

if __name__ == '__main__':
  
    #app.run(debug = True)