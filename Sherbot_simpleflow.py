import os
import json
import re
import random
import urllib
import openai
import langchain
from langchain.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

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
    # "clean a string to make it start with and end only with letter,numbers, or parentheses, and all the cases are upper"
    cleaned_string = re.sub(r'^[^a-zA-Z0-9()]+|[^a-zA-Z0-9()]+$', '', input_string)
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
    matches = re.findall(r'\'(.*?)\'', text)
    if len(matches)==0:
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
    #check if input is list, return a boolean
    checktype= isinstance(input, list)
    return checktype

######################################################
######################################################
#Task 1 - Generate Environment Image
def getcanvas(envir_description):
    response = openai.Image.create(
        prompt=f"{envir_description}",
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']
    urllib.request.urlretrieve(image_url, "static/envir.png")
    return image_url



######################################################
######################################################
#Task 2.1 - Minimum Version of Flow Generation
#Generate input from environment description
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.cache import InMemoryCache
langchain.llm_cache = InMemoryCache()

### Get input from environment description
input_llm = ChatOpenAI(model="gpt-4",temperature=1)

def getinput(envir_description):
    input_template = """
    You are a environmental engineering specialist, you will extract and imagine potential resources in the environment description as keywords. The resources in the environment include potential organisms, chemicals, materials; and they come from various systems, such as hydro, energy, and ecosystem. Please try to imagine as many as possonible, and provide me around 40 in total.

    Environment description: "This scene depicts an agricultural village in the mountains. There are a couple flood valleys with turbulent water.  To empower this village, there are some windfarms nearby. Cheetahs in the mountains need to be preserved. Food and potable water can be very valuable here."
    Input resources: cheetah, fresh water, wind, biomass, groundwater, wild herbs, flora, potable water, irrigation water, mountain soil, spring water, timber, medicine plants, granite, geothermal energy
    Environment description:"{envir_description}"
    Input resources: 
    """

    input_prompt_template = PromptTemplate(
        input_variables=["envir_description"],
        template=input_template,
    )

    input_chain = LLMChain(
        llm=input_llm,
        prompt=input_prompt_template,
        output_key="input_resources",
        verbose=False,
    )  

    input_resources = input_chain.run({"envir_description": envir_description}).split(",")
    clean_input=[clean(i) for i in input_resources]
    #get unique input
    unique_input=[]
    for i in clean_input:
        if i not in unique_input:
            unique_input.append(i)
    return unique_input

def returninput(env,max_tries=3):
    input=getinput(env)
    #while tries is less than max_tries, check if the inputlist is a nested list
    while checktype(input)==False and max_tries>0:
        input=(getinput(env))
        max_tries-=1
    #if the inputlist is not a nested list after max_tries, return error message
    if checktype(input)==False:
        return "Sorry, we can't generate result from the environment description, please try again."
    else:        
        return input

### Get output from environment description


def getsimpleflow(input_resources,randomNumber=3):
    insertstring=f'{input_resources}'
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
        {"role": "system", "content": '''    
         You are a environmental engineering specialist, given the input resources, please come up with output resources. 
         These output resources are values and helpful optimize the environmental process to achive net zero energy, net zero carbon, and net positive water systems. Please come up with two to three output for each input.
         
         I will ask in this list format:["input1","input2","input3"], such as ["waste water", "organic waste", "wind energy"].
         Step 1, think for each input in the list, such as "waste water" can generate "fresh water" and "nutrients".
         Step 2, please also try multiple inputs to co-optimize, such as "waste water" and "organic waste" can be combined in digestor to generate "biofuel".
         Please answer in this list format, please put the co-optimized output in each input list, such as:
         [  ["input1":["output1","output2","co-optimized output3"]],
            ["input2":["output1","output2","co-optimized output3"]],
            ["input3":["output1","output2"]], ]'''},
        {"role": "user", "content": '''["waste water", "organic waste", "wind energy"]'''},
        {"role": "assistant", "content": '''[["waste water":["fresh water","nutrients","biofuel"]], ["organic waste":["biofuel"; "biogas"]], ["wind":["electricity","humidity"]]]'''},
        {"role": "user", "content": '''["salt water", "organics"]'''},
        {"role": "assistant", "content": ''' [["salt water":["NaCl","fresh water"]], ["organic waste":["biofuel","biogas"]]]'''},     
        {"role": "user", "content": '''["wetland", "non-potable water storage"]'''},
        {"role": "assistant", "content": ''' [["wetland":"irrigation"], ["non-potable water storage":["irrigation","water treatment"]]]'''},                                             
        {"role": "user", "content": insertstring},
        ],
        temperature=1,
        n=randomNumber,
    )
    return response['choices'][0]['message']['content']



