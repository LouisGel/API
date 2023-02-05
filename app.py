from flask import Flask, make_response, jsonify, request
from apps.models.DatabaseManager import db
from apps.models.TablesManager import *

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    #Disable un Warning
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db?check_same_thread=False' #Le nom de la base de données
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
db.init_app(app)

@app.route("/")
async def index():
    return NOT_FOUND()

#!================================================================================================= USER
@app.route("/users", methods = ['GET', 'POST'])
async def users():
    if request.method == "GET":
        users = User.getAll();
        users_list = []
        for k in range(len(users)): users_list.append(users[k].toJson())
        return JSON(users_list)
    if request.method == "POST":
        data = request.get_json()
        fname = data["fname"]
        lname = data["lname"]
        email = data["email"]
        if not any([fname, lname, email]): return UNPROCESSABLE_ENTITY()
        if(User.exist(email)) : return CONFLICT()
        new_user = User(fname, lname, email)
        if not new_user.pushToDB(db) : return INTERNAL_SERVER_ERROR()
        return OK()

@app.route("/users/<id_user>", methods = ['GET'])
async def user(id_user):
    user = User.getById(id_user)
    if(user == None) : return NOT_FOUND()
    return JSON(user.toJson())


#!================================================================================================= ACCOMPLISSEMENT
@app.route("/accomplissements", methods = ['GET', 'POST'])
async def accomplissements():
    if request.method == "GET":
        accomplissements = Accomplissement.getAll();
        accomplissements_list = []
        for k in range(len(accomplissements)): accomplissements_list.append(accomplissements[k].toJson())
        return JSON(accomplissements_list)
    if request.method == "POST":
        data = request.get_json()
        label = data["label"]
        description = data["description"]
        exp_value = int(data["exp_value"])
        if not any([label, description, exp_value]): return UNPROCESSABLE_ENTITY()
        new_accomplissement = Accomplissement(label, description, exp_value)
        if not new_accomplissement.pushToDB(db) : return INTERNAL_SERVER_ERROR()
        return OK()

@app.route("/accomplissements/<id_accomplissement>", methods = ['GET'])
async def accomplissement(id_accomplissement):
    accomplissements = Accomplissement.getById(id_accomplissement)
    if(accomplissements == None) : return NOT_FOUND()
    return JSON(accomplissements.toJson())


#!================================================================================================= TODO
@app.route("/todos", methods = ['GET', 'POST'])
async def todos():
    if request.method == "GET":
        todos = Todo.getAll();
        todo_list = []
        for k in range(len(todos)): todo_list.append(todos[k].toJson())
        return JSON(todo_list)
    if request.method == "POST":
        data = request.get_json()
        id_user = int(data["id_user"])
        id_accomplissement = int(data["id_accomplissement"])
        id_state = int(data["id_state"])
        if not User.getById(id_user): return UNPROCESSABLE_ENTITY()
        print("Bob1")
        if not Accomplissement.exist(id_accomplissement) : return UNPROCESSABLE_ENTITY()
        print("Bob2")
        if not State.exist(id_state) : return UNPROCESSABLE_ENTITY()
        print("Bob3")
        if not any([id_user, id_accomplissement, id_state]): return UNPROCESSABLE_ENTITY()
        new_todo = Todo(id_user, id_accomplissement, id_state)
        if not new_todo.pushToDB(db) : return INTERNAL_SERVER_ERROR()
        return OK()

@app.route("/todos/<id_todo>", methods = ['GET', 'PUT'])
async def todo(id_todo):
    if request.method == "GET":
        todo = Todo.getById(id_todo)
        if(todo == None) : return NOT_FOUND()
        return JSON(todo.toJson())
    if request.method == "PUT":
        todo = Todo.getById(id_todo)
        if todo == None : return UNPROCESSABLE_ENTITY()
        print("============================================================")
        print(todo.finish_date)
        if todo.finish_date != None : return UNPROCESSABLE_ENTITY()
        if not todo.finished() : return INTERNAL_SERVER_ERROR()
        return OK()



#!================================================================================================= STATE
@app.route("/states", methods = ['GET', 'POST'])
async def states():
    if request.method == "GET":
        states = State.getAll();
        state_list = []
        for k in range(len(states)): state_list.append(states[k].toJson())
        return JSON(state_list)
    if request.method == "POST":
        data = request.get_json()
        label = data["label"]
        description = data["description"]
        if not any([label, description]): return UNPROCESSABLE_ENTITY()
        new_state = State(label, description)
        if not new_state.pushToDB(db) : return INTERNAL_SERVER_ERROR()
        return OK()

@app.route("/states/<id_states>", methods = ['GET'])
async def state(id_states):
    state = State.getById(id_states)
    if(state == None) : return NOT_FOUND()
    return JSON(state.toJson())


#=========================================================================#
#                                FUNCTION                                 #
#=========================================================================#
def NOT_FOUND(): return make_response(jsonify({}), 403)
def UNPROCESSABLE_ENTITY(): return make_response(jsonify({}), 422)
def CONFLICT(): return make_response(jsonify({}), 409)
def INTERNAL_SERVER_ERROR(): return make_response(jsonify({}), 500)
def JSON(json): return make_response(jsonify(json), 200)
def OK(): return make_response(jsonify(status=200), 200)


#=========================================================================#
#                                   APP                                   #
#=========================================================================#
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

#Permet de créer la BD si elle n'existe pas
with app.app_context():
    db.create_all()