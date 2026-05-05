import os

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.mcp import MCPServerHTTP
from crewai.project import CrewBase, agent, crew, task, tool
from dotenv import load_dotenv

from email_analyzer.tools.custom_tool import GenerateInvoicePDFTool

pdf_generate_upload=GenerateInvoicePDFTool()

load_dotenv()


@CrewBase
class EmailAnalyzer:
    """EmailAnalyzer crew"""

    agents: list[BaseAgent]
    tasks: list[Task]


    @agent
    def email_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config["email_analyzer"],  # type: ignore[index]
            verbose=True,
        )

    @agent
    def pdf_generator(self) -> Agent:
        return Agent(
            config=self.agents_config["pdf_generator"],  # type: ignore[index]
            verbose=True,
            tools=[pdf_generate_upload]
        )

    @agent
    def mcp_runner(self) -> Agent:
        return Agent(
            config=self.agents_config["mcp_runner"],  # type: ignore[index]
            verbose=True,
            mcps=[
                MCPServerHTTP(
                    url=os.getenv("MCP_URL"),
                    headers={"Authorization": os.getenv("UIPATH_BEARER_TOKEN")},
                    streamable=True,
                    cache_tools_list=True,
                ),
            ],
        )


    @task
    def email_analyzer_task(self) -> Task:
        return Task(
            config=self.tasks_config["email_analyzer_task"]  # type: ignore[index]
        )

    @task
    def pdf_generator_task(self) -> Task:
        return Task(
            config=self.tasks_config["pdf_generator_task"]  # type: ignore[index]
        )

    @task
    def mcp_runner_task(self) -> Task:
        return Task(
            config=self.tasks_config["mcp_runner_task"]  # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the EmailAnalyzer crew"""
        

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