def convertsimpleflow(output_string):
    # Get the first index of "["
    first_index = output_string.index("[")
    # Get the last index of "]"
    last_index = output_string.rindex("]")
    # Get the string between first and last index
    new_string = output_string[first_index+1:last_index]
    flowlist=[]
    tempflow=extract_brackets(new_string)
    for temp in tempflow:
        #str_input is like "waste water":["fresh water","nutrients"], split it by ":", get ["waste water",["fresh water","nutrients"]]
        flow_str=temp.split(":")
        templist=extract_quotation(flow_str[1])
        #loop through templist
        for i in range(len(templist)):
            flow_temp=[]
            flow_temp.append(clean(flow_str[0]))
            flow_temp.append(clean(templist[i]))
        flowlist.append(flow_temp)
    return flowlist

def returnsimpleflow(input_resources,max_tries=5):
    #while tries is less than max_tries, check if the flowlist is a nested list

    simpleflow=[]
    toggle=False

    while toggle==False and max_tries>0:
        try:
            random_number = random.randint(1, 20)
            flow_string=getsimpleflow(input_resources,random_number)
            print(flow_string)
            simpleflow=(convertsimpleflow(flow_string))
            print(simpleflow)
            toggle=checknestedlist(simpleflow)
            print(f'simpleflow toggle is {toggle}')
        except:
            toggle=False
            continue
        max_tries-=1
    #if the flowlist is not a nested list after max_tries, return error message
    if toggle==False:
        return "Sorry, we can't generate the flow from the environment description, please try again."
    else:
        json_object = json.dumps(simpleflow, indent=4)
        with open("static/simple/simpleflow.json", "w") as outfile:
            outfile.write(json_object)

        return simpleflow

### Get system from simpleflow
def getelement(flowlist):
    elementlist=[]
    #if flowlist contains sublist
    if checknestedlist(flowlist):
        for sublist in flowlist:
            for ele in sublist:
                unique=clean(ele)
                if unique not in elementlist:
                    elementlist.append(unique)
    return elementlist

# def getelement(flowlist):
#     elementlist=[]
#     #if flowlist contains sublist
#     if checknestedlist(flowlist):
#         for sublist in flowlist:
#             for ele in sublist:
#                 if ";" in ele:
#                     split_list=ele.split(";")
#                     for j in split_list:
#                         unique=clean(j)
#                         if unique not in elementlist:
#                             elementlist.append(unique)
#                 else:
#                     unique=clean(ele)
#                     if unique not in elementlist:
#                         elementlist.append(unique)
#     return elementlist


def classify(flowlist,element=None,randomNumber=3):
    if element==None:
        element=getelement(flowlist)
    insertstring=f'{element}'
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
        {"role": "system", "content": 
            '''You are an encyclopedia. Your job is to classify the element. I will give you an element list, and you will classfy each element in the list to 'ecosystem', 'energy', 'hydro'.
            You will think in the following step to output the classified system. Below are the step for this element list ["water","hydropower"] as an examples 
            Step1: Read every element in the elment list, like "water", "hydropower"
            Step2: Classify every element in the element list, like "water" is classified in "hydro", "hydropower" is classified in "energy". Please be rigourous with classification.
                    Output "unknown" if the element cannot be classified.
            Step3: Output the classified system in json format, like [["water":"hydro"],["hydropower","energy"]]

            Please provide the element list to classify:
                  
            '''},
        {"role": "user", "content": '''["Cheetah", "wildlife corridors", "wadis"]'''},
        {"role": "assistant", "content": '''[["Cheetah","ecosystem"], ["wildlife corridors","ecosystem"], ["wadis", "hydro"]]'''},
        {"role": "user", "content": ''' ["forest", "irrigation", "organic waste", "biofuel"]'''},
        {"role": "assistant", "content": '''[["forest","ecosystem"], ["irrigation","hydro"], ["organic waste", "ecosystem"], ["biofuel","energy"]]'''},
        {"role": "user", "content": '''["water","hydropower"]'''},
        {"role": "assistant", "content": ''' [["water","hydro"],["hydropower","energy"]]'''},     
        {"role": "user", "content": '''["knowledge","reduced vulnerability"]'''},
        {"role": "assistant", "content": ''' [["knowledge","unknown"],["reduced vulnerability","unknown"]]'''},
        {"role": "user", "content": insertstring},
        ],
        temperature=0.7,
        n=randomNumber,
    )
    return response['choices'][0]['message']['content']



