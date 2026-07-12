from crewai import Crew

from agents.email_agent import email_agent
from agents.inventory_agent import inventory_agent
from agents.manager_agent import manager_agent


from tasks.email_task import email_task
from tasks.inventory_task import inventory_task
from tasks.manager_task import manager_task


supply_chain_crew = Crew(
    agents=[
        email_agent,
        inventory_agent,
        manager_agent


    ],
    tasks=[
        email_task,
        inventory_task,
        manager_task

    ],
    verbose=True
)