
import os
import json
import re
import openai
import langchain
import random
from langchain.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from Sherbot_simpleflow import getelement, color, classify, convertsystem, returnsystem

os.environ["HUGGINGFACEHUB_API_TOKEN"] =  "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"
os.environ["OPENAI_API_KEY"] = "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"
openai.api_key = "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"
# "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"

######################################################
######################################################
#Helper Functions

# def clean(input_string):
#     "clean a string to make it start with letter and end with letter, and all the cases are upper"
#     cleaned_string = re.sub(r'^[^a-zA-Z]+|[^a-zA-Z]+$', '', input_string)
#     return cleaned_string.upper()

def clean(input_string):
    "clean a string to make it start with and end only with letter or parentheses, and all the cases are upper"
    cleaned_string = re.sub(r'^[^a-zA-Z(]+|[^a-zA-Z)]+$', '', input_string)
    return cleaned_string.upper()

def has_letters(string):
    return any(char.isalpha() for char in string)

def extract_brackets(text):
    pattern = r'\[(.*?)\]'  # Regular expression pattern to match strings between "[" and "]"
    matches = re.findall(pattern, text)  # Find all matches of the pattern in the text
    return matches

def extract_curly_brackets(text):
    pattern = r'\{(.*?)\}'  # Regular expression pattern to match strings between "{" and "}"
    matches = re.findall(pattern, text)  # Find all matches of the pattern in the text
    return matches

def extract_quotation(text):
    matches = re.findall('"(.*?)"', text)
    return matches


def checkjson(jsonfile):
    #open a json file from the path
    with open(jsonfile) as f:
        data = json.load(f)
        #check if the json file contains no letters
        return has_letters(str(data))

def checknestedlist(nestedlist):
    #input is a nested list, check if the input is not a nested list, return false  
    # check in each sublist, there's at least one element contains letters
    # if there's no element contains letters, return false
    # if there's at least one element contains letters, return true
    if len(nestedlist)==0:
        return False
    else:
        toggle=[]
        for sublist in nestedlist:
            for ele in sublist:
                toggle.append(has_letters(ele))
        return False not in toggle

def checktype(input):
    checktype= isinstance(input, list)
    return checktype

def checkcomplexflow(complexflow,simpleflow):
    if checktype(complexflow)==False:
        return False
    else:
        toggle=[]
        for flow in complexflow:
            # return if flow[0]==simpleflow[0] and flow[-1]==simpleflow[-1]
            toggle.append(flow[0]==simpleflow[0] and flow[-1]==simpleflow[-1])
        return False not in toggle
            

######################################################
######################################################
from langchain.cache import InMemoryCache
langchain.llm_cache = InMemoryCache()


#Generate output from input list
def getknowledge(simpleflow,randomNumber=4):
    insertstring=f'{simpleflow}'
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
        {"role": "system", "content": '''You are an encyclopedia. You are to provide knowledge for the generating the flow. 
        Flow is a list of two elements. The first element is the input and the second element is the output.
        Knowledge consists of four to five methods of generating the flow. Each method could be processes, resources, and technologies to transform input to output.
        Please don't make up the knowledge if you don't know it. 

        Only output an array of json arrays. Don't output if the knowledge is not an array of json arrays.

        Here are examples:
        Flow: ["BRINE","BASO4;NACL"]
        Knowledge: [["Brine can transform to Baso4 and NaCl through reproduction process."],["Brine can transform to BaSo4 and NaCl through salt evaporation pond."], ["Brine can transform to Baso4 and NaCl through inverse osmosis."]] 
        ##

        Flow: ["WASTEWATER","AGRICULTURE"]
        Knowledge:[["Wastewater is processed in Wastewater Treatment Plant to output treated water. Treated water can be used for agriculture."],["Wastewater can cut the need for fertilisers, and improve soi quality, and be useful to agriculture."]]
        ##

        Flow: ["AQUACULTURE","FOOD"]
        Knowledge: [["Aquaculture include oyster farming, and the output is food."],["Aquaculture include shrimp farming and fish house, and the output is food."]]
        '''},
        {"role": "user", "content": insertstring},
        ],
        temperature=1,
        n=randomNumber,
    )
    return response['choices'][0]['message']['content']