def convertsystem(sys_string):
    if type(sys_string)==list:
        sys_string=f"{sys_string}"
    # Get the first index of "["
    first_index = sys_string.index("[")
    # Get the last index of "]"
    last_index = sys_string.rindex("]")
    # Get the string between first and last index
    new_string = sys_string[first_index+1:last_index]

    systemdict={}
    tempflow=extract_brackets(new_string)
    for temp in tempflow:
        result=extract_quotation(temp)
        try:
            systemdict[clean(result[0])]=clean(result[1])
        except:
            print(f'{result} for flow {temp} cannot be classified')
            continue
    return systemdict

def returnsystem(simpleflowlist=None,max_tries=5,path="static/simple/sample.json",inputelement=None):
    systemdict={}

    #check if the len of systemdict is equal to the len of unique element of simpleflowlist
    if inputelement:
        unique_element=inputelement
    else:
        unique_element=getelement(simpleflowlist)
    print(unique_element)
    while len(systemdict)!=len(unique_element) and max_tries>0:
        try:
            randomNumber = random.randint(1, 20)
            sys_string=classify(simpleflowlist,unique_element,randomNumber)
            print(sys_string)
            systemdict=convertsystem(sys_string)
            max_tries-=1
        except:
            continue
    #if systemdict is empty after max_tries, return error message

    if len(systemdict)!=len(unique_element):
        print(unique_element)
        print(len(unique_element))
        print("/n")
        print(systemdict.keys())
        print(len(systemdict))
        return "Sorry, we can't classify the elements, please try again."
    else:
        json_object = json.dumps(systemdict, indent=4)
        with open(path, "w") as outfile:
            outfile.write(json_object)
        with open("static/dataset/sample_raw.json", "a") as outfile:
            outfile.write(json_object)
        return systemdict

def color(dict,path="static/simple/samplecolor.json"):
    #ecosystem-green:#39b54a, energy-yellow:#ffc60b, hydro-blue: #00aeef
    colordict={}
    for item in dict:
        print(f'{item} belongs to {dict[item]}')        
        if dict[item]=='ECOSYSTEM':
            colordict[item]="#39b54a"
        elif dict[item]=='ENERGY':
            colordict[item]="#ffc60b"
        elif dict[item]=='HYDRO':
            colordict[item]="#00aeef"
        else:
            colordict[item]="lightgrey"
   
    # Serializing json
    json_object = json.dumps(colordict, indent=4)
    
    # Writing to sample.json
    with open(path, "w") as outfile:
        outfile.write(json_object)

    return colordict
    
### Build Simple Matrix

def getsimpley(simplelist):
    systemcount={'HYDRO':0,'ENERGY':0,'ECOSYSTEM':0,'UNKNOWN':0}
    subcount={}

    with open('static/simple/sample.json') as json_file:
        systemdict = json.load(json_file)

    unique_values = []
    for ele in simplelist:
        tempsystem=systemdict[ele]
        if tempsystem not in systemcount:
            #add the value to unique_values
            unique_values.append(tempsystem)
            #add the count to systemcount 
            systemcount[tempsystem]=1
            #set the subcount of the element to systemcount
            subcount[ele]=systemcount[tempsystem]
        else:
            systemcount[tempsystem]+=1
            subcount[ele]=systemcount[tempsystem]

    #loop through systemdict,  if the key is "HYDRO", keep the value; if the key is "ENERGY", add the value with the length of "HYDRO"; if the key is "ECOSYSTEM", add the value with the length of "HYDRO" and "ENERGY"
    yindex={}
    for ele in simplelist:
        if systemdict[ele]=="HYDRO":
            yindex[ele]=subcount[ele]
        elif systemdict[ele]=="ENERGY":
            yindex[ele]=subcount[ele]+systemcount["HYDRO"]
        elif systemdict[ele]=="ECOSYSTEM":
            yindex[ele]=subcount[ele]+systemcount["ENERGY"]+systemcount["HYDRO"]
        else:
            yindex[ele]=subcount[ele]+systemcount["ENERGY"]+systemcount["HYDRO"]+systemcount["ECOSYSTEM"]
    return yindex
    
