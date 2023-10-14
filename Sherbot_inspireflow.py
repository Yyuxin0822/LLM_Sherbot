import os
import json
import re
import random
import urllib
import openai
import langchain
from langchain.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from Sherbot_simpleflow import returnsystem,color,classify
from Sherbot_complexflow import convertflow,checknestedlist,logtoJson



os.environ["HUGGINGFACEHUB_API_TOKEN"] =  "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"
os.environ["OPENAI_API_KEY"] = "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"
openai.api_key = "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"
# "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"
######################################################
######################################################
#Task 2.1 - Minimum Version of Flow Generation
#Generate input from environment description
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

#Generate inquire
def getinquire(element,randomNumber=4):
    insertstring=f'{element}'
    print(f'insertstring is {insertstring}')
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {
            "role": "system",
            "content": "You are to help me come up with environmental flows that contain the elements I provided.\n\nFirst, please try to use as multiple elements in one flow. \n\nSecond, please try to build circular flow with given elements.\n\nLastly, organize your thoughts in an array of jsons.\n\n\n"
            },
            {
            "role": "user",
            "content": "['RESERVOIR', 'FLOODWATER', 'BIOMASS', 'IRRIGATION', 'WATER SUPPLY', 'WIND TURBINE']"
            },
            {
            "role": "assistant",
            "content": "First, Using Multiple Elements in One Flow:\n\n        1.  Reservoir + Irrigation + Biomass: The reservoir stores water which is then used for irrigation. The irrigated fields support the growth of biomass.\n            Flow Outcome: \"Enhanced Agricultural Productivity\"\n         \n        2.  Wind Turbine + Floodwater: Wind turbines harness wind energy to pump floodwater to storage or treatment facilities.\n            Flow Outcome: \"Energy-driven Floodwater Management\"\n        \n        3.  Water Supply + Biomass: The water supply is used to irrigate fields, where biomass is grown. This biomass can be used as feedstock.\n            Flow Outcome: \"Biomass Feedstock Production\"\n\n        4.  Reservoir + Floodwater + Water Supply: Reservoirs store floodwater, ensuring steady water supply during droughts.\n            Flow Outcome: \"Drought Resilience\"\n         \n        5.  Biomass + Wind Turbine: Biomass is converted into biofuel. Wind turbines produce electricity. Both provide alternative energy sources.\n            Flow Outcome: \"Diversified Renewable Energy\"\n\n        6.  Irrigation + Water Supply + Reservoir: Water from reservoirs is distributed to fields through irrigation, ensuring water supply is effectively utilized.\n            Flow Outcome: \"Optimized Agricultural Water Use\"\n        ##\n\nSecond, Circular Flows with the Given Elements:\n        \n        1.  Water Cycle with Energy Input\n            Flow: \"Water Supply\" -> \"Irrigation\" -> \"Biomass\" (acts as a sponge, aiding in groundwater recharge) -> \"Enhanced Groundwater Recharge\" -> \"Water Supply\"\n            Add-On: \"Wind Turbine\" powers the water distribution systems, and \"Biomass\" can be converted into bioenergy to supplement the wind turbine during non-windy days.\n        \n        2.  Reservoir Management Cycle\n            Flow: \"Reservoir\" (stores water) -> \"Floodwater\" (controlled release during floods) -> \"Irrigation\" (provides water to crops) -> \"Biomass\" (grown crops) -> \"Bioenergy Production\" -> \"Reservoir\" (bioenergy powers water treatments & distribution)\n            Add-On: \"Wind Turbine\" powers reservoir management systems, complementing the energy derived from biomass.\n        \n        3.  Sustainable Water-Energy Nexus\n            Flow: \"Water Supply\" (used in cooling and processing) -> \"Wind Turbine\" (produces electricity) -> \"Biomass Feedstock Processing\" (using electricity) -> \"Bioenergy\" -> \"Water Desalination or Purification\" -> \"Water Supply\"\n            Add-On: The \"Reservoir\" can act as storage, ensuring a consistent water supply.\n\nLastly, organized as:\n        [[\"RESERVOIR\", \"ENHANCED AGRICULTURAL PRODUCTIVITY\"],\n         [\"IRRIGATION\", \"ENHANCED AGRICULTURAL PRODUCTIVITY\"],\n         [\"BIOMASS\", \"ENHANCED AGRICULTURAL PRODUCTIVITY\"],\n         [\"WATER SUPPLY\", \"IRRIGATION\",\"BIOMASS\",\"ENHANCED GROUND WATER RECHARGE,\"\"WATER SUPPLY\"]]"
            },
            {
            "role": "user",
            "content": "This is awesome let's try another: ['VILLAGE','SOIL FERTILITY','MOUNTAINOUS TERRAIN']. Please combine the explanation and outcome steps you had above."
            },
            {
            "role": "assistant",
            "content": " Element Co-optimization:\n         \"1.Village + Mountainous Terrain: Villages located in mountainous terrains adapt unique ways of living, often relying on the natural resources available in the mountains.\n            Flow Outcome: \"Mountain Community Living\"\n        \n        2.  Village + Soil Fertility: Villages rely on agriculture as a primary means of livelihood, and fertile soil directly influences their agricultural productivity.\n            Flow Outcome: \"Agricultural Productivity\"\n        \n        3.  Soil Fertility + Mountainous Terrain: In mountainous terrains, terraced farming is a common agricultural practice that utilizes the fertile soil in layers.\n            Flow Outcome: \"Terraced Farming\"\n        \n        The circular flows represent how villages, with their reliance on agricultural productivity, can be influenced by the geographical and soil conditions, creating a cyclical relationship between the land, its fertility, and the inhabitants.\n        \n        Organized as:\n         [[\"VILLAGE\", \"MOUNTAIN COMMUNITY LIVING\"],[\"MOUNTAINOUS TERRAIN\", \"MOUNTAIN COMMUNITY LIVING\"],\n          [\"VILLAGE\", \"AGRICULTURAL PRODUCTIVITY\"],[\"SOIL FERTILITY\", \"AGRICULTURAL PRODUCTIVITY\"]\n          [\"SOIL FERTILITY\", \"TERRACED FARMING\"],[\"MOUNTAINOUS TERRAIN\", \"TERRACED FARMING\"]\n         \n         [\"VILLAGE\", \"MOUNTAINOUS TERRAIN\", \"TERRACED FARMING\", \"SOIL FERTILITY\", \"VILLAGE\"]\n         [\"SOIL FERTILITY\", \"MOUNTAINOUS TERRAIN\", \"VILLAGE\", \"AGRICULTURAL PRODUCTIVITY\", \"SOIL FERTILITY\"]]"
            },
            {
            "role": "user",
            "content": "This is great, keep this format and try another one: [\"GEOLOGICAL RESOURCES\",\"MOUNTAINOUS TERRAIN\",  \"TERRACED FARMING\"]"
            },
            {
            "role": "assistant",
            "content": " Element Co-optimization:\n        \"1. Geological Resources + Mountainous Terrain: The mountainous terrains often harbor a wealth of geological resources which can be extracted for various purposes.\n            Flow Outcome: \"Resource Extraction\"\n\n        2.  Geological Resources + Terraced Farming: Geological resources, like minerals, can enhance the quality of the terraced fields, providing essential nutrients.\n            Flow Outcome: \"Terrain Enrichment\"\n        \n        3.  Mountainous Terrain + Terraced Farming: The inherent structure of mountainous terrains allows for the formation of terraces, facilitating agriculture on slopes.\n            Flow Outcome: \"Terraced Agriculture\"\n\n        The circular flows depict the symbiotic relationship between geological resources, the structure of the mountainous terrains, and the practice of terraced farming. Each element aids and sustains the other, creating a holistic cycle of enrichment and sustainability.\n        \n        Organized as:\n        [[\"GEOLOGICAL RESOURCES\", \"RESOURCE EXTRACTION\"]\n        [\"MOUNTAINOUS TERRAIN\", \"RESOURCE EXTRACTION\"]\n\n        [\"GEOLOGICAL RESOURCES\", \"TERRAIN ENRICHMENT\"]\n        [\"TERRACED FARMING\", \"TERRAIN ENRICHMENT\"]\n\n        [\"MOUNTAINOUS TERRAIN\", \"TERRACED AGRICULTURE\"]\n        [\"TERRACED FARMING\", \"TERRACED AGRICULTURE\"]\n         \n        [\"GEOLOGICAL RESOURCES\", \"MOUNTAINOUS TERRAIN\", \"TERRACED FARMING\", \"TERRAIN ENRICHMENT\", \"GEOLOGICAL RESOURCES\"]\n        [\"TERRACED FARMING\", \"MOUNTAINOUS TERRAIN\", \"GEOLOGICAL RESOURCES\", \"RESOURCE EXTRACTION\", \"TERRACED FARMING\"]]"
            },
            {
            "role": "user",
            "content": "This is great, keep this format and try another one:[\"TIDAL ENERGY\",\"WATER SUPPLY\",\"IRRIGATION\",\"RESERVOIR\",\"FLOODWATER\",\"BIOMASS\",\"WIND TURBINE\"]"
            },
            {
            "role": "assistant",
            "content": "Element Co-optimization:\n        \"1. Tidal Energy + Water Supply: Tidal energy can be harnessed to generate electricity, contributing to sustainable water supply systems.\n            Flow Outcome: \"Renewable Energy-Powered Water Supply\"\n\n        2.  Water Supply + Irrigation: Water supply systems can provide the necessary water for irrigation purposes in agricultural fields.\n            Flow Outcome: \"Secure Irrigation Water\"\n\n        3.  Water Supply + Reservoir: Water supply systems can store water in reservoirs, ensuring a steady and reliable water supply.\n            Flow Outcome: \"Water Reservoir Management\"\n\n        4.  Floodwater + Reservoir: Floodwater can be redirected to reservoirs, preventing floods and simultaneously ensuring a water supply.\n            Flow Outcome: \"Floodwater Management and Water Storage\"\n\n        5.  Biomass + Wind Turbine: Biomass can be converted into bioenergy while wind turbines generate electricity, together ensuring a diversified renewable energy sources.\n            Flow Outcome: \"Combined Biomass and Wind Energy Generation\"\n\n        The circular flows showcase the interplay between tidal energy, water supply, irrigation, reservoirs, floodwater, biomass, and wind turbines to create sustainable and interconnected systems of energy generation, water management, and agricultural practices.\n\nOrganized as:\n        [[\"TIDAL ENERGY\", \"RENEWABLE ENERGY-POWERED WATER SUPPLY\"],\n        [\"WATER SUPPLY\", \"RENEWABLE ENERGY-POWERED WATER SUPPLY\"],\n        \n        [\"WATER SUPPLY\", \"SECURE IRRIGATION WATER\"],\n        [\"IRRIGATION\", \"SECURE IRRIGATION WATER\"],\n        \n        [\"WATER SUPPLY\", \"WATER RESERVOIR MANAGEMENT\"],\n        [\"RESERVOIR\", \"WATER RESERVOIR MANAGEMENT\"],\n        \n        [\"FLOODWATER\", \"FLOODWATER MANAGEMENT AND WATER STORAGE\"],\n        [\"RESERVOIR\", \"FLOODWATER MANAGEMENT AND WATER STORAGE\"],\n        \n        [\"BIOMASS\", \"COMBINED BIOMASS AND WIND ENERGY GENERATION\"],\n        [\"WIND TURBINE\", \"COMBINED BIOMASS AND WIND ENERGY GENERATION\"],\n        \n        [\"TIDAL ENERGY\", \"WATER SUPPLY\", \"RENEWABLE ENERGY-POWERED WATER SUPPLY\"],\n        [\"WATER SUPPLY\", \"IRRIGATION\", \"SECURE IRRIGATION WATER\"],\n        [\"WATER SUPPLY\", \"RESERVOIR\", \"WATER RESERVOIR MANAGEMENT\"],\n        [\"FLOODWATER"
            },
            {
            "role": "user",
            "content": "Please do another one: "+insertstring
            },
        ],
        temperature=1,
        max_tokens=2500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        n=randomNumber,
    )
    return response['choices'][0]['message']['content']