def getchain(simpleflow,knowledge=None,randomNumber=4):
    if knowledge==None:
        knowledge=getknowledge(simpleflow)
    insertstring=f' To transform {simpleflow[0]} to {simpleflow[1]}, we know: {knowledge}'
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
        {"role": "user", "content": '''You are to convert knowledge about flow into chain of processes.
            The chain is an array of json sub arrays. Each sub array has three to six sequenced elements interpreting knowledge.
            Don't output if the chain is not an array of json sub arrays.
         
        '''},
        {"role": "system", "content": '''Please let me know your knowledge and I will generate the chain for you.'''},
        {"role": "user", "content": '''To transform "BRINE" to "BASO4;NACL", we know: [["Brine can transform to Baso4 and Nacl through reproduction process."],["Brine can transform to Baso4 and Nacl through salt evaporation pond."], ["Brine can transform to Baso4 and Nacl through inverse osmosis."]]'''},
        {"role": "system", "content": '''[["BRINE", "REPRODUCTION PROCESS", "BASO4;NACL"],["BRINE", "SALT EVAPORATION POND", "BASO4;NACL"],["BRINE", "INVERSE OSMOSIS", "BASO4;NACL"]] '''},
        {"role": "user", "content": ''' ["WASTEWATER","AGRICULTURE"]'''},
        {"role": "system", "content": '''To transform "WASTEWATER" to "AGRICULTURE", we know: [["Wastewater is processed in Wastewater Treatment Plant to output treated water. Treated water can be used for agriculture."],["Wastewater can cut the need for fertilisers, and improve soi quality, and be useful to agriculture."]]'''},
        {"role": "user", "content": '''[["WASTEWATER", "WASTEWATER TREATMENT PLANT", "TREATED WATER", "AGRICULTURE"],["WASTEWATER", "FERTILISER","SOIL QUALITY","AGRICULTURE"]]'''},
        {"role": "system", "content": ''' [["Aquaculture include oyster farming, and the output is food."],["Aquaculture include shrimp farming and fish house, and the output is food."]]'''},     
        {"role": "user", "content": insertstring},
        ],
        temperature=0.5,
        n=randomNumber,
    )
    return response['choices'][0]['message']['content']


def convertflow(flow_string):
    # Get the first index of "["
    first_index = flow_string.index("[")
    # Get the last index of "]"
    last_index = flow_string.rindex("]")
    # Get the string between first and last index
    new_string = flow_string[first_index+1:last_index]


    flowlist=[]
    tempflow=extract_brackets(new_string)
    for temp in tempflow:
        templist=extract_quotation(temp)
        cleanlist=[clean(ele) for ele in templist]
        print(cleanlist)
        flowlist.append(cleanlist)

    return flowlist

def returncomplexflow(simpleflow,max_tries=7):
    flowlist=[]
    toggle=False
    for i in range(max_tries):
        # generate a random int number between 2 and 10
        try:
            randomNumber = random.randint(1, 20)
            knowledge=getknowledge(simpleflow,randomNumber)
            print(knowledge)
            randomNumber = random.randint(4, 10)
            flow_string=getchain(simpleflow,knowledge,randomNumber)
            flowlist=(convertflow(flow_string))
            toggle=checkcomplexflow(flowlist,simpleflow)
            print(flowlist,toggle)
        except:
            print("error at return flow")
            toggle=False
        if toggle==True:
            break
    return flowlist, knowledge



def buildmatrix(flowlist,get_rid_of_ends=True):
    #flowlist is a nested list of flow, get the unique element in each sublist, and get the xpoistion, yposition of each element
    #xposition is index of sublist that contains the element, ypostion is the index of the element in the sublist
    #build a dictionary, the key is the element, the value is [xposition, yposition]
    if get_rid_of_ends:
        complexflow=[flow[1:-1] for flow in flowlist]


    systemdict=returnsystem(complexflow,path="static/complex/sample.json")
    colordict=color(systemdict,path="static/complex/samplecolor.json")
    print(f'colordict is {colordict}')
    print("\n")
    matrixdict={}
    max_len=0
    for flow in complexflow:
        for ele in flow:
            try:
                [code,x,y]=[colordict[ele],flow.index(ele),complexflow.index(flow)]
            except:
                print(f'here is an error with {colordict[ele]}')
                [code,x,y]=["white",flow.index(ele),complexflow.index(flow)]
            if ele not in matrixdict.keys():
                matrixdict[ele]=[code,x,y]
            else: 
                if matrixdict[ele][1]<x:
                    matrixdict[ele][1]=x
                if matrixdict[ele][2]<y:
                    matrixdict[ele][2]=y
        if len(flow)>max_len:
            max_len=len(flow)
    matrixdict["TOTAL"]=["white",max_len,len(complexflow)]
    return matrixdict
 




