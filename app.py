from Sherbot_test import getcanvas
from flask import Flask, render_template, redirect, url_for, request
from form import EnvDescriptionForm

print (Sherbot_test.getcanvas("env"))
app=Flask(__name__)
app.config["SECRET_KEY"] = "mysecret"


@app.route('/', methods=['GET','POST'])
def index():
    env_form = EnvDescriptionForm(csrf_enabled=False)
    if env_form.validate_on_submit():
        env=env_form.env_description.data
        #input=Sherbot.getinput(env)
        #output=Sherbot.getoutput(env)
        canvas=Sherbot_test.getcanvas(env)
    return render_template("index.html",canvas=canvas)



if __name__=="__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)




    