from crewai import Crew, Process
from agents import news_writer, news_researcher
from tasks import write_task, research_task

crew = Crew(
    agents=[news_researcher, news_writer],
    tasks=[research_task,write_task],
    process=Process.sequential,
)

result = crew.kickoff(inputs={'topic':'New Age AI based and traditional digital marketing agencies in USA'})
print(result)