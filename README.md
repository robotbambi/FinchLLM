This shows a simple LLM agent for the Finch robot. You will need a few things to get it to work. 

First, you are going to need a Finch robot, and you will need to be running the BlueBird Connector software and be connected to your Finch. If any of that seems like a mystery, head to www.birdbraintechnologies.com.

Second, you will need API keys for LangChain and OpenAI. The code assumes that these live in a .env file in the FinchLLM folder.

You will need to pip install a lot of things, and I really recommend using venv for this (if you want to run the speech recognition, that is mandatory, not optional). You need at least the following, but this list may not be exhaustive:
langchain
langchain_openai
environs
setuptools (speech recognition) - this has to be installed in venv
SpeechRecognition (speech recognition)
PyAudio (speech recognition)
