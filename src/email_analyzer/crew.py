import os

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.mcp import MCPServerHTTP
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv

from email_analyzer.tools.custom_tool import GenerateInvoicePDFTool

load_dotenv()

pdf_tool = GenerateInvoicePDFTool()


@CrewBase
class EmailAnalyzer:
    """EmailAnalyzer crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
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
            tools=[pdf_tool],
            mcps=[
                MCPServerHTTP(
                    url=os.getenv("MCP_URL"),
                    headers={"Authorization": os.getenv("UIPATH_BEARER_TOKEN")},
                    streamable=True,
                    cache_tools_list=True,
                ),
            ],
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
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

    @crew
    def crew(self) -> Crew:
        """Creates the EmailAnalyzer crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
