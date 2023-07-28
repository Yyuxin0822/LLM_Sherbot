#Step 1 - Generate Environment Image
import os

from langchain.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

os.environ["HUGGINGFACEHUB_API_TOKEN"] =  "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"
os.environ["OPENAI_API_KEY"] = "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"

import openai

def getcanvas(envir_description):
    response = openai.Image.create(
        prompt=f"{envir_description}",
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']
    return image_url

#Step 2 - Building the Input LLM
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

response_schemas = [
    ResponseSchema(name="Ecosystem", description="resources or flow belonging to ecosystem"),
    ResponseSchema(name="Energy System", description="resources or flow belonging to energy system"),
    ResponseSchema(name="Hydro System", description="resources or flow belonging to hydro system"),
]
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()

######################################################
######################################################
# Template for generating input resources and what variables (using the {text} syntax) it should use.
input_llm = OpenAI(model="text-davinci-003",temperature=0.6)

def getinput(envir_description):

    input_template = """
    You are a environmental engineering specialist, you will extract and imagine potential resources in the environment description as keywords. The resources in the environment are primarily in three systems: ecosystem, energy system, and hydro system. Please try to imagine as much as possible, around 6–10 in each category.
    Environment description:" {envir_description}"
    Input resources: 

    {format_instructions}
    """

    input_prompt_template = PromptTemplate(
        input_variables=["envir_description"],
        template=input_template,
        partial_variables={"format_instructions": format_instructions}
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


    #finalizedinput=output_parser.parse(input_resources)


######################################################
######################################################


output_llm = OpenAI(model="text-davinci-003",temperature=1.0)

def getoutput(envir_description):
    input_resources=getinput(envir_description)
    output_template = """
    You are a environmental engineering specialist, based on the input resources, you will come up with output resources to optimize the environmental process to achive net zero energy, net zero carbon, and net positive water systems.
    Input resources: {input_resources}
    Output:

    {format_instructions}
    """

    output_prompt_template = PromptTemplate(
        input_variables=["input_resources"],
        template=output_template,
        partial_variables={"format_instructions": format_instructions}
    )

    output_chain = LLMChain(
        llm=output_llm, prompt=output_prompt_template, verbose=False
    )  
    output_resources = output_chain.run({"input_resources": input_resources})
    return output_resources
    #finalizedoutput=output_parser.parse(output_resources)

    
######################################################
######################################################

if __name__=="__main__":
    pass
    #envir_description="This scene depicts an agricultural village in the mountains. There are a couple flood valleys with turbulent water.  To empower this village, there are some windfarms nearby. Cheetahs in the mountains need to be preserved. Food and potable water can be very valuable here."
    