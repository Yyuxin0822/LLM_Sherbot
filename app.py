from Sherbot_test import getcanvas,getinput,getoutput
from flask import Flask, render_template, redirect, url_for, request
from form import EnvDescriptionForm


app=Flask(__name__)
app.config["SECRET_KEY"] = "mysecret"

canvas={0:""}
envD={0:""}
inputD={0:""}
outputD={0:""}


@app.route('/', methods=['GET','POST'])
def index(id=0):
    env_form = EnvDescriptionForm(csrf_enabled=False)
    if env_form.validate_on_submit():
        env=env_form.env_description.data
        id=len(canvas)
        envD[id]=env
        inputD[id]=getinput(env)
        outputD[id]=getoutput(env)
        canvas[id]=getcanvas(env)
        return redirect(url_for('index',id=id))
    id=len(canvas)-1
    return render_template("index.html",env=envD[id],input=inputD[id],output=outputD[id],canvas=canvas[id],temp_form=env_form)

if __name__=="__main__":
    app.run(debug=True)
    #app.run(host='0.0.0.0', port=5000, debug=True)




    