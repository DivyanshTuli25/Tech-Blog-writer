import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

# Set your API keys
os.environ['SERPER_API_KEY'] = os.getenv('SERPER_API_KEY')
import os
import re
from datetime import datetime

import requests
from crewai import Agent, Crew, Process,Task
from crewai_tools import tool
from langchain.agents import load_tools
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

def format_response (response: str) -> str:
    entries = re.split(r" (?<=]), (?=\[)", response)
    return [entry.strip("[]") for entry in entries]

# os.environ ["GROQ_API_KEY"] = "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"

# llm = ChatGroq(temperature = 0.2,model_name="llama3-70b-8192")
import os

from crewai import Agent
from dotenv import load_dotenv
load_dotenv()

from tools import tool

# call gemini model
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model = "gemini-1.5-flash",
                             verbose = True,
                             temperature = 0.5,
                             google_api_key = os.getenv("GOOGLE_API_KEY")
                             )

# Creating tools
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()
#content_tool = ContentCreationTool()

# Creating agents
market_researcher = Agent(
    role='Market Researcher',
    goal='Gather comprehensive data on the e-rickshaw market in India and potential markets around the world.'
          'Gather data about target buyers of battery rickshaws, sales data across different states in the country'
          'also perform a pricing comparison and specifications of different companies inlcuding - range,maxspeed battery type, charging time etc.',
    verbose=True,
    memory=True,
    backstory="You are an expert in market research, skilled at identifying market trends and customer demographics."
               "You have a specialisation in ELectric Vehicles primarily E-Rickshaws or battery rickshaws",
    tools=[search_tool, scrape_tool],
    llm = llm,
    allow_delegation=True,
    max_iter = 10,
)

lead_generator = Agent(
    role='Lead Generator',
    goal='Identify and compile a list of potential leads for bulk e-rickshaw sales in India'
    "Find dealers and prospective dealers of E-Rickshaws"
    "Also include government leads and institutional buyers of E-Rickshaws or battery rickshaws",
    verbose=True,
    memory=True,
    backstory="You are proficient in generating B2B and bulk leads and finding potential customers using research data."
    "You can identify very carefully and find B2B leads for bulk orders of Battery Rickshaws",
    tools=[search_tool],
    llm = llm,
    allow_delegation=True,
    max_iter = 10
)


# Creating tasks
market_research_task = Task(
    description="Research the e-rickshaw market in India, focusing on customer demographics, competitors, and market trends."
                'Gather comprehensive data on the e-rickshaw market in India and potential markets around the world.'
                'Gather data about target buyers of battery rickshaws, sales data across different states in the country'
                'also perform a pricing comparison and specifications of different companies inlcuding - range,maxspeed battery type, charging time etc.'
    ,
    expected_output='A detailed report on market research findings and format as a markdown.',
    tools=[search_tool, scrape_tool],
    agent=market_researcher,
    output_file = 'report.md',
    max_iter = 10

)

lead_generation_task = Task(
    description="Identify and compile a list of potential leads based on the market research."
                'Identify and compile a list of potential leads for bulk e-rickshaw sales in India'
                "Find dealers and prospective dealers of E-Rickshaws along with their contact details"
                "Also include government leads and institutional buyers of E-Rickshaws or battery rickshaws along with their contact details"
    ,
    expected_output='A list of potential leads with contact information formatted as markdown.',
    tools=[search_tool],
    agent=lead_generator,
    async_execution=False,
    output_file='leads.md',
    max_iter=10,
)


# Forming the crew
crew = Crew(
    agents=[market_researcher, lead_generator],
    tasks=[market_research_task, lead_generation_task],
    process=Process.sequential  # Sequential task execution
)

# Kick off the crew with the input topic
result = crew.kickoff(inputs={'topic': 'e-rickshaw market in India'})
print(result)