def returninquire(element,max_tries=7):
    flowlist=[]
    toggle=False
    for i in range(max_tries):
        # generate a random int number between 2 and 10
        try:
            randomNumber = random.randint(1, 20)
            message=getinquire(element,randomNumber)
            print(f'message is {message}')
            flowlist=(convertflow(message))
            toggle=checknestedlist(flowlist)
        except:
            toggle=False
            print("reconvertflow")
            continue

        print(flowlist,toggle)
        if toggle==True:
            break
    return flowlist,message







def buildinquirematrix(flowlist):
    systemdict=returnsystem(flowlist,path="static/inquire/sample.json")
    colordict=color(systemdict,path="static/inquire/samplecolor.json")
    print(f'colordict is {colordict}')
    print("\n")
    matrixdict={}
    max_len=0
    for flow in flowlist:
        for ele in flow:
            try:
                [code,x,y]=[colordict[ele],flow.index(ele),flowlist.index(flow)]
            except:
                print(f'here is an error with {colordict[ele]}')
                [code,x,y]=["white",flow.index(ele),flowlist.index(flow)]
            if ele not in matrixdict.keys():
                matrixdict[ele]=[code,x,y]
            else: 
                if matrixdict[ele][1]>x:
                    matrixdict[ele][1]=x
                if matrixdict[ele][2]>y:
                    matrixdict[ele][2]=y
        if len(flow)>max_len:
            max_len=len(flow)
    matrixdict["TOTAL"]=["white",max_len,len(flowlist)]
    return matrixdict


