
import os
import json
import re
import openai
import langchain
from langchain.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

os.environ["HUGGINGFACEHUB_API_TOKEN"] =  "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"
os.environ["OPENAI_API_KEY"] = "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"

######################################################
######################################################
#Helper Functions

def clean(input_string):
    "clean a string to make it start with letter and end with letter, and all the cases are upper"
    cleaned_string = re.sub(r'^[^a-zA-Z]+|[^a-zA-Z]+$', '', input_string)
    return cleaned_string.upper()

def has_letters(string):
    return any(char.isalpha() for char in string)


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
    return image_url



######################################################
######################################################
#Task 2 - Flow Generater
#Generate input from environment description
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.cache import InMemoryCache
langchain.llm_cache = InMemoryCache()

# Template for generating input resources and what variables (using the {text} syntax) it should use.
input_llm = ChatOpenAI(model="gpt-4",temperature=1)

def getinput(envir_description):
    input_template = """
    You are a environmental engineering specialist, you will extract and imagine potential resources in the environment description as keywords. The resources in the environment include potential organisms, chemicals, materials; and they come from various systems, such as hydro, energy, and ecosystem. Please try to imagine as much as possonible, and provide me around 40 in total.

    Environment description: "This scene depicts an agricultural village in the mountains. There are a couple flood valleys with turbulent water.  To empower this village, there are some windfarms nearby. Cheetahs in the mountains need to be preserved. Food and potable water can be very valuable here."
    Input resources: cheetah, fresh water, biomass, groundwater, wild herbs, flora, potable water, irrigation water
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
    return clean_input


#Generate output from input list
flow_llm = ChatOpenAI(model="gpt-4",temperature=1.0)

def getflow(envir_description):
    element=getinput(envir_description)

    flow_template = """You are to generate the flow from element. 
        The flow is a sequenced list of processes, resources, and technology that transform input resources to output resources, going from the first index to the last one. 
        Element at every index of the flow list is a result of the previous index.The flow list is usually three to ten index long. 
        The element could be any index of the flow list, and can be part of the index when paired by synonyms or related elements. 
        The flow is to optimize the environmental process to achive net zero energy, net zero carbon, and net positive water systems. 
        Generate a list of json, one json for each input element.

        Element: ["DEEP INJECTION WELLS","BRINE","SALT EVAPORATION POND"]
        Flow:[["BRINE", "DEEP INJECTION WELLS"], ["BRINE", "REPRODUCTION PROCESS", "BASO4;NACL"], ["BRINE", "SALT EVAPORATION POND"]]
        Element: ["IRRIGATION"]
        Flow:[["WASTE WATER TREATMENT;WASTEWATER TREATMENT", "IRRIGATION WATER;IRRIGATION", "REVEGETATION;REGREENING;ADAPTIVE GREENHOUSES"]]
        Element:["REGREENING","WWT"]
        Flow:[["GREY WATER;GREYWATER; WASTE WATER", "TREATMENT WETLAND;IRRIGATION WATER", "REVEGETATION;REGREENING;ADAPTIVE GREENHOUSES"],["GREY WATER;GREYWATER; WASTE WATER", "WASTEWATER TREATMENT PLANT;WWT;TREATED WATER;RECYCLED WATER;ASSET; BUILDINGS"]]
        Element: ["DESALINATION","SWEET WATER"]
        Flow:[["SALT WATER", "DESALINATION PLANT;DESALINATION"], ["SALT WATER", "INVERSE OSMOSIS", "SWEET WATER;FRESH WATER;FRESHWATER"]]
        Element:["DESSICANT MATERIAL","SPIDER SILK","FLOOD","WAVE"]
        Flow:[["DESSICANT MATERIAL", "INVERSE OSMOSIS", "SWEET WATER;FRESH WATER"], ["DEPLOYABLE SYNTHETIC SPIDER SILK; SPIDER SILK", "INVERSE OSMOSIS"], ["MOISTURE HARVESTING;DEW COLLECTION;RAINFALL;FLOOD", "IRRIGATION"], ["OCEAN WAVES;WAVE;WAVES", "WAVE ATTENUATER; ENERGY GENERATOR", "ELECTRICITY"]]
        Element: ["PHOTOSYNTHESIS","GRID","POTABLE WATER"]
        Flow:[["CHILOROPHYLL", "PHOTOSYNTHESIS", "OXYGEN"], ["CHILORINE; SODIUM HYDROXIDE", "ELECTROLYSIS", "ELECTRICITY; GRID;ELECTRICITY GRID"], ["DESALINATION FACILITY", "BRINE; POTABLE WATER"]]
        Element:["BATTERY","WIND","CROPS","REGENERATIVE AGRICULTURE", "COMPOST"]
        Flow:[["HYDROGEN", "BATTERY STORAGE;BATTERY"], ["WIND","WIND TURBINE", "ELECTRICITY; GRID; BATTERY STORAGE; BATTERY"], ["REGENERATIVE AGRICULTURE", "SOIL CARBON;CROPS;FOOD"], ["REGENERATIVE AGRICULTURE", "ASSETS; BUILDINGS; FOOD"], ["WASTE; ORGANIC WASTE", "COMPOST; FERTILIZER", "VEGETATION"]]
        Element: ["ORGANICS","BIOCHAR","ALGAE","BATTERY","ELECTRICITY"]
        Flow:[["ORGANICS", "BIODIGESTOR; BIOGAS; BIOFUEL"], ["BIODIGESTER", "METHANE;METHANE-BASED ENERGY", "BIOCHAR;HYDROGEN FUEL CELLS"], ["ALGAE; ALGAE TIDE", "BIOMASS GENERATOR; ALGAE TUBE WASTEWATER TREATMENT"], ["BIOFUEL", "BATTERY"], ["ELECTRICITY", "GRID;BATTERY"]]
        Element: ["HYDRO PUMP","LEAVES", "ALGAE PRODUCE FARM","WADIS"]
        Flow:[["HYDRO PUMP", "ELECTRICITY; GRID"], ["MANGROVE; HALOPHYTE-BASED AGRICULTURE", "LEAVES; LEAF LITTER", "FOOD FOR SHRIMP; FOOD FOR CRAB", "SEA FARM TO TABLE"], ["ORGANIC MARINE DEBRIS", "ALGAE PRODUCE FARM"], ["FRESH WATER; FRESH FLOW; WADIS", "LAGOONS; WETLANDS"]]
        Element: ["MANGROVES","VADOSE WELLS"]
        Flow:[["MANGROVES;VEGETATION; GREENING; REGREENING; FORESTATION", "BIO-FILTRATION; INCREASE INFILTRATION", "VADOSE WELLS", "INCREASED GROUND WATER RECHARGE"]]
        Element: ["AQUACULTURE","FOOD"]
        Flow:[["AQUACULTURE;AQUACULTURE FISH HOUSE; SEA FARM", "FOOD; FOOD FOR ASSETS; FOOD FOR BUILDINGS; FOOD FOR PEOPLE;TABLES"]]
        Element: {element}
        Flow:
    """

    flow_prompt_template = PromptTemplate(
        input_variables=["element"],
        template=flow_template,
    )

    flow_chain = LLMChain(
        llm=flow_llm, prompt=flow_prompt_template, verbose=False
    )  
    flow_string= flow_chain.run({"element": element})

    return flow_string

def extract_brackets(text):
    pattern = r'\[(.*?)\]'  # Regular expression pattern to match strings between "[" and "]"
    matches = re.findall(pattern, text)  # Find all matches of the pattern in the text
    return matches


def extract_quotation(text):
    matches = re.findall('"(.*?)"', text)
    return matches


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
        flowlist.append(templist)

    json_object = json.dumps(flowlist, indent=4)
    with open("static/v2/flow.json", "w") as outfile:
        outfile.write(json_object)
    with open("static/dataset/flow_raw.json", "a") as outfile:
        outfile.write(json_object)
    return flowlist


######################################################
######################################################
#Task 3 - Classify Elements

def getelement(flowlist):
    elementlist=[]
    for sublist in flowlist:
        for ele in sublist:
        #if ele contains ";", split it at ";" and clean each element
            if ";" in ele:
                split_list=ele.split(";")
                for j in split_list:
                    elementlist.append(clean(j))
            else:
                elementlist.append(clean(ele))
    return elementlist

classify_llm = ChatOpenAI(model="gpt-4",temperature=1.0)


def classify(flowlist):
    #flow is the list processed from last llm string
    element=getelement(flowlist)

    classify_template = """You are to classify the element.
        Every element belong to one system and each has a fixed corresponding color. They are ecosystem:#39b54a, energy:#ffc60b, hydro:#00aeef.
        You are to output the classified system and color in json format.

        element: ["Cheetah", "wildlife corridors", "wind speed assessment", "water","hydropower"]
        classified: [["Cheetah","ecosystem","#39b54a"], ["wildlife corridors","ecosystem","#39b54a"], ["wind speed assessment", "energy", "#ffc60b"], ["water","hydro","#00aeef"],["hydropower","energy","#ffc60b"]]
        element: ["forest", "irrigation", "organic waste", "food"]
        classified: [["forest","ecosystem","#39b54a"], ["irrigation","hydro","#00aeef"], ["organic waste", "energy", "#ffc60b"], ["food","ecosystem","#39b54a"]]
        element: {element}
        classified: 

    """

    classify_prompt_template = PromptTemplate(
        input_variables=["element"],
        template=classify_template,
    )

    classify_chain = LLMChain(
        llm=classify_llm , prompt=classify_prompt_template, verbose=False
    ) 
        
    classified = classify_chain.run({"element":element})

    return classified


def convertelement(flow_string):
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
        flowlist.append(templist)

    json_object = json.dumps(flowlist, indent=4)
    with open("static/v2/sample.json", "w") as outfile:
        outfile.write(json_object)
    with open("static/dataset/sample_raw.json", "a") as outfile:
        outfile.write(json_object)
    return flowlist

# zero_shot_pipeline = pipeline(
#     task="zero-shot-classification",
#     model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli",
#     model_kwargs={"cache_dir": "__pycache__/dataset"},
#     tokenizer = AutoTokenizer.from_pretrained("MoritzLaurer/mDeBERTa-v3-base-mnli-xnli", use_fast=False)
# )

# def categorize(dict):
#     """
#     This helper function defines the categories (labels) which the model must use to label articles.
#     Note that our model was NOT fine-tuned to use these specific labels,
#     but it "knows" what the labels mean from its more general training.