def complexflowtojson(simpleflow,refopt="input"):
    reorderedflow=[]
    filepath=f"static/simple/sorted_{refopt}.json"
    # load static/simple/input.json as python list
    with open(filepath) as f:
        input = json.load(f)
        for i in range(len(input)):
            for flow in simpleflow:
                if input[i]==flow[0]:
                    reorderedflow.append(flow)
    print(f'simpleflow is {simpleflow}')
    simpleflow=reorderedflow
    print(f'reorderedflow is {reorderedflow}')

    messagefilepath="static/message/sherbotmessage.json"

    matrix=[]
    complexflow=[]
    for flow in simpleflow:
        complextemp,know_string=returncomplexflow(flow)
        if complextemp:
            matrixtemp=buildmatrix(complextemp)
            matrix.append(matrixtemp)

            log1=f'To transform "{flow[0]}" to "{flow[1]}:",\n'
            logtoJson(log1,messagefilepath)

            for temp in complextemp:
                complexflow.append(temp)

            log2=f'{know_string}, \n'
            log3=f'Organized as: {complextemp}.\n'
            log4=f'\n'

            logtoJson(log1+log2+log3+log4,messagefilepath)

    json_object = json.dumps(complexflow, indent=4)  
    with open("static/complex/flowtree.json", "w") as outfile:
        outfile.write(json_object)
    json_object2 = json.dumps(matrix, indent=4)  
    with open("static/complex/matrix.json", "w") as outfile:
        outfile.write(json_object2)


    # write new flow file to simpleflow
    # with open('static/simple/simplematrix.json', 'r') as f:
    #     logjson=json.load(f)
    #     loglist=list(logjson)
    #     return 
        # f.write("[]")
    # with open('static/simple/simpleflow.json', 'r') as f:
    #     f.write("[]")
    # with open('static/simple/sample.json', 'r') as f:
    #     f.write("[]")
    # with open('static/simple/samplecolor.json', 'r') as f:
    #     f.write("[]")
        
    return complexflow,matrix

def addtosimple(inquireflow):

    # write simpleflow 
    simpleflowpath="static/simple/simpleflow.json"
    toaddflow=[]
    with open(simpleflowpath, 'r') as f:
        logjson_sf=json.load(f)
        loglist_sf=list(logjson_sf)
        for flow in inquireflow:
            if flow not in loglist_sf:
                toaddflow.append(flow)
                loglist_sf.append(flow)
    json_object = json.dumps(loglist_sf, indent=4)  
    with open(simpleflowpath, "w") as outfile:
        outfile.write(json_object)
    
    #update simplematrix
    simplematrixpath="static/simple/simplematrix.json"
    with open(simplematrixpath, 'r') as f:
        logjson_sm=json.load(f)
        loglist_sm=dict(logjson_sm)
        # for flow in toaddflow:

    return loglist_sf,loglist_sm

# load a json file from the path
def logtoJson(message,filepath):
    with open(filepath, 'r') as f:
        logjson = json.load(f)
        loglist=list(logjson)
        if loglist:
            log_string=loglist[0]+message
            newlog=[log_string]
        else:
            newlog=[message]
    json_object = json.dumps(newlog, indent=4)  
    with open(filepath, "w") as outfile:
        outfile.write(json_object)
    return newlog
# ######################################################
# ######################################################
# #Task 2.x generate flow matrix

# def getxindex(flowlist, systemdict):
#     #xindex is a dictionary that contains the index of the flowlist, the key is the element, the value is the index
#     xindex={}
#     for key in systemdict.keys():
#         #loop through flowlist, if the key is in the sublist or part of the string in the sublist, add the index of the sublist to the xindex
#         for sublist in flowlist:
#             for ele in sublist:
#                 if key==ele or key in ele:
#                     #xindex[key]= the index of ele in sublist
#                     xindex[key]=sublist.index(ele)
#     return xindex   

# def getyindex(systemdict):
#     systemcount={}
#     subcount={}
#     #get all unique values in systemdict
#     uniquelist=[]
#     for key in systemdict.keys():
#         if systemdict[key] not in uniquelist:
#             uniquelist.append(systemdict[key])
#     #get the count of each unique value in systemdict
#     for i in uniquelist:
#         systemcount[i]=0

#     for key in systemdict.keys():
#         for i in uniquelist:
#             if systemdict[key]==i:
#                 subcount[key]=systemcount[i]
#                 systemcount[i]+=1

#     #loop through systemdict,  if the key is "HYDRO", keep the value; if the key is "ENERGY", add the value with the length of "HYDRO"; if the key is "ECOSYSTEM", add the value with the length of "HYDRO" and "ENERGY"
#     yindex={}
#     for key in systemdict.keys():
#         if systemdict[key]=="HYDRO":
#             yindex[key]=subcount[key]
#         elif systemdict[key]=="ENERGY":
#             yindex[key]=subcount[key]+systemcount["HYDRO"]
#         elif systemdict[key]=="ECOSYSTEM":
#             yindex[key]=subcount[key]+systemcount["ENERGY"]+systemcount["HYDRO"]
#     return yindex
    
# def matrix(flowlist,systemdict):
#     #get xindex and yindex
#     xindex=getxindex(flowlist, systemdict)
#     yindex=getyindex(systemdict)
#     #xindex is a dictionary, the key is the element, the value is the xindex of the element
#     #yindex is a dictionary, the key is the element, the value is the yindex of the element
#     matrix={}
#     for key in systemdict.keys():
#         if key in xindex.keys() and key in yindex.keys():
#             matrix[key]=[xindex[key],yindex[key]]
#     return matrix

