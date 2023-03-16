from flask import Flask,request,jsonify
import DB_Connection as db

app=Flask(__name__)


##############################Motivator#######################################
@app.route("/add_motivator",methods=['POST'])
def motivator():
    req=request.get_json()
   
    motivator_type=req['motivator_type']
    
    query1="INSERT INTO motivator_1(motivator_type) VALUES('"+str(motivator_type)+"');" 
    result=db.dbTransactionIUD(query1)
    return jsonify(result)


@app.route("/show_motivator",methods=['GET'])
def show_motivator():
    
    query1="SELECT motivator_type FROM motivator_1"
    result=db.dbTransactionSelect(query1)
    return jsonify(result)


@app.route("/addmotivator_response",methods=['POST'])
def motivator_res():
    req=request.get_json()
    ref_id_from1=req['ref_id_from1']
    motivator_response=req['motivator_response']
    
    query1="INSERT INTO motivator_response_2(ref_id_from1,motivator_response) VALUES('"+str(ref_id_from1)+"','"+str(motivator_response)+"');" 
    result=db.dbTransactionIUD(query1)
    return jsonify(result)


@app.route("/show_motivator_response",methods=['GET'])
def show_motivator_response():
    req=request.get_json()
    ref_id_from1=req['ref_id_from1']
    
    query1="SELECT motivator_response FROM motivator_response_2 WHERE ref_id_from1='"+str(ref_id_from1)+"';"
    result=db.dbTransactionSelect(query1)
    return jsonify(result)

@app.route("/delete",methods=['POST'])
def delete():
    req=request.get_json()
    motivator_response=req['motivator_response']
    query="DELETE FROM motivator_response_2 WHERE motivator_response='"+str(motivator_response)+"';"
    result=db.dbTransactionIUD(query)
    return result

###############################################call_incoming/outgoing##############################

@app.route("/add_call_type",methods=['POST'])
def add_call_type():
    req=request.get_json()
   
    call_type=req['call_type']
    
    query1="INSERT INTO call_table1(call_type) VALUES('"+str(call_type)+"');" 
    result=db.dbTransactionIUD(query1)
    return jsonify(result)

@app.route("/show_call_type",methods=['GET'])
def show_call_type():
    
    query1="SELECT call_type FROM call_table1"
    result=db.dbTransactionSelect(query1)
    return jsonify(result)

##############################################call_level2#######################################

@app.route("/add_call_level2",methods=['POST'])
def add_call_level2():
    req=request.get_json()
    call_id=req['call_id']
    response_type=req['response_type']
    
    query1="INSERT INTO call_level2(call_id,response_type) VALUES('"+str(call_id)+"','"+str(response_type)+"');" 
    result=db.dbTransactionIUD(query1)
    return jsonify(result)

@app.route("/show_call_level2",methods=['GET'])
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
def delete_level2():
    req=request.get_json()
    response_type=req['response_type']
    query="DELETE FROM call_level2 WHERE response_type='"+str(response_type)+"';"
    result=db.dbTransactionIUD(query)
    return result
    
##############################################call_level3#######################################

@app.route("/add_call_level3",methods=['POST'])
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
def show_call_level3():
    
    req=request.get_json()
    call_id=req['call_id']
    level2_id=req['level2_id']

    query="SELECT level3_id,call_id,level2_id,response_type FROM call_level3 WHERE call_id="+str(call_id)+" AND level2_id="+str(level2_id)+";"
    
    result=db.dbTransactionSelect(query)
    return jsonify(result)


@app.route("/delete_level3",methods=['POST'])
def delete_level3():
    req=request.get_json()
    response_type=req['response_type']
    query="DELETE FROM call_level3 WHERE response_type='"+str(response_type)+"';"
    result=db.dbTransactionIUD(query)
    return result
    


############################################## call_level4 #######################################

@app.route("/add_call_level4",methods=['POST'])
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
def show_call_level4():
    
    req=request.get_json()
    call_id=req['call_id']
    level2_id=req['level2_id']
    level3_id=req['level3_id']

    query="SELECT call_id,level2_id,level3_id,response_type FROM call_level4 WHERE call_id="+str(call_id)+" AND level2_id="+str(level2_id)+" AND level3_id="+str(level3_id)+";"
    
    result=db.dbTransactionSelect(query)
    return jsonify(result)


@app.route("/delete_level4",methods=['POST'])
def delete_level4():
    req=request.get_json()
    response_type=req['response_type']
    query="DELETE FROM call_level4 WHERE response_type='"+str(response_type)+"';"
    result=db.dbTransactionIUD(query)
    return result


if __name__=="__main__":
    app.run()








































# req=request.get_json()
    # call_type=req['call_type']
    # level2_response_type=req["level2_response_type"]
    # level3_response_type=req["level3_response_type"]
    # response_type=req["response_type"]
    
    # call_idq="SELECT call_id FROM call_table1 WHERE call_type='"+str(call_type)+"';"
    # call_id=db.dbTransactionSelect(call_idq)
    # call_id=call_id[0]['call_id']

    # level2_idq="SELECT level2_id FROM call_level2 WHERE response_type='"+str(level2_response_type)+"';"
    # level2_id=db.dbTransactionSelect(level2_idq)
    # level2_id=level2_id[0]['level2_id']

    # level3_idq="SELECT level3_id FROM call_level3 WHERE response_type='"+str(level3_response_type)+"';"
    # level3_id=db.dbTransactionSelect(level3_idq)
    # level3_id=level3_id[0]['level3_id']

    
    
    # q="INSERT INTO call_level4(call_id,level2_id,level3_id,response_type)VALUES ('"+str(call_id)+"','"+str(level2_id)+"','"+str(level3_id)+"','"+str(response_type)+"');"
    # result=db.dbTransactionIUD(q)
    # return jsonify(result)