#     This function then prints out the predicted labels alongside their confidence scores.
#     """
#     categorydict={}
#     for item in getlist(dict):
#         results = zero_shot_pipeline(
#             item,candidate_labels=["hydro","energy","ecosystem",],)
#        # del results["sequence"]
#         if item not in categorydict.keys():
#             categorydict[item]=results['labels'][0]

#     return categorydict


# def color(dict):
#     #ecosystem-green:#39b54a, energy-yellow:#ffc60b, hydro-blue: #00aeef
#     colordict={}
#     for item in dict:
#         if dict[item]=='ecosystem':
#             colordict[item]="#39b54a"
#         elif dict[item]=='energy':
#             colordict[item]="#ffc60b"
#         elif dict[item]=='hydro':
#             colordict[item]="#00aeef"
#         else:
#             colordict[item]="white"
   
#     # Serializing json
#     json_object = json.dumps(colordict, indent=4)
    
#     # Writing to sample.json
#     with open("static/sample.json", "w") as outfile:
#         outfile.write(json_object)

#     return colordict
    
######################################################
######################################################
if __name__=="__main__":
    #pass
    env="This scene depicts an agricultural village in the mountains. There are a couple flood valleys with turbulent water. To empower this village, there are some windfarms nearby. Cheetahs in the mountains need to be preserved. Food and potable water can be very valuable here."
    #env="This scene depicts a coastal environment."
    #print (getinput(env))
    # print("\n")
    result=(convertflow(getflow(env)))
    print(result)
    print("\n")
    print(convertelement(classify(result)))



    # print(result.types())
    # test=f'[["MOUNTAIN ROCKS", "WEATHERING PROCESS;WIND ENERGY", "SOIL;MINERALS"], ["RIVER WATER; LOCAL WEATHER DATA; PRECIPITATION; ATMOSPHERIC MOISTURE; DEW WATER; FLOOD WATER", "WATER TREATMENT FACILITY", "WATER EXTRACTION; WATER CONSERVATION"], ["WIND ENERGY", "WIND TURBINES; WINDFARM INFRASTRUCTURE", "ELECTRICITY GENERATION; RENEWABLE ENERGY"], ["AGRO WASTE; ANIMAL MANURE; VILLAGE WASTE; HUMAN WASTE", "BIOGAS DIGESTER; COMPOSTING", "BIOMASS ENERGY; COMPOST"], ["MOUNTAIN HERBS; MOUNTAIN FLORA; LOCAL FLORA AND FAUNA SPECIES", "SUSTAINABLE HARVESTING; REGENERATIVE AGRICULTURE", "HERBAL PRODUCTS; FOOD PRODUCTION; PHARMACEUTICALS"], ["EROSION SOIL; MOUNTAIN SEDIMENTS; FLOOD PLAIN SILT", "FLOOD PLAIN FERTILIZATION", "SOIL ENHANCEMENT; CROP CULTIVATION"], ["FLOOD PLAIN WILDLIFE; BIRD SPECIES; INSECT SPECIES; LOCAL LIVESTOCK; MOUNTAIN FAUNA", "ECOLOGICAL BALANCE; INDIGENOUS KNOWLEDGE", "BIO-DIVERSITY; ECOSYSTEM SERVICES"], ["MOUNTAIN MINERALS", "SUSTAINABLE MINING", "BUILDING MATERIALS; NUTRIENTS"], ["LOCAL CROP SEEDS", "PLANTING; REGENERATIVE AGRICULTURE", "SUSTAINABLE FOOD PRODUCTION"], ["SOLAR ENERGY", "SOLAR PANELS", "ELECTRICITY GENERATION; RENEWABLE ENERGY"], ["LOCAL WOOD RESOURCES", "SUSTAINABLE FORESTRY", "BUILDING MATERIALS;FUEL;ECOSYSTEM SERVICES"], ["REGIONAL AIR QUALITY; LOCAL WEATHER DATA", "ENVIRONMENTAL MONITORING", "POLICY MAKING;ENVIRONMENTAL MANAGEMENT"], ["AQUIFER WATER", "WATER EXTRACTION", "POTABLE WATER;IRRIGATION"], ["VILLAGE WASTEWATER; CHEETAH GENETIC MATERIAL", "WASTE WATER TREATMENT;GENETIC CONSERVATION", "TREATED WATER;BIOLOGICAL CONSERVATION"]]'
    # result=convertflow(test)
    # print(getelement(result))
    # print("\n")
    # print(getelement(result))
    #print("\n")
    #print(result.keys())
    #print("\n")
    #print(result.values())
    #print(color(categorize(result)))