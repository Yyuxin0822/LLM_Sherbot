# pip install wikipedia==1.4.0 google-search-results==2.4.2 better-profanity==0.7.0 sqlalchemy==2.0.15 langchain==0.0.239 transformers  'transformers[torch]' tensort

# %% 
import os

os.environ["HUGGINGFACEHUB_API_TOKEN"] =  "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"
os.environ["OPENAI_API_KEY"] = "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"


# ## `SherBot` - An Environment Process Optimiation Bot
# 
# Hello, you are an environmental process optimization bot. You are great at coming up with impressive and creative environmental processes with information from my input and online resources. I will give you a description of an image.
# ##"Input"
# ##"Output"


# %%
# ### Step 1 - User: Type Environment Description
# We'll also need our image_description post:
envir_description = "This scene depicts an agricultural village in the mountains. There are a couple flood valleys with turbulent water.  To empower this village, there are some windfarms nearby. Cheetahs in the mountains need to be preserved. Food and potable water can be very valuable here."


# %% [markdown]
# ### Step 2 - Building the Input LLM
# ##### Building Input Prompt Template

# %%
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

# %% [markdown]
# ##### LangChain_Output_Parser for Input_Prompt

# %%
response_schemas = [
    ResponseSchema(name="Ecosystem", description="resources or flow belonging to ecosystem"),
    ResponseSchema(name="Energy System", description="resources or flow belonging to energy system"),
    ResponseSchema(name="Hydro System", description="resources or flow belonging to hydro system"),
]
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

# %%
# Let's start with the prompt template

from langchain import PromptTemplate
import numpy as np

format_instructions = output_parser.get_format_instructions()

# Our template for Jekyll will instruct it on how it should respond, and what variables (using the {text} syntax) it should use.
input_template = """
You are a environmental engineering specialist, you will extract and imagine potential resources in the environment description as keywords. The resources in the environment are primarily in three systems: ecosystem, energy system, and hydro system. Please try to imagine as much as possible, around 6–10 in each category.
Environment description:" {envir_description}"
Resources: 
{format_instructions}
"""
# We use the PromptTemplate class to create an instance of our template that will use the prompt from above and store variables we will need to input when we make the prompt.
input_prompt_template = PromptTemplate(
    input_variables=["envir_description"],
    template=input_template,
    partial_variables={"format_instructions": format_instructions}
)

# Let's create the prompt and print it out, this will be given to the LLM.
input_prompt = input_prompt_template.format(
    envir_description=envir_description
)
print(f"Input prompt:{input_prompt}")

# %% [markdown]
# ##### Building Input LLM

# %%
# # To interact with LLMs in LangChain we need the following modules loaded
from langchain.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain.llms import OpenAI

input_llm = OpenAI(model="text-davinci-003",temperature=0.6)
## We can also use a model from HuggingFaceHub if we wish to go open-source!

# model_id = "EleutherAI/gpt-neo-2.7B"
# tokenizer = AutoTokenizer.from_pretrained(model_id, cache_dir=DA.paths.datasets)
# model = AutoModelForCausalLM.from_pretrained(model_id, cache_dir=DA.paths.datasets)
# pipe = pipeline(
#     "text-generation", model=model, tokenizer=tokenizer, max_new_tokens=512, device_map='auto'
# )
# jekyll_llm = HuggingFacePipeline(pipeline=pipe)

# %% [markdown]
# ##### Building Input LLMChain

# %%

from langchain.chains import LLMChain
from better_profanity import profanity

input_chain = LLMChain(
    llm=input_llm,
    prompt=input_prompt_template,
    output_key="input_resources",
    verbose=False,
)  # Now that we've chained the LLM and prompt, the output of the formatted prompt will pass directly to the LLM.

# To run our chain we use the .run() command and input our variables as a dict
input_resources = input_chain.run(
    {"envir_description": envir_description}
)

# Before printing the answer, let's clean it up:
# cleaned_input_resources = profanity.censor(input_resources)
print(f"Input_resources:{input_resources}")

# %%
finalizedinput=output_parser.parse(input_resources)

# %% [markdown]
# ### Step 3 - Building the Input LLM 
# ##### Building the second chain for output generater