def simplematrix(simpleflow):
    #simpleflow is a nested list of flow, get the unique element in each sublist, and get the xpoistion, yposition of each element
    listinput=[]
    listoutput=[]
    for sublist in simpleflow:
        if sublist[0] not in listinput:
            listinput.append(sublist[0])
        if sublist[1] not in listoutput:
            listoutput.append(sublist[1])

    #write the input and output list to json
    json_object = json.dumps(listinput, indent=4)
    with open("static/simple/input.json", "w") as outfile:
        outfile.write(json_object)
    json_object = json.dumps(listoutput, indent=4)
    with open("static/simple/output.json", "w") as outfile:
        outfile.write(json_object)

    yindexinput=getsimpley(listinput)
    yindexoutput=getsimpley(listoutput)
    


    sorted_input=[]
    sorted_output=[]
    # sort the input by yindex
    for ele in sorted(yindexinput, key=yindexinput.get):
        sorted_input.append(ele)
    # sort the output by yindex
    for ele in sorted(yindexoutput, key=yindexoutput.get):
        sorted_output.append(ele)

    #write the input and output list to json
    json_object = json.dumps(sorted_input, indent=4)
    with open("static/simple/sorted_input.json", "w") as outfile:
        outfile.write(json_object)
    json_object = json.dumps(sorted_output, indent=4)
    with open("static/simple/sorted_output.json", "w") as outfile:
        outfile.write(json_object)

    #open color.json
    with open('static/simple/samplecolor.json') as json_file:
        colordict= json.load(json_file)

    matrixdict={}
    for ele in listinput:
        if yindexinput[ele] and colordict[ele]:
            matrixdict[ele]=[colordict[ele],0,yindexinput[ele]]
        else:
            matrixdict[ele]=["white",0,0]

    for ele in listoutput:
        if yindexoutput[ele] and colordict[ele]:
            matrixdict[ele]=[colordict[ele],1,yindexoutput[ele]]
        else:
            matrixdict[ele]=["white",1,0]


    #get the max length of listinput and listoutput
    maxlen=max(len(listinput),len(listoutput))
    matrixdict["TOTAL"]=["white",2,maxlen]
    json_object = json.dumps(matrixdict, indent=4)
    with open("static/simple/simplematrix.json", "w") as outfile:
        outfile.write(json_object)
    return matrixdict