# def getmatrixXY(matrixdict):
#     #matrixdict is a dictionary, the key is the element, the value is [xposition, yposition]
#     #get the max xcount and ycount
#     xposition=[]
#     yposition=[]
#     for key in matrixdict.keys():
#         xposition.append(matrixdict[key][0])
#         yposition.append(matrixdict[key][1])
#     max_xposition=max(xposition) 
#     max_yposition=max(yposition) 
#     return [max_xposition+1, max_yposition+1]

# def trans_topaligned(matrixdict):
#     #matrixdict is a dictionary, the key is the element, the value is [xposition, yposition]
    
#     dictcount=len(matrixdict)
#     max_xcount=getmatrixXY(matrixdict)[0]

#     transmatrix_topaligned={}
#     #loop through all keys in matrixidct, according to the sequence of xposition, and then the sequence of yposition
#     for i in range(max_xcount):
#         ysubcount=0
#         for j in range(dictcount):
#             for key in matrixdict.keys():
#                 if matrixdict[key][0]==i and matrixdict[key][1]==j:
#                     transmatrix_topaligned[key]=[i,ysubcount]
#                     ysubcount+=1
    
    
#     #loop through transmatrix_topaligned, transform the value of xposition to 2*xposition+1
#     # for key in transmatrix_topaligned.keys():
#     #     transmatrix_topaligned[key][0]=2*transmatrix_topaligned[key][0]      
#         # transmatrix_topaligned[key][1]=2*transmatrix_topaligned[key][1]     

#     transmatrix_topaligned["TOTAL"]=getmatrixXY(transmatrix_topaligned)
    
#     json_object = json.dumps(transmatrix_topaligned, indent=4)
#     with open("static/v2/matrix.json", "w") as outfile:
#         outfile.write(json_object)

#     return transmatrix_topaligned

# def trans_inline(flowlist):
#     matrixdict={}
#     for sublist in flowlist:
#         for ele in sublist:
#             [x,y]=[sublist.index(ele),flowlist.index(sublist)]
#             if ele not in matrixdict.keys():
#                 matrixdict[ele]=[x,y]
#             else: 
#                 #compare x,y, get the larger x,y
#                 if matrixdict[ele][0]<x:
#                     matrixdict[ele][0]=x
#                 if matrixdict[ele][1]<y:
#                     matrixdict[ele][1]=y

#     #loop through matrixdict, transform the value of xposition to 2*xposition
#     for key in matrixdict.keys():
#         matrixdict[key][0]=2*matrixdict[key][0]
    
    
#     matrixdict["TOTAL"]=getmatrixXY(matrixdict)    
#     json_object = json.dumps(matrixdict, indent=4)
#     with open("static/v2/matrix.json", "w") as outfile:
#         outfile.write(json_object)

#     return matrixdict

