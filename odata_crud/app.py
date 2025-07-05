from flask import Flask,render_template,request,redirect,url_for,flash
import requests
import json
import base64

app = Flask(__name__, template_folder="templates")

@app.route("/", methods=['GET', 'POST'])
def homepage():
    username = 'DEVELOPER'
    password = 'ABAPtr2022#01'
    v_url = "http://vhcala4hci:50000/sap/opu/odata/sap/YPEGAWAI_SRV/PEGAWAISet?$format=json"
    response = requests.get(v_url, auth=(username, password)).content
    data = json.loads(response)
# Extract into list of dicts
    employee_list = []

    for entry in data['d']['results']:
        employee = {
            "Empid": entry['Empid'],
            "Empname": entry['Empname'],
            "Emppost": entry['Emppost'],
            "Empphoto": entry['Empphoto']
         }
        employee_list.append(employee)

    return render_template("index.html", data = employee_list)


@app.route('/readform')
def readform():
    if request.method == 'GET':
        empid = request.args.get("r_empid")
        empname = request.args.get("r_empname")
        emppost = request.args.get("r_emppost")
        empphoto = request.args.get("r_empphoto")
        myjson = json.dumps([{'Empid':empid, 'Empname':empname, 'Emppost':emppost, 'Empphoto':empphoto}])
        loaded_r = json.loads(myjson)
        print (loaded_r)
    return render_template("read.html", data = loaded_r)  


@app.route('/addform')
def addform():

    return render_template("create.html")

@app.route('/addpost', methods = ['POST'])
def addpost():
    if request.method == 'POST':
        empid = request.form["Empid"]
        empname = request.form["Empname"]
        emppost = request.form["Emppost"]
        empphoto = request.form["Empphoto"]        
        payload = json.dumps({"Empid": empid, "Empname": empname, "Emppost": emppost, "Empphoto": empphoto})  
        username = 'DEVELOPER'
        password = 'ABAPtr2022#01'          
        ## CSRF TOken Fetch###
        base_url = 'http://vhcala4hci:50000'
        csrf_sess = requests.session()
        csrf_sess.headers.update({'connection':'keep-alive'})        
        header = {
            'x-csrf-token':'fetch',
            'Authorization':f'Basic {base64.b64encode(f"{username}:{password}".encode()).decode()}',
            'Content-Type':'application/json'
        }
        csrf_url = f"{base_url}/sap/opu/odata/sap/YPEGAWAI_SRV/PEGAWAISet"
        csrf_params = {'x-csrf-token':'fetch'}
        csrf_call = csrf_sess.get(csrf_url,params=csrf_params,headers=header)

        token_header = csrf_call.headers
        #csrf_token = token_header['x-csrf-token']
        post_headers = token_header['x-csrf-token']
        headers2= {'Content-type': 'application/json;charset=utf-8', 'X-CSRF-TOKEN': post_headers}
        print(post_headers)
        print(payload)
        x = csrf_sess.post('http://vhcala4hci:50000/sap/opu/odata/sap/YPEGAWAI_SRV/PEGAWAISet', data=payload, headers=headers2, auth=(username, password))
        print(x)
        return redirect(url_for('homepage'))
    return render_template("create.html")
 

@app.route('/updateform', methods = ['POST', 'GET'])
def updateform():
    if request.method == 'GET':
        empid = request.args.get("u_empid")
        empname = request.args.get("u_empname")
        emppost = request.args.get("u_emppost")
        empphoto = request.args.get("u_empphoto")
        print(empid, empname)
        myjson = json.dumps([{'Empid':empid, 'Empname':empname, 'Emppost':emppost, 'Empphoto':empphoto}])
        loaded_r = json.loads(myjson)
        #return redirect(url_for('homepage'))
    return render_template("update.html", data = loaded_r)