######################################################
######################################################
if __name__=="__main__":
    pass
    # env1="This scene depicts an agricultural village in the mountains. There are a couple flood valleys with turbulent water. To empower this village, there are some windfarms nearby. Cheetahs in the mountains need to be preserved. Food and potable water can be very valuable here."
    # env2= "This scene features a coastal resort, many off-grid infrastructure, luxury camping."
    # env3= "This scene is an industrial wasteland."  
    # env4="This landscape showcases a dense tropical rainforest, with a shimmering river winding its way through. Rare birds fly overhead, and there's a distant sound of a waterfall. Conservation efforts are visible with designated wildlife sanctuaries. The native tribes have sustainable huts made of natural materials."
    # env5= "This scene is a bustling urban metropolis, with skyscrapers reaching for the heavens. Amidst the concrete jungle, rooftop gardens provide a touch of green. A network of trams and electric buses navigate the streets, emphasizing the city's push towards sustainability."
    # env6= "Here, we have a vast, arid desert landscape. Amidst the golden dunes, there are patches of oasis settlements with date palms. Nomadic tribes travel with their camels, leaving trails in the sand. Solar panels harnessing the sun's energy are a common sight, highlighting the people's adaptability."
    # env7= "This scene portrays a frozen tundra, where the ground is blanketed by snow and ice. Hardy wildlife, such as polar bears and seals, are seen navigating this chilly expanse. Ice fishing villages, with their igloos and sled dogs, depict the resilience of life in extreme cold."
    # env8= "A serene archipelago is depicted, where turquoise waters surround clusters of islands with white sandy beaches. Mangroves and coral reefs thrive in this marine sanctuary. Island inhabitants live in stilt houses, using boats for transportation and fishing."
    # env9= "This scene reveals a misty highland plateau. The grasslands are dotted with wildflowers, and there's a peaceful herd of grazing bison. Farther in the distance, you can spot an ancient stone observatory, a testament to the region's historical significance."
    # env10= "This area showcases a dense bamboo forest. The whispers of the breeze sound like a soft melody. Occasional clearings reveal panda sanctuaries, where these gentle giants munch away contentedly. Nearby villages specialize in crafting bamboo products, reflecting a symbiotic relationship with nature."
    # env11= "This environment is a sprawling wetland. The horizon is dominated by reeds, lily pads, and a mosaic of water channels. Flocks of migratory birds rest here, and it's not uncommon to spot a crocodile basking in the sun. Locals use wooden canoes to traverse this watery realm."
    # env12= "Here lies a volcanic region, with smoky peaks and rugged terrain. Lava flows have carved unique landforms, and geothermal springs dot the landscape. Local communities have tapped into this geothermal energy, making the most of their challenging surroundings."
    # env13= "This scene portrays a vast savannah, where the horizon seems endless. Acacia trees punctuate the golden grasslands, and the distant rumble of an approaching wildebeest migration can be felt. Nearby, a tribe dances around a fire, celebrating the bounty this land offers."
    # env14= "This setting reveals a deep canyon with a river snaking through its base. Jagged cliffs house nesting eagles, and one can hear the distant echo of a Native American flute. Cliffside villages rely on the river's bounty and have built suspension bridges to connect communities."

    # env15= "This area displays a lush mangrove forest, where roots dive deep into the brackish waters. Brightly colored crabs scuttle about, and the chirping of unseen insects is constant. Fishermen navigate through channels, casting nets in a dance as old as time."

    # env16= "This place is an expansive grassy steppe, interrupted only by occasional rocky outcrops. Herds of horses gallop freely, their manes flowing with the wind. Yurts dot the landscape, home to the nomads who master this land."

    # env17= "Here, we witness a vibrant coral reef, bursting with marine life. Schools of fish dart between anemones, while turtles glide majestically overhead. On the shores, locals have established eco-resorts, with a focus on marine conservation."

    # env18= "This environment is a dense cloud forest, where every surface is cloaked in moss and ferns. Water droplets hang in the air, and colorful orchids bloom in the canopy. Zip-lining tours provide a thrilling perspective, promoting eco-tourism."

    # env19= "This scene unveils a sprawling salt flat, reflecting the sky like a vast mirror. During rainy seasons, it becomes a surreal, otherworldly landscape. Nearby communities harvest salt and have made art out of its crystalline forms."

    # env20= "Here, we have a serene tea plantation on rolling hills. Rows upon rows of green stretch far, with workers meticulously picking leaves. Traditional ceremonies honor the earth, and eco-lodges offer tranquil retreats."

    # env21= "This setting features a dark, mysterious swamp, where ancient trees are draped in Spanish moss. Fireflies illuminate the twilight, and the hoot of an owl breaks the silence. Boardwalks guide visitors through, revealing the beauty in the shadows."

    # env22= "This place portrays a rocky coastline, where waves crash against cliffs and sea caves beckon explorers. Tide pools brim with marine creatures, and seals bask on offshore rocks. Lighthouses stand guard, guiding ships and telling tales of old."

    # env23= "This environment showcases a bustling port city, where tradition meets modernity. Ancient temples stand side by side with factories. Colorful markets spill onto streets, and energy-efficient ferries crisscross the harbor."

    # env24= "Here lies a serene lavender field, stretching to the horizon. The gentle hum of bees fills the air, and the scent is intoxicating. Traditional farms offer organic products, promoting sustainable agriculture."

    # env25= "This setting is a sprawling vineyard, where rows of grapevines undulate with the terrain. Wineries built with reclaimed materials offer tastings, and solar panels power operations. The community celebrates with an annual harvest festival."

    # env26= "This scene depicts a dense, moss-covered forest, where ancient trees tower overhead. Streams babble, and deer tread softly. Wooden cabins with green roofs blend seamlessly, emphasizing coexistence with nature."

    # env27= "Here, we have a bustling harbor town. Fishing boats return with their catch, while wind turbines rotate in the distance. The town square features a weekly farmer's market, emphasizing local produce and sustainability."

    # env28= "This environment captures a serene lotus pond, surrounded by willow trees. The gentle splash of koi fish and croaking of frogs create an ambient soundtrack. Nearby temples practice water conservation, drawing from this natural resource."

    # env29= "This place showcases a rugged mountain pass, where snow-capped peaks touch the heavens. Monasteries perched on cliffs overlook deep valleys. Villagers practice terrace farming, making use of every inch of arable land."

    # env30= "This scene is a bustling bee farm, where hives are organized in neat rows. Fields of wildflowers stretch beyond, providing a buffet for the bees. The community promotes organic farming and holds an annual honey festival."

    # env31= "Here lies a tranquil zen garden, with meticulously raked sand and strategically placed rocks. Bonsai trees and koi ponds add to the serenity. Meditation retreats are offered, promoting mental well-being and harmony with nature."

    # env32= "This setting depicts a sun-drenched olive grove. Trees stretch in all directions, their silver leaves shimmering in"
   
   
   
    # # env="Draw a science magazine illustration which contains mountain valley with wadis(), and agricultural village, and farms.This also shows geology substrate. Watercolor, fine-detailed.camera angle should be strictly section, or perspective section "
    # # url=getcanvas(env)
    # # urllib.request.urlretrieve(url, "static/envir.png")
    
    # print("\n")
    # input=(returninput(env5))
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



 
    # simpleflow=[['MOUNTAINOUS TERRAIN', 'FACILITIES (CABLE CARS, HIKING TRAILS, CAMPING SITES)', 'TOURISM OPPORTUNITIES'], ['MOUNTAINOUS TERRAIN', 'ACTIVITIES (MOUNTAINEERING, TREKKING, SKI RESORTS)', 'TOURISM OPPORTUNITIES'], ['MOUNTAINOUS TERRAIN', 'ECO-TOURISM (CONSERVATION OF NATURE, FLORA, AND FAUNA)', 'TOURISM OPPORTUNITIES'], ['MOUNTAINOUS TERRAIN', 'CULTURAL TOURISM (TRADITIONS, LIFESTYLE OF LOCAL TRIBES)', 'TOURISM OPPORTUNITIES']]
    # systemdict=returnsystem(simpleflow)
    # print(systemdict)


    # simpleflowlist=simpleflow(result)

    # # test_simpleflow=[["OCEAN CURRENT","WAVE ENERGY"],["WAVE ENERGY","WAVE ENERGY PLANT"],["WAVE ENERGY","GRID"],["FUEL","GRID"],["SEA LIFE","FISHERIES"],["FIRE","FUEL"]]
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

    # test=f'[["SOLAR ENERGY":["electricity","reduced carbon emissions"]],["SALTWATER":["desalination","salt production"]],["BEACH SAND":["building material","erosion control"]],["CORAL REEF":["biodiversity conservation","tourist attraction"]],["SEAWEED":["biofuel production","nutrient absorption"]],["MARINE LIFE":["ecosystem balance","oxygen production"]],["FISH":["food source","economic value"]],["SEASHELLS":["beach souvenirs","decoration material"]],["SEA BREEZE":["cooling effect","renewable energy"]],["WAVE ENERGY":["electricity generation","reduced reliance on fossil fuels"]],["SEAFOOD":["nutrient-rich food","source of income"]],["MANGROVES":["coastal protection","carbon sequestration"]],["HAMMOCKS":["relaxation","tourist attraction"]],["COCONUT WATER":["refreshing beverage","hydration"]],["PALM TREES":["shade","landscaping"]],["TOURISM":["economic growth","cultural exchange"]],["ECO-TOURISM":["environmental education","sustainable development"]],["CLEAN ENERGY":["reduced greenhouse gas emissions","energy independence"]],["RECYCLABLE MATERIALS":["resource conservation","waste reduction"]],["COMPOST":["soil enrichment","organic waste management"]],["OCEAN VIEWS":["scenic beauty","property value"]],["BIOFUELS":["renewable fuel source","reduced carbon emissions"]],["BEACH CLEANUPS":["waste reduction","community engagement"]],["BEACH ACTIVITIES":["recreation","stress relief"]],["ORGANIC FARMING":["chemical-free food production","soil health"]],["SEAFOOD RESTAURANTS":["culinary experience","support for local economy"]],["OUTDOOR GAMES":["physical activity","social interaction"]],["SEAGULLS":["marine ecosystem indicator","bird watching"]],["COASTAL VEGETATION":["erosion prevention","habitat for wildlife"]],["BEACH CHAIRS":["comfort","relaxation"]],["BEACH UMBRELLAS":["shade","sun protection"]],["BEACH TOWELS":["comfort","beach accessory"]],["RESORT FACILITIES":["accommodation","recreation options"]],["OCEAN WATER":["recreation","health benefits"]],["TIDE ENERGY":["renewable energy generation","reduced reliance on fossil fuels"]],["BEACH PARTIES":["celebration","social gathering"]],["SNORKELING":["marine exploration","recreational activity"]],["DIVING":["underwater adventure","marine conservation"]]]'
    # result=convertsimpleflow(test)
    # print(result)

    # obejct=json.load(open("static/simple/simpleflow.json"))
    # print(obejct)
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


