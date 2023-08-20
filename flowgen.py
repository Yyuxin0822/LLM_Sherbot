import os
import json
import re


def clean(input_string):
    "clean a string to make it start with letter and end with letter, and all the cases are upper"
    cleaned_string = re.sub(r'^[^a-zA-Z]+|[^a-zA-Z]+$', '', input_string)
    return cleaned_string.upper()


# flowD=[]
# def gen(input_string):
#     #input_string is like "a:b, b:c1;c2, c1;d:e"
#     #output a python dictionary and convert to an json object like like {a:b,b:c1;c2, c1;d:e}
#     dict={}
#     cleaned_list = clean(input_string).split(",")
#     for i in cleaned_list:
#         input = clean(i.split(":")[0].replace(";",","))
#         output = clean(i.split(":")[1].replace(";",","))
#         dict[input]=output
#     flowD.append(dict)

#     # Serializing json
#     json_object = json.dumps(dict, indent=4)
#     # Writing to sample.json
#     with open("static/flowexample.json", "a") as outfile:
#         outfile.write(json_object)

flowL=[]
def gen(input_string):
    #input_string is like "a,b, c1;c2, d"
    #input_string a python list and convert to a json array like like [a,b, c1;c2, d]
    unitflow=input_string.split(",")
    cleaned_unitflow = [clean(i) for i in unitflow]
    flowL.append(cleaned_unitflow)



# def gen(node,parent,child):
#     #node, parent, child are string like "a,b,c"
#     dict={}
#     dict["node"]=node
#     dict['child']=child.split(",")
#     dict['parent']=parent.split(",")
#     flowD[node]= dict
#     # Serializing json

def write_to_json(item):
    #item could be nested list or nested dictionary
    # Serializing json
    json_object = json.dumps(item, indent=None)
    # Writing to sample.json
    with open("static/flowexample.json", "w") as outfile:
        outfile.write(json_object)


 
if __name__=="__main__":
    #pass
    gen("brine,deep injection wells")
    gen("brine, reproduction process, BaSO4;NaCl")  
    gen("brine, Salt evaporation pond")    
    gen("waste water treatment,irrigation water,revegetation;regreening;adaptive greenhouses")
    gen("grey water;greywater; waste water, treatment wetland;irrigation water,revegetation;regreening;adaptive greenhouses")
    gen("grey water;greywater; waste water, wastewater treatment plant;WWT;treated water;recycled water;asset; buildings")
    gen("salt water, desalination plant")
    gen("salt water, inverse osmosis, sweet water;fresh water")
    gen("dessicant material, inverse osmosis, sweet water;fresh water")
    gen("deployable synthetic spider silk, inverse osmosis")   
    gen("moisture harvesting;dew collection, irrigation")
    gen("ocean waves, wave attenuater; energy generator, electricity")
    gen("chilorophyll, photosynthesis, oxygen")
    gen("chilorine; sodium hydroxide, electrolysis, electricity; grid")
    gen("desalination facility, brine; potable water")
    gen("hydrogen, battery storage")
    gen("wind turbine, electricity; grid; battery storage; battery")
    gen("regenerative agriculture, soil carbon")
    gen("regenerative agriculture, assets; buildings; food")
    gen("waste; organic waste, compost; fertilizer,vegetation")
    gen("organics,biodigestor; biogas; biofuel")
    gen("biodigester,methane;methane-based energy, hydrogen fuel cells")
    gen("algae; algae tide, biomass generator; algae tube wastewater treatment")
    gen("biofuel, battery")
    gen("electricity, grid;battery ")
    gen("hydro pump, electricity; grid")
    gen("mangrove; halophyte-based agriculture, leaves; leaf litter, food for shrimp; food for crab, sea farm to table")
    gen("organic marine debris, algae produce farm")
    gen("fresh water; fresh flow; wadis, lagoons; wetlands")
    gen("mangroves;vegetation; greening; regreening; forestation, bio-filtration; increase infiltration, vadose wells, increased ground water recharge ")
    gen("aquaculture;aquaculture fish house; sea farm, food; food for assets; food for buildings; food for people")

    write_to_json(flowL)




##############Nothing Useful Below########################################
##############Nothing Useful Below########################################
    #gen("brine:deep injection wells; salt evaporation pond")
    #gen("brine:reproduction process, reproduction process: BaSO4;NaCl")
    #gen("waste water treatment:irrigation water; revegetation; treated water, treated water:assets")
    #gen("grey water:b, b:c1;c2, c1;d:e")
    #gen("a:b, b:c1;c2, c1;d:e")
