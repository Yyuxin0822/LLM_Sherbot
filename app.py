from Sherbot_v1 import getcanvas,getinput,getoutput,getinputlist,getoutputlist,flowdict,categorize,color
from flask import Flask, render_template, redirect, url_for, request
from form import EnvDescriptionForm
import json

app=Flask(__name__,static_folder="static", template_folder='templates')
app.config["SECRET_KEY"] = "mysecret"

canvas={0:""}
envD={0:""}
resultD={0:""}
colorD={0:""}

@app.route('/', methods=['GET','POST'])
def index(id=0):
    env_form = EnvDescriptionForm(csrf_enabled=False)
    if env_form.validate_on_submit():
        env=env_form.env_description.data
        id=len(canvas)
        envD[id]=env
        result=flowdict(getoutput(env))
        resultD[id]=result
        colorD[id]= color(categorize(result))
        #inputD[id]=getinputlist(result)
        #outputD[id]=getoutputlist(result)
        canvas[id]=getcanvas(env)
        return redirect(url_for('index',id=id))
    id=len(canvas)-1
    return render_template("index.html",env=envD[id],result=resultD[id],canvas=canvas[id],color=colorD[id],temp_form=env_form)

if __name__=="__main__":
    app.run(debug=True)
    #app.run(host='0.0.0.0', port=5000, debug=True)




    