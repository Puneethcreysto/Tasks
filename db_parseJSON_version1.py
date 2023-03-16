from flask import Flask,request,jsonify
import DB_Connection as db
from functools import wraps
import protected_test as test

import datetime

from flask_jwt_extended import (create_access_token,create_refresh_token,get_jwt_identity,jwt_required,JWTManager)


app=Flask(__name__)

##################################Api header ###########################
registration_header_key = 'e5dadf6524624f79c3127e247f04b548'


################################## JWT access ####################
app.config["JWT_SECRET_KEY"] = "Be-positive"  # Change this!

#app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(seconds=60)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(minutes=60)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = datetime.timedelta(minutes=50)

jwt = JWTManager(app)

######################################## Registration ##########################

@app.route('/register',methods=['POST'])
def register():
    
    try:
        auth_key= request.headers['api_key']
        
        if auth_key == registration_header_key:
            
            try:
                req=request.get_json()
                user_name=req['user_name']
                phone_no=req['phone_no']
                user_email=req['user_email']
                created_on=req['created_on']
                is_active=req['is_active']
                my_pw=req['password']
                d_salt=test.getDynamicSalt()
                h_password=test.generatePassword(my_pw,d_salt)
                
                query2="INSERT INTO user_employee_table(user_name, phone_no, user_email,created_on, is_active, d_salt, h_password)VALUES( '"+str(user_name)+"','"+str(phone_no)+"','"+str(user_email)+"', '"+str(created_on)+"', '"+str(is_active)+"', '"+str(d_salt)+"', '"+str(h_password)+"');"
                
                result=db.dbTransactionIUD(query2)
                return result
            except:
                return "can't register"
        else:
            return jsonify({"can't verify"})
    except:
        return jsonify({"error"})

####################################### LOGIN  ################################

@app.route("/login", methods=["POST"])
def login():
    try:
        auth_key= request.headers['api_key']
        
        if auth_key == registration_header_key:

            try:
                req=request.get_json()
                user_email=req['user_email']
                password=req['my_pw']
                
                d_salt_query="SELECT d_salt FROM user_employee_table WHERE user_email='"+str(user_email)+"';"
            
                d_salt=db.dbTransactionSelect(d_salt_query)
            
                d_salt=d_salt[0]['d_salt']
            

                hash_query="SELECT h_password FROM user_employee_table WHERE user_email='"+str(user_email)+"';"
                
                h_password=db.dbTransactionSelect(hash_query)
                
                h_password=h_password[0]['h_password']
                
                check=test.checkPassword(password,h_password,d_salt)
                
                if check==0:
                    return "Check Your password again" 
                else:
                    #return "login successful"
                    access_token = create_access_token(identity= user_email)
                    refresh_token = create_refresh_token(identity= user_email)
                    return jsonify(access_token=access_token, refresh_token=refresh_token)
                
            except:
                return "wrong data"
        else:
            return jsonify({"can't login"})
    except:
        return jsonify({"error"})
    
################################ Refresh Token #######################
@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)


################################# logout #####################
@app.route("/logout", methods=["POST"])
@jwt_required(refresh=True)
def logout():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    
    return jsonify(access_token=access_token)


##############################Motivator#######################################
@app.route("/add_motivator",methods=['POST'])
@jwt_required()
def motivator():
    req=request.get_json()
   
    motivator_type=req['motivator_type']
    
    query1="INSERT INTO motivator_1(motivator_type) VALUES('"+str(motivator_type)+"');" 
    result=db.dbTransactionIUD(query1)
    return jsonify(result)


@app.route("/show_motivator",methods=['GET'])
@jwt_required()
def show_motivator():
    
    query1="SELECT motivator_type FROM motivator_1"
    result=db.dbTransactionSelect(query1)
    return jsonify(result)


@app.route("/addmotivator_response",methods=['POST'])
@jwt_required()
def motivator_res():
    req=request.get_json()
    ref_id_from1=req['ref_id_from1']
    motivator_response=req['motivator_response']
    
    query1="INSERT INTO motivator_response_2(ref_id_from1,motivator_response) VALUES('"+str(ref_id_from1)+"','"+str(motivator_response)+"');" 
    result=db.dbTransactionIUD(query1)
    return jsonify(result)


@app.route("/show_motivator_response",methods=['GET'])
@jwt_required()
def show_motivator_response():
    req=request.get_json()
    ref_id_from1=req['ref_id_from1']
    
    query1="SELECT motivator_response FROM motivator_response_2 WHERE ref_id_from1='"+str(ref_id_from1)+"';"
    result=db.dbTransactionSelect(query1)
    return jsonify(result)

@app.route("/delete_motivator_response",methods=['POST'])
@jwt_required()
def delete_motivator_response():
    req=request.get_json()
    motivator_response=req['motivator_response']
    query="DELETE FROM motivator_response_2 WHERE motivator_response='"+str(motivator_response)+"';"
    result=db.dbTransactionIUD(query)
    return result

