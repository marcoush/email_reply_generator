\# Prerequisites

Install Docker Desktop with WSL2 backend on Windows.

---



\# Steps



\## Get emails

First, get the emails in the csv file from the imap:



Open extract\_past\_mails\_from\_imap.py, adjust parameters and run script. Examples:

IMAP\_SERVER = "server.net"

IMAP\_PORT = 993

USERNAME = "mymail@mail.com"

PASSWORD = "abc"

KEYWORDS = \["application", "invitation", "Application", "Invitation"]



Afterwards, run the script format\_past\_mails.py.



☑️ The past\_emails.csv file is now prepared and lies in the /gradio\_app/ folder.



---



\## Build application 



Now, let's build the application: 



Make sure you have Docker installed, then open CMD and navigate to the root folder. Example:

cd "E:\\0\_git\_repos\\application\_email\_style\_based\_ai\_answerer"



Adjust the parameters in the app.py if you want. I chose:

&nbsp;       #"model": "mistral",  # Original choice, but too heavy on CPU for local usage

&nbsp;       "model": "llama3.2:3b",  # Smaller, GPU-friendly alternative

&nbsp;       "prompt": prompt,

&nbsp;       "max\_tokens": 250,       # Maximum number of tokens in the generated reply

&nbsp;       "temperature": 0.7,      # Controls creativity/randomness of the output (0 = deterministic)

&nbsp;       "stream": False          # Whether to stream partial outputs (False = wait for full reply)



Before we can start the app, we need to load the AI Model (llama3.2:3b, around 2GB big and enough for this use case):

docker-compose up -d ollama

docker exec -it ollama /bin/bash

ollama pull llama3.2:3b

ollama list 

-> should show it.



Afterwards, run the code:

docker-compose up --build -d gradio\_app

(don't run docker-compose up --build -d without the gradio\_app, otherwise you'll recreate the ollama container and lose the pulled ai model in the container)



☑️ Frontend app now started, open in your browser on http://localhost:7860/.



Start generating 🚀.





\# PS

Sadly, I didn't manage to run the model on the GPU, therefore the CPU is under heavy bombardement for this task and might shoot up to 80%. But it works in around 40 seconds still and not too bad.







