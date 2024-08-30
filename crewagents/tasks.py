from crewai import Task
from tools import tool
from agents import news_researcher, news_writer

research_task = Task(
    description=(
        "Identify the next big trend in {topic}."
        "Focus on identifying pros and cons and the overall narrative."
        "Your final report should clearly articulate the key points"
        "Its market opportunities and potential risks"
    ),
    expected_output="A comprehensive 3 paragraph long report on the {topic}",
    tools=[tool],
    agent=news_researcher
)

write_task = Task(
    description=(
                 "Compose an insightful article on {topic}."
                 "Focus on latest trends and how is it important for industry."
                 "This article should be engaging, easy to understand and positive"
    ),
    expected_output="A detailed long form report on {topic} advancements formatted as markdown",
    agent=news_writer,
    async_execution=False,
    output_file='file_magenices.md'

)