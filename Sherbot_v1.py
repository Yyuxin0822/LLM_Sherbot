
import os
import json
import re

from langchain.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

os.environ["HUGGINGFACEHUB_API_TOKEN"] =  "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"
os.environ["OPENAI_API_KEY"] = "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"


######################################################
######################################################
#Step 1 - Generate Environment Image
import openai

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

#Step 2 - Building the Input LLM
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

######################################################
######################################################
# Template for generating input resources and what variables (using the {text} syntax) it should use.
input_llm = ChatOpenAI(model="gpt-4",temperature=1)

def getinput(envir_description):

    input_template = """
    You are a environmental engineering specialist, you will extract and imagine potential resources in the environment description as keywords. The resources in the environment include potential organisms, chemicals, materials; and they come from various systems, such as hydro, energy, and ecosystem. Please try to imagine as much as possonible, and provide me around 40 in total.

    Environment description: "This scene depicts an agricultural village in the mountains. There are a couple flood valleys with turbulent water.  To empower this village, there are some windfarms nearby. Cheetahs in the mountains need to be preserved. Food and potable water can be very valuable here."
    Input resources: cheetah, fresh water, biomass, groundwater, wild herbs, flora, potable water, irrigation water
    Environment description:" {envir_description}"
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
    )  # Now that we've chained the LLM and prompt, the output of the formatted prompt will pass directly to the LLM.


    input_resources = input_chain.run(
        {"envir_description": envir_description}
    )# To run our chain we use the .run() command and input our variables as a dict

    return input_resources


######################################################
######################################################

output_llm = ChatOpenAI(model="gpt-4",temperature=1.0)

def getoutput(envir_description):
    input_resources=getinput(envir_description)
    output_template = """
        You are a environmental engineering specialist, given the input resources, you will come up with output resources to optimize the environmental process to achive net zero energy, net zero carbon, and net positive water systems. Please come up with two to three output for each input.
        Create a dictionary in this format: - input:[output1;output2],

        Input resources: waste water, organic waste, wind
        Output resources: - waste water:[fresh water ; nutrients], - organic waste:[biofuel; biogas], - wind:[electricity; humidity]
        Input resources: {input_resources}
        Output resources:


    """

    output_prompt_template = PromptTemplate(
        input_variables=["input_resources"],
        template=output_template,
    )

    output_chain = LLMChain(
        llm=output_llm, prompt=output_prompt_template, verbose=False
    )  
    output_resources = output_chain.run({"input_resources": input_resources})
    return output_resources


######################################################
######################################################

def clean(input_string):
    "clean a string to make it start with letter and end with letter, and all the cases are upper"
    cleaned_string = re.sub(r'^[^a-zA-Z]+|[^a-zA-Z]+$', '', input_string)
    return cleaned_string.upper()

def has_letters(string):
    return any(char.isalpha() for char in string)

def flowdict(result):
    finalizedoutput=result.replace("\n","").replace("-","").split(",")
    dict={}
    for item in finalizedoutput:
        key=clean(item.partition(":")[0])
        value=clean(item.partition(":")[-1])
        parsed=value.split(";")
        parsed_value=[]
        for item in parsed:
            if has_letters(item):
                parsed_value.append(clean(item))
        dict[key]=parsed_value
    
    # Serializing json
    json_object = json.dumps(dict, indent=4)
    
    # Writing to sample.json
    with open("static/flow.json", "w") as outfile:
        outfile.write(json_object)
    
    return dict

def getoutputlist(dict):
    dict_list=[]
    for key in dict.keys():
        for v in dict[key]:
            dict_list.append(v)

    return dict_list

def getinputlist(dict):
    dict_list=[]
    for key in dict.keys():
        dict_list.append(key)

    return dict_list

######################################################
######################################################

def getstring(dict):
    dict_list=[]
    for key in dict.keys():
        dict_list.append(key)
        for v in dict[key]:
            dict_list.append(v)

    full_string=""
    for i in dict_list:
        full_string+=i
        full_string+=","

    return full_string

def getlist(dict):
    dict_list=[]
    for key in dict.keys():
        dict_list.append(key)
        for v in dict[key]:
            dict_list.append(v)

    return dict_list



# classify_llm = OpenAI(model="text-davinci-003",temperature=1)

# def classify(dict):
#     full_string=getstring(dict)
#     classify_template = """
#         Please take my list, classify all my list items into three categories: energy, hydro, and ecosystem, and return a dictionary.

#         full_string: Cheetah, wildlife corridors, wind speed assessment, water
#         classified dictionary: Cheetah:ecosystem, wildlife corridors:ecosystem, wind speed assessment:energy, water:hydro
#         full_string: {full_string}
#         classified: 

#     """

#     classify_prompt_template = PromptTemplate(
#         input_variables=["full_string"],
#         template=classify_template,
#     )

#     classify_chain = LLMChain(
#         llm=classify_llm , prompt=classify_prompt_template, verbose=False
#     ) 
        
#     classified = classify_chain.run({"full_string":full_string})

#     system=classified.split(',')

#     dict_system={}
#     for item in system:
#         key=item.partition(":")[0].strip("[]").strip("\n").strip(" ").upper()
#         value=item.partition(":")[-1].strip("[]").strip("''")
#         dict_system[key]=value

#     return dict_system


zero_shot_pipeline = pipeline(
    task="zero-shot-classification",
    model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli",
    model_kwargs={"cache_dir": "__pycache__/dataset"},
    tokenizer = AutoTokenizer.from_pretrained("MoritzLaurer/mDeBERTa-v3-base-mnli-xnli", use_fast=False)
)

def categorize(dict):
    """
    This helper function defines the categories (labels) which the model must use to label articles.
    Note that our model was NOT fine-tuned to use these specific labels,
    but it "knows" what the labels mean from its more general training.

    This function then prints out the predicted labels alongside their confidence scores.
    """
    categorydict={}
    for item in getlist(dict):
        results = zero_shot_pipeline(
            item,candidate_labels=["hydro","energy","ecosystem",],)
       # del results["sequence"]
        if item not in categorydict.keys():
            categorydict[item]=results['labels'][0]

    return categorydict


def color(dict):
    #ecosystem-green:#39b54a, energy-yellow:#ffc60b, hydro-blue: #00aeef
    colordict={}
    for item in dict:
        if dict[item]=='ecosystem':
            colordict[item]="#39b54a"
        elif dict[item]=='energy':
            colordict[item]="#ffc60b"
        elif dict[item]=='hydro':
            colordict[item]="#00aeef"
        else:
            colordict[item]="white"
   
    # Serializing json
    json_object = json.dumps(colordict, indent=4)
    
    # Writing to sample.json
    with open("static/sample.json", "w") as outfile:
        outfile.write(json_object)

    return colordict
    
######################################################
######################################################
if __name__=="__main__":
    pass
    #env="This scene depicts an agricultural village in the mountains. There are a couple flood valleys with turbulent water. To empower this village, there are some windfarms nearby. Cheetahs in the mountains need to be preserved. Food and potable water can be very valuable here."
    #env="This scene depicts a coastal environment."
    #print getoutput(envir_description)
    #result=flowdict(getoutput(env))
    #print(result)
    #print("\n")
    #print(result.keys())
    #print("\n")
    #print(result.values())
    #print(color(categorize(result)))