@app.route('/updatepost', methods = ['POST'])
def updatepost():
    if request.method == 'POST':
        empid = request.form.get("empid")
        empname = request.form.get("empname")
        emppost = request.form.get("emppost")
        empphoto = request.form.get("empphoto")
        payload = json.dumps({"Empid": empid, "Empname": empname, "Emppost": emppost, "Empphoto": empphoto})
        print(payload)
        ## CSRF TOken Fetch###
        username = 'DEVELOPER'
        password = 'ABAPtr2022#01'          
        base_url = 'http://vhcala4hci:50000'
        csrf_sess = requests.session()
        csrf_sess.headers.update({'connection':'keep-alive'})        
        header = {
            'x-csrf-token':'fetch',
            'Authorization':f'Basic {base64.b64encode(f"{username}:{password}".encode()).decode()}',
            'Content-Type':'application/json'
        }
        csrf_url = f"{base_url}/sap/opu/odata/sap/YPEGAWAI_SRV/PEGAWAISet"
        csrf_params = {'x-csrf-token':'fetch'}
        csrf_call = csrf_sess.get(csrf_url,params=csrf_params,headers=header)

        token_header = csrf_call.headers
        csrf_token = token_header['x-csrf-token']
        post_headers = token_header['x-csrf-token']
        headers2= {'Content-type': 'application/json;charset=utf-8', 'X-CSRF-TOKEN': post_headers}
        print(post_headers)   
        x = csrf_sess.post('http://vhcala4hci:50000/sap/opu/odata/sap/YPEGAWAI_SRV/PEGAWAISet', data=payload, headers=headers2, auth=(username, password))             
        print(x)
        return redirect(url_for('homepage'))
    return render_template("update.html") 

@app.route('/deleteform', methods = ['POST', 'GET'])
def deleteform():
    if request.method == 'GET':
        empid = request.args.get("d_empid")
        empname = request.args.get("d_empname")
        emppost = request.args.get("d_emppost")
        empphoto = request.args.get("d_empphoto")
        #print (json.dumps({'productid': productid, 'name': name})
        #myjson = []
        myjson = json.dumps([{'Empid':empid, 'Empname':empname, 'Emppost':emppost, 'Empphoto':empphoto}])
        loaded_r = json.loads(myjson)
        #return redirect(url_for('homepage'))
    return render_template("delete.html", data = loaded_r)

@app.route('/deletepost', methods = ['POST'])
def deletepost():
    if request.method == 'POST':
        empid = request.form.get("empid")
        empname = request.form.get("empname")
        emppost = request.form.get("emppost")
        empphoto = request.form.get("empphoto")
        myjson = json.dumps({'Empid':empid})
        ## CSRF TOken Fetch###
        username = 'DEVELOPER'
        password = 'ABAPtr2022#01'          
        base_url = 'http://vhcala4hci:50000'
        csrf_sess = requests.session()
        csrf_sess.headers.update({'connection':'keep-alive'})        
        header = {
            'x-csrf-token':'fetch',
            'Authorization':f'Basic {base64.b64encode(f"{username}:{password}".encode()).decode()}',
            'Content-Type':'application/json'
        }
        csrf_url = f"{base_url}/sap/opu/odata/sap/YPEGAWAI_SRV/PEGAWAISet"
        csrf_params = {'x-csrf-token':'fetch'}
        csrf_call = csrf_sess.get(csrf_url,params=csrf_params,headers=header)

        token_header = csrf_call.headers
        csrf_token = token_header['x-csrf-token']
        post_headers = token_header['x-csrf-token']
        headers2= {'Content-type': 'application/json;charset=utf-8', 'X-CSRF-TOKEN': post_headers}
        print(post_headers)  
        empid = "'" + empid + "'"
        v_url = 'http://vhcala4hci:50000/sap/opu/odata/sap/YPEGAWAI_SRV/PEGAWAISet' + '(' + empid + ')'
        x = csrf_sess.delete(v_url, data=myjson, headers=headers2, auth=(username, password))             
        print(v_url)
        print(myjson)
        print(x)
        return redirect(url_for('homepage'))
    return render_template("delete.html")

if __name__ == "__main__":
    app.run()