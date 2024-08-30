import os

from crewai import Agent
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq

from tools import tool

# call gemini model
from langchain_google_genai import ChatGoogleGenerativeAI
llm1 = ChatGoogleGenerativeAI(model = "gemini-1.5-flash",
                             verbose = True,
                             temperature = 0.5,
                             google_api_key = os.getenv("GOOGLE_API_KEY")
                             )

os.environ ["GROQ_API_KEY"] = "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"
llm = ChatGroq(temperature = 0.2,model_name="llama3-70b-8192")


news_researcher = Agent(
    role="Senior Researcher",
    goal="Uncover ground breaking technologies in {topic}",
    verbose=True,
    memory=True,
    backstory =("Driven by curiosity, you are at the forefront of"
    "innovation, eager to explore and share the knowledge that could"
    "change the world"),

    tools=[tool],
    llm=llm,
    allow_delegation=True,
    max_iter=10,
)

news_writer = Agent(
    role="Writer",
    goal="Narrate compelling tech stories about {topic}, from the following sites  - 'www.abc.com', 'www.xyz.com' ",
    verbose=True,
    memory=True,
    backstory=(
        "with a flair of simplifying complex topics you craft"
        "engaging narratives that captivate and educate, bringing new"
        "discoveries to light in an accessible manner"
    ),
    llm=llm,
    allow_delegation=False,
    max_iter=10,
)







