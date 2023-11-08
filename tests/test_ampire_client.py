"""
These test assume you have at least 1 agent connected to empire!
"""

import pytest
from conftest import beautify_json


@pytest.mark.asyncio
async def test_listeners(empire):
    r = await empire.listeners.create(name="Utinni-Test", additional={"Port": 8989})
    r = await empire.listeners.get("Utinni-Test")
    assert "error" not in r

    await empire.listeners.kill("Utinni-Test")


@pytest.mark.asyncio
async def test_agents(empire):
    agents = await empire.agents.get()
    assert len(agents) > 0

    agent = await empire.agents.get(agents[0].name)
    assert agent


@pytest.mark.asyncio
async def test_modules(empire, agents):
    agent = agents[0]

    modules = await empire.modules.search("get_domain_sid")
    assert len(modules) > 0

    module = await empire.modules.get("powershell/management/get_domain_sid")
    assert module

    r = await empire.modules.execute(module, agent)
    print(beautify_json(r))
    assert r["results"] != None and not r["results"].startswith("Job started")


@pytest.mark.asyncio
async def test_agent_results(empire, agents):
    agent = agents[0]

    r = await empire.agents.results(agent)
    print(beautify_json(r))


@pytest.mark.asyncio
async def test_shell(empire, agents):
    agent = agents[0]

    r = await empire.agents.shell("tasklist", agent)
    print(beautify_json(r))


@pytest.mark.asyncio
async def test_events(empire, agents):
    agent = agents[0]

    r = await empire.events.all()
    print(beautify_json(r))

    r = await empire.events.agent(agent)
    print(beautify_json(r))