######################################################
######################################################
if __name__=="__main__":
    # pass
    simplelist=addtosimple([])
    print(simplelist)



    # env="This scene depicts an agricultural village in the mountains. There are a couple flood valleys with turbulent water. To empower this village, there are some windfarms nearby. Cheetahs in the mountains need to be preserved. Food and potable water can be very valuable here."
    # # env="This scene depicts a coastal environment."
    # input=(returninput(env))
    # print(input)
    # print("\n")
    # output=(returnsimpleflow(input))
    # print(output)
    # print("\n")
    # system=(returnsystem(output))
    # print(system)
    # print("\n")
    # colordict=(color(system))
    # print(colordict)
    # print("\n")
    # matrixdict=(simplematrix(output))
    # print(matrixdict)

    # test_simpleflow=[ ["MOUNTAINOUS TERRAIN","TOURISM OPPORTUNITIES"],["WIND ENERGY","CLIMATE CONTROL"],["AGRICULTURE","BIOMASS"],["SOIL FERTILITY","CARBON SEQUESTRATION"],["LIVESTOCK","DAIRY PRODUCTS"],["FOOD CROPS","BIOFUEL"]]
    # test_simpleflow2=[ ["MOUNTAINOUS TERRAIN","TOURISM OPPORTUNITIES"],["WIND ENERGY","CLIMATE CONTROL"],
    # ["AGRICULTURE","BIOMASS"],["SOIL FERTILITY","CARBON SEQUESTRATION"],
    # ["LIVESTOCK","DAIRY PRODUCTS"],["FOOD CROPS","BIOFUEL"],["STONE/MINERAL DEPOSITS", "MINERALS"],
    # ["WOOD","FUEL"],["WILDLIFE HABITAT","ECOTOURISM OPPORTUNITIES"],
    # [ "WIND TURBINES","INDUSTRIAL POWER SUPPLY"],["FLOODWATER","IRRIGATION"],["HYDROPOWER","WATER SUPPLY"]]
    # test_simpleflow3=[ ["MOUNTAINOUS TERRAIN","TOURISM OPPORTUNITIES"],["WIND ENERGY","CLIMATE CONTROL"],["AGRICULTURE","BIOMASS"],["SOIL FERTILITY","CARBON SEQUESTRATION"],
    # ["LIVESTOCK","DAIRY PRODUCTS"],["FOOD CROPS","BIOFUEL"],["STONE/MINERAL DEPOSITS","MINERALS"],["WOOD","FUEL"],
    # ["WILDLIFE HABITAT","ECOTOURISM OPPORTUNITIES"],["WIND TURBINES","INDUSTRIAL POWER SUPPLY"],["FLOODWATER","IRRIGATION"],
    # ["HYDROPOWER","WATER SUPPLY"],["WILD GAME","LEATHER GOODS"],["GRASSES FOR GRAZING","SOIL PRESERVATION"],
    # ["FRESH AIR","CARBON SINKS"],["SUNLIGHT","NATURAL LIGHTING"],["SEDIMENT DEPOSITS","BUILDING MATERIAL"],["GEOLOGICAL RESOURCES","CONSTRUCTION MATERIALS"],
    # ["NATIVE PLANTS","MEDICINE"],["WILD EDIBLES AND MEDICINAL HERBS","HEALTHCARE PRODUCTS"],["TOPSOIL","LAND REHABILITATION"],
    # ["MICROORGANISMS","SOIL FERTILITY"],["LOCAL HUMAN RESOURCES","KNOWLEDGE"],["CLAY DEPOSITS","POTTERY"],
    # ["CARBON DIOXIDE (FROM PLANTS)","AIR PURIFICATION"],["OXYGEN (FROM PLANTS)","AVOIDS GREENHOUSE GASES"],
    # ["CULTURAL HERITAGE","TOURISM"],["ECOTOURISM POTENTIAL","CONSERVATION EFFORTS"],
    # ["LOCAL INDIGENOUS KNOWLEDGE","CULTURAL PRESERVATION"]]
    # test_simpleflow4=[['LOCAL HUMAN RESOURCES', 'KNOWLEDGE']]

    # test_simpleflow5=[
    #     [
    #         "GEOLOGIC SUBSTRATE",
    #         "ORES"
    #     ],
    #     [
    #         "TOPSOIL",
    #         "NUTRIENT-RICH SOIL"
    #     ],
    #     [
    #         "MINERAL RESOURCES",
    #         "INDUSTRIAL MINERALS"
    #     ],
    #     [
    #         "CROPS",
    #         "BIOFUEL"
    #     ],]




    # complexflow=complexflowtojson(test_simpleflow5,refopt="input")
    # print(complexflow)
    # print("\n")