###############################################call_incoming/outgoing##############################

@app.route("/add_call_type",methods=['POST'])
@jwt_required()
def add_call_type():
    req=request.get_json()
   
    call_type=req['call_type']
    
    query1="INSERT INTO call_table1(call_type) VALUES('"+str(call_type)+"');" 
    result=db.dbTransactionIUD(query1)
    return jsonify(result)

@app.route("/show_call_type",methods=['GET'])
@jwt_required()
def show_call_type():
    
    query1="SELECT call_id,call_type FROM call_table1"
    result=db.dbTransactionSelect(query1)
    return jsonify(result)

##############################################call_level2#######################################

@app.route("/add_call_level2",methods=['POST'])
@jwt_required()
def add_call_level2():
    req=request.get_json()
    call_id=req['call_id']
    response_type=req['response_type']
    
    query1="INSERT INTO call_level2(call_id,response_type) VALUES('"+str(call_id)+"','"+str(response_type)+"');" 
    result=db.dbTransactionIUD(query1)
    return jsonify(result)

@app.route("/show_call_level2",methods=['GET'])
@jwt_required()
def show_call_level2():
    req=request.get_json()
    call_id=req['call_id']
    #response_type=req['response_type']

    
    query="SELECT level2_id,call_id,response_type FROM call_level2 WHERE call_id="+str(call_id)+";"
    #query="SELECT type FROM going_response_table WHERE call_id="+str(id)+" AND going_id="+str(contact_id)+";"
    #query1="SELECT response_type FROM call_level2"
    result=db.dbTransactionSelect(query)
    return jsonify(result)



@app.route("/delete_level2",methods=['POST'])
@jwt_required()
def delete_level2():
    req=request.get_json()
    response_type=req['response_type']
    query="DELETE FROM call_level2 WHERE response_type='"+str(response_type)+"';"
    result=db.dbTransactionIUD(query)
    return result
    
##############################################call_level3#######################################

@app.route("/add_call_level3",methods=['POST'])
@jwt_required()
def add_call_level3():
    req=request.get_json()

    call_id=req['call_id']
    level2_id=req['level2_id']
    response_type=req["response_type"]
    
    query1="INSERT INTO call_level3(call_id,level2_id,response_type) VALUES('"+str(call_id)+"','"+str(level2_id)+"','"+str(response_type)+"');" 
    #q="INSERT INTO going_promise_table(call_id,going_id,response_id,type) VALUES("+str(id)+","+str(contact_id)+","+str(response_id)+",'"+str(req['type'])+"');"
    result=db.dbTransactionIUD(query1)
    return jsonify(result)
    
@app.route("/show_call_level3",methods=['GET'])
@jwt_required()
def show_call_level3():
    
    req=request.get_json()
    call_id=req['call_id']
    level2_id=req['level2_id']

    query="SELECT level3_id,call_id,level2_id,response_type FROM call_level3 WHERE call_id="+str(call_id)+" AND level2_id="+str(level2_id)+";"
    
    result=db.dbTransactionSelect(query)
    return jsonify(result)


@app.route("/delete_level3",methods=['POST'])
@jwt_required()
def delete_level3():
    req=request.get_json()
    response_type=req['response_type']
    query="DELETE FROM call_level3 WHERE response_type='"+str(response_type)+"';"
    result=db.dbTransactionIUD(query)
    return result
    


############################################## call_level4 #######################################

@app.route("/add_call_level4",methods=['POST'])
@jwt_required()
def add_call_level4():

    req=request.get_json()

    call_id=req['call_id']
    level2_id=req['level2_id']
    level3_id=req['level3_id']
    response_type=req["response_type"]
    
    query1="INSERT INTO call_level4(call_id,level2_id,level3_id,response_type) VALUES('"+str(call_id)+"','"+str(level2_id)+"','"+str(level3_id)+"','"+str(response_type)+"');" 
    #q="INSERT INTO going_promise_table(call_id,going_id,response_id,type) VALUES("+str(id)+","+str(contact_id)+","+str(response_id)+",'"+str(req['type'])+"');"
    result=db.dbTransactionIUD(query1)
    return jsonify(result)
    

@app.route("/show_call_level4",methods=['GET'])
@jwt_required()
def show_call_level4():
    
    req=request.get_json()
    call_id=req['call_id']
    level2_id=req['level2_id']
    level3_id=req['level3_id']

    query="SELECT call_id,level2_id,level3_id,response_type FROM call_level4 WHERE call_id="+str(call_id)+" AND level2_id="+str(level2_id)+" AND level3_id="+str(level3_id)+";"
    
    result=db.dbTransactionSelect(query)
    return jsonify(result)


@app.route("/delete_level4",methods=['POST'])
@jwt_required()
def delete_level4():
    req=request.get_json()
    response_type=req['response_type']
    query="DELETE FROM call_level4 WHERE response_type='"+str(response_type)+"';"
    result=db.dbTransactionIUD(query)
    return result



if __name__ == "__main__":
    app.run()