# def classify(flowlist,element=None):
#     #flow is the list processed from last llm string
#     # if element doesn't exist, get the element from flowlist
#     if element==None:
#         element=getelement(flowlist)

#     classify_template = """You are to classify the element. I will give you an element list and you are to classfy each element in the list to 'ecosystem', 'energy', 'hydro'.
#         You think in the following step to output the classified system. I will use an element list like ["water","hydropower"] to explain. 
#         Step1: Read every element in the elment list, like "water", "hydropower"
#         Step2: Classify every element in the element list, like "water" is classified in "hydro", "hydropower" is classified in "energy". Please be rigourous with classification.
#         Step3: Output the classified system in json format, like [["water":"hydro"],["hydropower","energy"]]

#         Here are output examples:
#         element: ["Cheetah", "wildlife corridors", "wadis"]
#         classified: [["Cheetah","ecosystem"], ["wildlife corridors","ecosystem"], ["wadis", "hydro"]]
#         ##
#         element: ["forest", "irrigation", "organic waste", "biofuel"]
#         classified: [["forest","ecosystem"], ["irrigation","hydro"], ["organic waste", "ecosystem"], ["biofuel","energy"]]
#         ##
#         element:["water","hydropower"]
#         classified: [["water","hydro"],["hydropower","energy"]]
#         ##             
#         element: {element}
#         classified: 

