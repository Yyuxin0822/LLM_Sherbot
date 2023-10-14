from Sherbot import simpleflow_main,complexflow_main,getcanvas_main,inspirationflow_main,inquiresys_main,logtoJson
from flask import Flask, render_template, redirect, url_for,jsonify,request
from form import EnvDescriptionForm
import json
from datetime import datetime

app=Flask(__name__,static_folder="static", template_folder='templates')
app.config["SECRET_KEY"] = "mysecret"

envD={0:""}
canvas={0:""}
resultD={0:""}
flowD={0:""}
systemD={0:""}
colorD={0:""}
matrixD={0:""}

@app.route('/', methods=['GET','POST'])
def index(id=0):
    env_form = EnvDescriptionForm(csrf_enabled=False)
    if env_form.validate_on_submit():
        env=env_form.env_description.data
        id=len(canvas)
        envD[id]=env

        #getcanvasD
        canvas[id]=getcanvas_main(env)
        simpleflow_main(env)

        return redirect(url_for('index',id=id))
    id=len(canvas)-1
    return render_template("index.html",env=envD[id],canvas=canvas[id],temp_form=env_form)

@app.route('/inquire_data', methods=['POST'])
def inquire_data():
    data = request.get_json()
    # convert data to dictionary
    # result=json.load(data)
    result_flow=data["toinquireFlow"]
    result_element=data["toinquireElement"]
    result_system=data["toinquireSystem"]
    
    messagefilepath="static/message/sherbotmessage.json"
    now = datetime.now()
    formatted_time = now.strftime("%H:%M:%S")


    logtoJson("--------(Time of This Ask:"+formatted_time+")--------- \n",messagefilepath)
    logtoJson("--------(Time of This Ask:"+formatted_time+")--------- \n",messagefilepath)
    logtoJson("Hi! I am Sherbot! \n",messagefilepath)

    if result_flow:
        complexflow_main(result_flow)
    if result_element:
        inspirationflow_main(result_element)
    if result_system:
        inquiresys_main(result_system)
    return jsonify(data)

@app.route('/regenerate_image', methods=['POST'])
def regenerate_image():
    data=request.get_json()
    if data["image"]:
        url=getcanvas_main(data["image"])
    dicturl={"url":url}
    return jsonify(dicturl)

if __name__=="__main__":
    app.run(debug=True)
    #app.run(host='0.0.0.0', port=5000, debug=True)




    