# %%
# -----------------------------------
# -----------------------------------
# 1 We will build the prompt template
# Our template for Hyde will take Jekyll's comment and do some sentiment analysis.
output_template = """
You are a environmental engineering specialist, based on the input resources, you will come up with output resources to optimize the environmental process to achive net zero energy, net zero carbon, and net positive water systems.
Input resources: {input_resources}
Output:
{format_instructions}
"""
# We use the PromptTemplate class to create an instance of our template that will use the prompt from above and store variables we will need to input when we make the prompt.
output_prompt_template = PromptTemplate(
    input_variables=["input_resources"],
    template=output_template,
    partial_variables={"format_instructions": format_instructions}
)
# -----------------------------------
# -----------------------------------
# 2 We connect an LLM for Hyde, (we could use a slightly more advanced model 'text-davinci-003 since we have some more logic in this prompt).

# hyde_llm=jekyll_llm
# Uncomment the line below if you were to use OpenAI instead
output_llm = OpenAI(model="text-davinci-003",temperature=1.0)

# -----------------------------------
# -----------------------------------
# 3 We build the chain for Hyde
output_chain = LLMChain(
    llm=output_llm, prompt=output_prompt_template, verbose=False
)  # Now that we've chained the LLM and prompt, the output of the formatted prompt will pass directly to the LLM.
# -----------------------------------
# -----------------------------------
# 4 Let's run the chain with what Jekyll last said
# To run our chain we use the .run() command and input our variables as a dict
output_resources = output_chain.run({"input_resources": input_resources})
# Let's see what hyde said...
print(f"Output_resources: {output_resources}")

# %%
finalizedoutput=output_parser.parse(output_resources)

# %% [markdown]
# ### Step X - Building another LLM 
# ##### Building the X chain for output generater

# %%
# -----------------------------------
# -----------------------------------
# 1 We will build the prompt template
# Our template for Hyde will take Jekyll's comment and do some sentiment analysis.
flow_template = """
You are a environmental engineering specialist, please match keywords of various system in input resources with keywords in output resources using symbol"→", the bridging relationship can be one-to-many.
Input resources: {input_resources}
Output resources: {output_resources}
Flow:

"""
# We use the PromptTemplate class to create an instance of our template that will use the prompt from above and store variables we will need to input when we make the prompt.
flow_prompt_template = PromptTemplate(
    input_variables=["input_resources","output_resources"],
    template=flow_template,
)
# -----------------------------------
# -----------------------------------
# 2 We connect an LLM for Hyde, (we could use a slightly more advanced model 'text-davinci-003 since we have some more logic in this prompt).

# Uncomment the line below if you were to use OpenAI instead
flow_llm = OpenAI(model="text-davinci-003",temperature=1.5)

# -----------------------------------
# -----------------------------------
# 3 We build the chain for Hyde
flow_chain = LLMChain(
    llm=flow_llm,output_key="Flow",prompt=flow_prompt_template, verbose=False
)  # Now that we've chained the LLM and prompt, the output of the formatted prompt will pass directly to the LLM.
# -----------------------------------
# -----------------------------------
# 4 Let's run the chain with what Jekyll last said
# To run our chain we use the .run() command and input our variables as a dict
flow = flow_chain.run({"input_resources": input_resources, "output_resources": output_resources})
# Let's see what hyde said...
print(f"Flow_process: {flow}")

# %% [markdown]
# ### Step 4 - Creating `InputOutput`
# #### Building our first Sequential Chain (Not so good yet)

# %%
from langchain.chains import SequentialChain

# The SequentialChain class takes in the chains we are linking together, as well as the input variables that will be added to the chain. These input variables can be used at any point in the chain, not just the start.
inputoutput_chain = SequentialChain(
    chains=[input_chain, output_chain],
    input_variables=["envir_description"],
    verbose=False,
)

# We can now run the chain with our randomized sentiment, and the social post!
inputoutput_chain.run({"envir_description": envir_description})

# %% [markdown]
# ### Step 5 - Generate Environment Image

# %%
import openai

response = openai.Image.create(
  prompt=f"{envir_description}",
  n=1,
  size="1024x1024"
)
image_url = response['data'][0]['url']


# %%
print({f"Environment_description: {envir_description}"})

print(f"Environment_description:{image_url}")

print(f'Input:/n')
print(f'Ecosystem: {finalizedinput["Ecosystem"]}/n')
print(f'EnergySystem: {finalizedinput["Energy System"]}/n')
print(f'HydroSystem: {finalizedinput["Hydro System"]}/n')

print(f'Output:/n')
print(f'Ecosystem: {finalizedoutput["Ecosystem"]}/n')
print(f'EnergySystem: {finalizedoutput["Energy System"]}/n')
print(f'HydroSystem: {finalizedoutput["Hydro System"]}/n')

print(f"Flow_process: {flow}")