def inspireflowtojson(element):
    inquireflow,message=returninquire(element,max_tries=5)
    matrix=buildinquirematrix(inquireflow)

    json_object = json.dumps(inquireflow, indent=4)  
    with open("static/inquire/flowtree.json", "w") as outfile:
        outfile.write(json_object)
    json_object2 = json.dumps(matrix, indent=4)  
    with open("static/inquire/matrix.json", "w") as outfile:
        outfile.write(json_object2)

    logtoJson(message,filepath="static/message/sherbotmessage.json")

    return inquireflow,matrix

def inquireclassify(element):
    systemdict=classify(flowlist=None,element=element)
    # colordict=color(systemdict,path="static/inquire/samplecolor_user.json")
    return systemdict



# def inquirejsontojson(filepath):
#     inquireload = json.load(open('static/inquire/inquire.json'))
#     elementforflow=inquireload['toinquireElement']
#     elementtoclassify=inquireload['toclassifyElement']

#     inquireflow=returninquire(elementforflow,max_tries=5)
#     matrix=buildinquirematrix(inquireflow)

#     json_object = json.dumps(inquireflow, indent=4)  
#     with open("static/inquire/flowtree.json", "w") as outfile:
#         outfile.write(json_object)
#     json_object2 = json.dumps(matrix, indent=4)  
#     with open("static/inquire/matrix.json", "w") as outfile:
#         outfile.write(json_object2)
#     return inquireflow,matrix
######################################################
######################################################
if __name__=="__main__":
    pass
    # test=["TIDAL ENERGY","WATER SUPPLY","IRRIGATION","RESERVOIR","FLOODWATER","BIOMASS","WIND TURBINE"]
    # # print(f'toclassify is {toclassify}')
    # print(f'inquiry is {test}')
    # result=inspireflowtojson(test)
    # print(f'result is {result}')

    # result2=inquireclassify(toclassify)
    # print(f'result2 is {result2}')
    # test= [['RESERVOIR', 'ENHANCED AGRICULTURAL PRODUCTIVITY'], 
    #        ['IRRIGATION', 'ENHANCED AGRICULTURAL PRODUCTIVITY'], 
    #        ['BIOMASS', 'ENHANCED AGRICULTURAL PRODUCTIVITY'], 
           
    #        ['WIND TURBINE', 'ENERGY-DRIVEN FLOODWATER MANAGEMENT'],
    #         ['FLOODWATER', 'ENERGY-DRIVEN FLOODWATER MANAGEMENT'], 

    #         ['WATER SUPPLY', 'BIOMASS FEEDSTOCK PRODUCTION'], 
    #         ['BIOMASS', 'BIOMASS FEEDSTOCK PRODUCTION'], 
            
    #         ['RESERVOIR', 'DROUGHT RESILIENCE'], 
    #         ['FLOODWATER', 'DROUGHT RESILIENCE'], 
    #         ['WATER SUPPLY', 'DROUGHT RESILIENCE'],
            
    #         ['BIOMASS', 'DIVERSIFIED RENEWABLE ENERGY'], 
    #         ['WIND TURBINE', 'DIVERSIFIED RENEWABLE ENERGY'], 
    #         ['IRRIGATION', 'OPTIMIZED AGRICULTURAL WATER USE'], 
    #         ['WATER SUPPLY', 'OPTIMIZED AGRICULTURAL WATER USE'], 
    #         ['RESERVOIR', 'OPTIMIZED AGRICULTURAL WATER USE'], 
    #         ['RESERVOIR', 'FLOODWATER', 'IRRIGATION', 'WATER SUPPLY', 'RESERVOIR'], 
    #         ['BIOMASS', 'WIND TURBINE', 'FLOODWATER', 'IRRIGATION', 'BIOMASS']]
    # matrix=buildinquirematrix(test)
    # print(f'matrix is {matrix}')