# 
    # for flow in test_simpleflow:
    #     print('Input: ' + flow[0]+', Output: '+flow[1])
    #     result=convertflow(getchain(flow))
    #     print(result)
    #     complexflow=returncomplexflow(flow)
    #     print(complexflow)
    #     print("\n")

        # print("\n")
        # testmatrix=buildmatrix(result)
        # print(testmatrix)
        # print("\n")
        # totalmatrix=matrixtojson(result)
        # print(totalmatrix)
        # print("\n")



    # # # #test_simpleflow=[["OCEAN CURRENT","WAVE ENERGY"],["WAVE ENERGY","WAVE ENERGY PLANT"],["WAVE ENERGY","GRID"],["FUEL","GRID"]]
    # # # #test_simpleflow=[["OCEAN CURRENT","WAVE ENERGY"],["WAVE ENERGY","WAVE ENERGY PLANT"]]
    # flow_tree=flowtree(simpleflowlist)
    # print(flow_tree)
    # systemdict=returnsystem(flow_tree)
    # print(systemdict)
    # print("/n")
    # matrixdict=trans_inline(flow_tree)
    # print(matrixdict)

    # test=f'[['OCEAN CURRENT', 'WAVE ENERGY', 'WAVE ENERGY PLANT'], ['WAVE ENERGY', 'GRID'], ['FIRE', 'FUEL', 'GRID'], ['SEA LIFE', 'FISHERIES']]'
    # #test=f'[["MOUNTAIN ROCKS", "WEATHERING PROCESS;WIND ENERGY", "SOIL;MINERALS"], ["RIVER WATER; LOCAL WEATHER DATA; PRECIPITATION; ATMOSPHERIC MOISTURE; DEW WATER; FLOOD WATER", "WATER TREATMENT FACILITY", "WATER EXTRACTION; WATER CONSERVATION"], ["WIND ENERGY", "WIND TURBINES; WINDFARM INFRASTRUCTURE", "ELECTRICITY GENERATION; RENEWABLE ENERGY"], ["AGRO WASTE; ANIMAL MANURE; VILLAGE WASTE; HUMAN WASTE", "BIOGAS DIGESTER; COMPOSTING", "BIOMASS ENERGY; COMPOST"], ["MOUNTAIN HERBS; MOUNTAIN FLORA; LOCAL FLORA AND FAUNA SPECIES", "SUSTAINABLE HARVESTING; REGENERATIVE AGRICULTURE", "HERBAL PRODUCTS; FOOD PRODUCTION; PHARMACEUTICALS"], ["EROSION SOIL; MOUNTAIN SEDIMENTS; FLOOD PLAIN SILT", "FLOOD PLAIN FERTILIZATION", "SOIL ENHANCEMENT; CROP CULTIVATION"], ["FLOOD PLAIN WILDLIFE; BIRD SPECIES; INSECT SPECIES; LOCAL LIVESTOCK; MOUNTAIN FAUNA", "ECOLOGICAL BALANCE; INDIGENOUS KNOWLEDGE", "BIO-DIVERSITY; ECOSYSTEM SERVICES"], ["MOUNTAIN MINERALS", "SUSTAINABLE MINING", "BUILDING MATERIALS; NUTRIENTS"], ["LOCAL CROP SEEDS", "PLANTING; REGENERATIVE AGRICULTURE", "SUSTAINABLE FOOD PRODUCTION"], ["SOLAR ENERGY", "SOLAR PANELS", "ELECTRICITY GENERATION; RENEWABLE ENERGY"], ["LOCAL WOOD RESOURCES", "SUSTAINABLE FORESTRY", "BUILDING MATERIALS;FUEL;ECOSYSTEM SERVICES"], ["REGIONAL AIR QUALITY; LOCAL WEATHER DATA", "ENVIRONMENTAL MONITORING", "POLICY MAKING;ENVIRONMENTAL MANAGEMENT"], ["AQUIFER WATER", "WATER EXTRACTION", "POTABLE WATER;IRRIGATION","VEGETATION","ENHANCED INFILTRATION","VADOSE WELLS","AQUIFER"], ["BUILDING;ASSETS","VILLAGE WASTEWATER; CHEETAH GENETIC MATERIAL", "WASTE WATER TREATMENT;GENETIC CONSERVATION", "TREATED WATER;BIOLOGICAL CONSERVATION"]]'
    # #trans_matrix={}
    # print(f'transform matrix is :{trans_matrix}')


    # print(simpleflow(result))
    # print(convertelement(classify(result)))


    # test=f'[["MOUNTAIN ROCKS", "WEATHERING PROCESS;WIND ENERGY", "SOIL"], ["RIVER WATER; LOCAL WEATHER DATA","WWT"]]'
    # #test=f'[["MOUNTAIN ROCKS", "WEATHERING PROCESS;WIND ENERGY", "SOIL;MINERALS"], ["RIVER WATER; LOCAL WEATHER DATA; PRECIPITATION; ATMOSPHERIC MOISTURE; DEW WATER; FLOOD WATER", "WATER TREATMENT FACILITY", "WATER EXTRACTION; WATER CONSERVATION"], ["WIND ENERGY", "WIND TURBINES; WINDFARM INFRASTRUCTURE", "ELECTRICITY GENERATION; RENEWABLE ENERGY"], ["AGRO WASTE; ANIMAL MANURE; VILLAGE WASTE; HUMAN WASTE", "BIOGAS DIGESTER; COMPOSTING", "BIOMASS ENERGY; COMPOST"], ["MOUNTAIN HERBS; MOUNTAIN FLORA; LOCAL FLORA AND FAUNA SPECIES", "SUSTAINABLE HARVESTING; REGENERATIVE AGRICULTURE", "HERBAL PRODUCTS; FOOD PRODUCTION; PHARMACEUTICALS"], ["EROSION SOIL; MOUNTAIN SEDIMENTS; FLOOD PLAIN SILT", "FLOOD PLAIN FERTILIZATION", "SOIL ENHANCEMENT; CROP CULTIVATION"], ["FLOOD PLAIN WILDLIFE; BIRD SPECIES; INSECT SPECIES; LOCAL LIVESTOCK; MOUNTAIN FAUNA", "ECOLOGICAL BALANCE; INDIGENOUS KNOWLEDGE", "BIO-DIVERSITY; ECOSYSTEM SERVICES"], ["MOUNTAIN MINERALS", "SUSTAINABLE MINING", "BUILDING MATERIALS; NUTRIENTS"], ["LOCAL CROP SEEDS", "PLANTING; REGENERATIVE AGRICULTURE", "SUSTAINABLE FOOD PRODUCTION"], ["SOLAR ENERGY", "SOLAR PANELS", "ELECTRICITY GENERATION; RENEWABLE ENERGY"], ["LOCAL WOOD RESOURCES", "SUSTAINABLE FORESTRY", "BUILDING MATERIALS;FUEL;ECOSYSTEM SERVICES"], ["REGIONAL AIR QUALITY; LOCAL WEATHER DATA", "ENVIRONMENTAL MONITORING", "POLICY MAKING;ENVIRONMENTAL MANAGEMENT"], ["AQUIFER WATER", "WATER EXTRACTION", "POTABLE WATER;IRRIGATION","VEGETATION","ENHANCED INFILTRATION","VADOSE WELLS","AQUIFER"], ["BUILDING;ASSETS","VILLAGE WASTEWATER; CHEETAH GENETIC MATERIAL", "WASTE WATER TREATMENT;GENETIC CONSERVATION", "TREATED WATER;BIOLOGICAL CONSERVATION"]]'
    # result=convertflow(test)
    # systemdict=convertelement(classify(result))
    # # print(systemdict)
    # # print(f'Total element number: {len(systemdict)}')
    # matrixdict=matrix(result,systemdict)
    # # print(f'matrix is :{matrixdict}')
    # trans_matrix=trans_topaligned(matrixdict)
    # print(f'transform matrix is :{trans_matrix}')

    # test2=f'[["MOUNTAIN ROCKS","ecosystem","#39b54a"],["FARM CROPS","ecosystem","#39b54a"],["SOIL NUTRIENTS","ecosystem","#39b54a"]]'
    # print(convertelement(test2))

    # print("\n")
    # print(getelement(result))
    #print("\n")
    #print(result.keys())
    #print("\n")
    #print(result.values())
    #print(color(categorize(result)))





