# LLM_Sherbot

## Sherbot is an LLM-based web application for generative flow diagrams. As an educative tool for environmental engineering, it generates flow / circular economy diagram and allows freedom for users to doodle and modify.


### Activate virtual environment and python dependencies
### cd "static", install node modules in package-lock, this project uses leader-line and plain-draggable package by anseki
### The webapp is powered by gpt-4 and dalle2, you can adapt the code to the model you selected accordingly

### Run python app.py, the webpage will open

## "GENERATE FLOW" is the button to send new TEXT-TO-FLOW DIAGRAM request.
### First, Input your environmental description here, click "GENERATE FLOW"
![Alt text](URL or file path)

### The web will generate a compacted view of input-to-output flow. 
![Alt text](URL or file path)
### You can toggle image on and off by "Explore > Show Creative Image" and "Explore > Hide Creative Image" 



## "ASK SHERBOT" is the button to send new request based on the element selections.
### Try, right-click to select one element, such as "OXYGEN"
### Then, click "ASK SHERBOT" 


### Now, go back to by clicking "Explore > Lookup Simple Flow"


### Try, right-click to select one flow, such as  right-click "OXYGEN" --> select "Select Output Flow"--> "FUEL SOURCE"
### Then, click "ASK SHERBOT"
### The tool will expand on the internal process for generating flow


### Now, go back to by clicking "Explore > Lookup Simple Flow"
### Try, right-click on multiple element and multiple flow, like below
### Then, click "ASK SHERBOT"
### It will generate a complex flow view, delinating multiple processes for going from input to output


### Navigate to "Explore > Lookup Element Co-optimization"
### It will generate a networked flow view, delinating how all the elements can be connected


### Now, go back to by clicking "Explore > Lookup Simple Flow"
### Select all element and flow
### Then, click "ASK SHERBOT"


## This tool contains many editing features under "Explore"
### Here are some examples