#     """

#     classify_prompt_template = PromptTemplate(
#         input_variables=["element"],
#         template=classify_template,
#     )

#     classify_chain = LLMChain(
#         llm=classify_llm , prompt=classify_prompt_template, verbose=False
#     ) 
        
#     classified = classify_chain.run({"element":element})

#     return classified


# output_llm=ChatOpenAI(model="gpt-4",temperature=1.0)
# def getsimpleflow(input_resources):
#     #input_resources is a list of input resources
#     output_template = """
#     You are a environmental engineering specialist, given the input resources, you will come up with output resources. These output resources are values and helpful optimize the environmental process to achive net zero energy, net zero carbon, and net positive water systems. Please come up with two to three output for each input.
#     Generate a list of json, one json for each input element.

#     Input resources: ["waste water", "organic waste", "wind"]
#     Output resources: [["waste water":["fresh water","nutrients"]], ["organic waste":["biofuel"; "biogas"]], ["wind":["electricity","humidity"]]]
#     Input resources: ["salt water", "organics"]
#     Output resources:[["salt water":["NaCl","fresh water"]],["organic waste":["biofuel","biogas"]]]
#     Input resources: "{input_resources}"
#     Output resources:
#     """

#     output_prompt_template = PromptTemplate(
#         input_variables=["input_resources"],
#         template=output_template,
#     )

#     output_chain = LLMChain(
#         llm=output_llm, prompt=output_prompt_template, verbose=False
#     )  
#     output_resources = output_chain.run({"input_resources": input_resources})
#     return output_resources