#####################NOTHING USEFUL AFTER THIS################################
######################################################



# def getmatrix(flowlist):
#     #this is the flow before simplification
#     #flowlist is a nested list of flow, transform every sublist to have the same length as the longest sublist
#     #get the max length of the sublist
#     max_len=0
#     for sublist in flowlist:
#         if len(sublist)>max_len:
#             max_len=len(sublist)
#     #transform every sublist to have the same length as the longest sublist
#     for sublist in flowlist:
#         if len(sublist)<max_len:
#             for i in range(max_len-len(sublist)):
#                 sublist.append(0)
#     #transform the flowlist to a matrix
#     flowmatrix=[]
#     for sublist in flowlist:
#         flowmatrix.append(sublist)
#     return flowmatrix

# def flipmatrix(flowlist):
#     #flip matrix of the flow list, the flowlist was a nested list like [[a,b,c][d,e,f]], after flip it becomes [[a,d][b,e][c,f]]
#     #get the max length of the sublist
#     max_len=0
#     for sublist in flowlist:
#         if len(sublist)>max_len:
#             max_len=len(sublist)
#     #transform every sublist to have the same length as the longest sublist
#     for sublist in flowlist:
#         if len(sublist)<max_len:
#             for i in range(max_len-len(sublist)):
#                 sublist.append(0)
#     #flip the matrix
#     flipmatrix=[]
#     for i in range(max_len):
#         temp=[]
#         for sublist in flowlist:
#             temp.append(sublist[i])
#         flipmatrix.append(temp)
#     return flipmatrix





# flow_llm = ChatOpenAI(model="gpt-4",temperature=1.0)

# def getknowledge(simpleflow,randomNumber=4):
#     flow_template = """You are an encyclopedia. You are to provide knowledge for the generating the flow. 
#         Flow is a list of two elements. The first element is the input and the second element is the output.
#         Knowledge consists of {randomNumber} methods of generating the flow. Each method includes processes, resources, and technologies to transform input to output.
#         Please don't make up the knowledge if you don't know it. 
#         Only output an array of json arrays. Don't output if the knowledge is not an array of json arrays.

#         Flow: ["BRINE","BASO4;NACL"]
#         Knowledge: [["Brine can transform to Baso4 and Nacl through reproduction process."],["Brine can transform to Baso4 and Nacl through salt evaporation pond."], ["Brine can transform to Baso4 and Nacl through inverse osmosis."]] 

#         Flow: ["WASTEWATER","AGRICULTURE"]
#         Knowledge:[["Wastewater is processed in Wastewater Treatment Plant to output treated water. Treated water can be used for agriculture."],["Wastewater can cut the need for fertilisers, and improve soi quality, and be useful to agriculture."]]

#         Flow: ["AQUACULTURE","FOOD"]
#         Knowledge: [["Aquaculture include oyster farming, and the output is food."],["Aquaculture include shrimp farming and fish house, and the output is food."]]

#         Flow: {simpleflow}
#         knowledge:
#     """

#     flow_prompt_template = PromptTemplate(
#         input_variables=["simpleflow","randomNumber"],
#         template=flow_template,
#     )

