from langchain_openai import ChatOpenAI
from langchain.agents import tool, AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
import os
from environs import Env
from time import sleep              # Import sleep() function

from BirdBrain import Finch

# Get the API keys from .env - you will need to create a folder in FinchLLM
# that contains your API keys
env = Env()
env.read_env() # read .env file
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

finch = Finch()

@tool
def moveForwardDistance(distance: float, speed: float) -> str:
    """Moves Finch forward a distance in centimeters at a speed between 0 and 100."""
    finch.setMove('F',float(distance),speed)
    return 'Moved ' + str(distance) + ' cm at speed ' + str(speed) + '\n'

@tool
def moveBackwardDistance(distance: float, speed: float) -> str:
    """Moves Finch backward a distance in centimeters at a speed between 0 and 100."""
    finch.setMove('B',float(distance),speed)
    return 'Moved ' + str(distance) + ' cm back at speed ' + str(speed) + '\n'

@tool
def turnRightAngle(angle: float, speed: float) -> str:
    """Turns Finch to the right a given angle at a speed between 0 and 100."""
    finch.setTurn('R',float(angle),speed)
    return 'Turned right ' + str(angle) + ' degrees at speed ' + str(speed) + '\n'

@tool
def turnLeftAngle(angle: float, speed: float) -> str:
    """Turns Finch to the left a given angle at a speed between 0 and 100."""
    finch.setTurn('L',float(angle),speed)
    return 'Turned left ' + str(angle) + ' degrees at speed ' + str(speed) + '\n'

@tool
def moveForward() -> str:
    """Starts Finch moving forward."""
    finch.setMotors(10,10)
    return 'Finch is moving forward at speed 20\n'

@tool
def moveBackward() -> str:
    """Starts Finch moving backward."""
    finch.setMotors(-10,-10)
    return 'Finch is moving backward at speed 20\n'

@tool
def turnLeft() -> str:
    """Starts Finch turning left."""
    finch.setMotors(-10,10)
    return 'Finch is turning left\n'

@tool
def turnRight() -> str:
    """Starts Finch turning right."""
    finch.setMotors(10,-10)
    return 'Finch is turning right\n'

@tool
def stop() -> str:
    """Stops the Finch."""
    finch.setMotors(0,0)
    return 'Finch is stopped\n'

@tool
def playNote(note: int, beats: float) -> str:
    '''
    Makes the Finch play a note for certain number of beats.

    parameters:
        'note' is an integer for that represents a midi note number. Must be between 32 and 135.
        'beats' is a float between 0 and 16 that gives the number of beats the note should play. One beat lasts one second.

    returns:
        a string describing the note played
    '''
    finch.playNote(note,beats)
    sleep(beats+0.1)
    return 'Played note + ' + str(note) + ' for ' + str(beats) + ' beats\n'

@tool
def setBeak(red: int, green: int, blue: int) -> str:
    '''
    Sets the color of the light in the Finch's beak.

    parameters:
        'red' is an integer between 0 and 100 that represents the amount of red
        'green' is an integer between 0 and 100 that represents the amount of green
        'blue' is an integer between 0 and 100 that represents the amount of blue
        
    returns:
        a string describing the beak color
    '''
    finch.setBeak(red, green, blue)
    return 'Set beak to ' + str(red) + ' red, ' + str(green) + ' green, ' + str(blue) + ' blue\n'

@tool
def setTail(red: int, green: int, blue: int) -> str:
    '''
    Sets the color of the lights in the Finch's tail.

    parameters:
        'red' is an integer between 0 and 100 that represents the amount of red
        'green' is an integer between 0 and 100 that represents the amount of green
        'blue' is an integer between 0 and 100 that represents the amount of blue
        
    returns:
        a string describing the tail color
    '''
    finch.setTail('all',red, green, blue)
    return 'Set tail to ' + str(red) + ' red, ' + str(green) + ' green, ' + str(blue) + ' blue\n'

@tool
def setSingleTailLED(ledNum: int, red: int, green: int, blue: int) -> str:
    '''
    Sets the color of a single light in the Finch's tail.

    parameters:
        'ledNum' is an integer between 1 and 4 that identifies the light
        'red' is an integer between 0 and 100 that represents the amount of red
        'green' is an integer between 0 and 100 that represents the amount of green
        'blue' is an integer between 0 and 100 that represents the amount of blue
        
    returns:
        a string describing the nose color
    '''
    finch.setTail(ledNum,red, green, blue)
    return 'Set tail number ' + str(ledNum) + ' to ' + str(red) + ' red, ' + str(green) + ' green, ' + str(blue) + ' blue\n'


@tool
def angryBeep() -> str:
    """Shows that the Finch cannot do something by turning the lights red and making a low beep.
    parameters:
        none
        
    returns:
        a string stating that the Finch cannot do the task
    """
    finch.setBeak(100, 0, 0)
    finch.setTail('all',100, 0, 0)
    finch.playNote(50,1)
    sleep(1.1)
    finch.setBeak(0, 0, 0)
    finch.setTail('all',0, 0, 0)
    return 'The Finch cannot do that\n'

@tool
def wait(numSeconds: float) -> str:
    ''' Makes the Finch wait a given number of seconds'''
    sleep(numSeconds)
    return 'The Finch is waiting ' + str(numSeconds) + ' seconds\n'
@tool
def getLight() -> int:
    """Returns the amount of light measured by the Finch from 0-100"""
    return finch.getLight('L')

@tool
def getDistance() -> float:
    """Returns the distance between the Finch and the closest obstacle in front of it"""
    return finch.getDistance()

tools = [
    moveForwardDistance,
    moveBackwardDistance,
    turnRightAngle,
    turnLeftAngle,
    moveForward,
    moveBackward,
    turnLeft,
    turnRight,
    stop,
    playNote,
    setBeak,
    setTail,
    setSingleTailLED,
    angryBeep,
    wait,
    getLight,
    getDistance
]

systemPrompt = '''You are a small robot named Finch.'''

prompt = ChatPromptTemplate.from_messages([
    ("system", systemPrompt),
    ("placeholder", "{chat_history}"),
    ("human", "{input}"), 
    ("placeholder", "{agent_scratchpad}"),
])

llm = ChatOpenAI(model_name="gpt-3.5-turbo")
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    hang_tool_error=True,
    handle_parsing_errors="Check your output and make sure it conforms! Do not output an action and a final answer at the same time.",
    max_iterations = 15 # useful when agent is stuck in a loop
)
config = {"configurable": {"thread_id": "abc123"}}

#@traceable # Auto-trace this function
def sendMessageToAgent(user_input: str):
    agent_executor.invoke(
        {
            "input": user_input,
            "chat_history": []
        },
        config
    )

userPrompt = 'Give instructions to the Finch (q to end):\n'  
userInput = input(userPrompt)
while userInput != 'q':
    sendMessageToAgent(userInput)
    userInput = input(userPrompt)





