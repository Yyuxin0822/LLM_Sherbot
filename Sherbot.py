from Sherbot_simpleflow import getcanvas,returninput,returnsimpleflow,returnsystem,color,simplematrix
from Sherbot_complexflow import complexflowtojson,logtoJson
from Sherbot_inspireflow import inspireflowtojson
import os
import openai
from config import OPENAI_API_KEY

def getcanvas_main(env):
    canvas=getcanvas(env)
    return canvas


def simpleflow_main(env):
    input=(returninput(env))
    print(input)
    print("\n")
    output=(returnsimpleflow(input))
    print(output)
    print("\n")
    system=(returnsystem(output))
    print(system)
    print("\n")
    colordict=(color(system))
    print(colordict)
    print("\n")
    matrixdict=(simplematrix(output))
    print(matrixdict)

    # clear json files
    with open('static/complex/flowtree.json', 'w') as f:
        f.write("[]")
    with open('static/complex/matrix.json', 'w') as f:
        f.write("[]")
    with open('static/complex/sample.json', 'w') as f:
        f.write("[]")
    with open('static/complex/samplecolor.json', 'w') as f:
        f.write("[]")
    with open('static/message/sherbotmessage.json', 'w') as f:
        f.write("[]")


def complexflow_main(simpleflow):
    with open('static/complex/flowtree.json', 'w') as f:
        f.write("[]")
    with open('static/complex/matrix.json', 'w') as f:
        f.write("[]")
    with open('static/complex/sample.json', 'w') as f:
        f.write("[]")
    with open('static/complex/samplecolor.json', 'w') as f:
        f.write("[]")

    complexflowtojson(simpleflow,refopt="input")



def inspirationflow_main(ele):
    with open('static/inquire/flowtree.json', 'w') as f:
        f.write("[]")
    with open('static/inquire/matrix.json', 'w') as f:
        f.write("[]")
    with open('static/inquire/sample.json', 'w') as f:
        f.write("[]")
    with open('static/inquire/samplecolor.json', 'w') as f:
        f.write("[]")
        
    inspireflowtojson(ele)


def inquiresys_main(ele):
    with open('static/inquire/sample_usersys.json', 'w') as f:
        f.write("[]")
    with open('static/inquire/samplecolor_usersys.json', 'w') as f:
        f.write("[]")

    systemdict=returnsystem(path="static/inquire/sample_usersys.json",inputelement=ele)
    colordict=color(systemdict,path="static/inquire/samplecolor_usersys.json")




if __name__=="__main__":
    pass
    # test=["TIDAL ENERGY","WATER SUPPLY","IRRIGATION","RESERVOIR","FLOODWATER","BIOMASS","WIND TURBINE"]
    # inquiresys_main(test)