#     flow_chain = LLMChain(
#         llm=flow_llm, prompt=flow_prompt_template, verbose=False,memory=None
#     )  
#     flow_string= flow_chain.run({"simpleflow": simpleflow,"randomNumber": randomNumber})

#     return flow_string



# def getchain(simpleflow,knowledge=None,randomNumber=4):
#     insertstring=f'{simpleflow}'
#     response = openai.ChatCompletion.create(
#         model="gpt-4",
#         messages=[
#         {"role": "user", "content": '''You are to convert knowledge about flow into chain of processes.
#             The chain is an array of json sub arrays. Each sub array has three to ten sequenced elements interpreting knowledge.
#             Don't output if the chain is not an array of json sub arrays.'''},
#         {"role": "system", "content": '''Please let me know your knowledge and I will generate the flow for you.'''},
#         {"role": "user", "content": '''To transform "BRINE" to "BASO4;NACL", 
#          we know: [["Brine can transform to Baso4 and Nacl through reproduction process."],["Brine can transform to Baso4 and Nacl through salt evaporation pond."], ["Brine can transform to Baso4 and Nacl through inverse osmosis."]]'''},
#         {"role": "system", "content": '''[["BRINE", "REPRODUCTION PROCESS", "BASO4;NACL"],["BRINE", "SALT EVAPORATION POND", "BASO4;NACL"],["BRINE", "INVERSE OSMOSIS", "BASO4;NACL"]]'''},
#         {"role": "user", "content": ''' ["WASTEWATER","AGRICULTURE"]'''},
#         {"role": "system", "content": '''[["Wastewater is processed in Wastewater Treatment Plant to output treated water. Treated water can be used for agriculture."],["Wastewater can cut the need for fertilisers, and improve soi quality, and be useful to agriculture."]]'''},
#         {"role": "user", "content": '''["AQUACULTURE","FOOD"]'''},
#         {"role": "system", "content": ''' [["Aquaculture include oyster farming, and the output is food."],["Aquaculture include shrimp farming and fish house, and the output is food."]]'''},     
#         {"role": "user", "content": insertstring},
#         ],
#         temperature=0.5,
#         n=randomNumber,
#     )
#     return response['choices'][0]['message']['content']


# chain_llm = ChatOpenAI(model="gpt-4",temperature=0.5)
# def getchain(simpleflow,knowledge=None,randomNumber=4):
#     if knowledge==None:
#         knowledge=getknowledge(simpleflow)
#     chain_template = """You are to convert knowledge about flow into chain of processes.
#         The chain is an array of json sub arrays. Each sub array has three to {randomNumber} sequenced elements interpreting knowledge.
#         Don't output if the chain is not an array of json sub arrays.
        
#         knowledge: To transform "BRINE" to "BASO4;NACL", we know: [["Brine can transform to Baso4 and Nacl through reproduction process."],["Brine can transform to Baso4 and Nacl through salt evaporation pond."], ["Brine can transform to Baso4 and Nacl through inverse osmosis."]]
#         Chain:[["BRINE", "REPRODUCTION PROCESS", "BASO4;NACL"],["BRINE", "SALT EVAPORATION POND", "BASO4;NACL"],["BRINE", "INVERSE OSMOSIS", "BASO4;NACL"]]
#         ##
#         knowledge: To transform "WASTEWATER" to "AGRICULTURE", we know: [["Wastewater is processed in Wastewater Treatment Plant to output treated water. Treated water can be used for agriculture."],["Wastewater can cut the need for fertilisers, and improve soi quality, and be useful to agriculture."]]
#         Chain:[["WASTEWATER", "WASTEWATER TREATMENT PLANT", "TREATED WATER", "AGRICULTURE"],["WASTEWATER", "FERTILISER","SOIL QUALITY","AGRICULTURE"]]
#         ##
#         Flow: To transform "AQUACULTURE" to "FOOD", we know:[["Aquaculture include oyster farming, and the output is food."],["Aquaculture include shrimp farming and fish house, and the output is food."]]
#         Chain:[["AQUACULTURE","OYSETER FARMING","FOOD"],["AQUACULTURE","SHRIMP FARMING; FISH HOUSE","FOOD"]]
#         ##
#         knowledge: To transform {input} to {output}, we know: {knowledge}
#         Chain:
#     """

#     chain_prompt_template = PromptTemplate(
#         input_variables=["randomNumber","input","output","knowledge"],
#         template=chain_template,
#     )

#     flowjson_chain = LLMChain(
#         llm=chain_llm, prompt=chain_prompt_template, verbose=False,memory=None
#     )  

#     flow_string= flowjson_chain.run({"randomNumber":randomNumber,"input": simpleflow[0],"output": simpleflow[1],"knowledge": knowledge})

#     return flow_string
