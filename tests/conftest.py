import pytest
import os
import logging
import json
from utinni import EmpireApiClient, EmpireModuleExecutionTimeout

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("[%(name)s] %(levelname)s - %(message)s"))

log = logging.getLogger("utinni")
log.setLevel(logging.DEBUG)
log.addHandler(handler)

def beautify_json(obj) -> str:
    return "\n" + json.dumps(obj, sort_keys=True, indent=4, separators=(",", ": "))

@pytest.mark.asyncio
@pytest.fixture
async def empire():
    empire = EmpireApiClient(
        host=os.environ.get("EMPIRE_HOST") or "localhost",
        port=os.environ.get("EMPIRE_PORT") or "1337"
    )

    await empire.login(
        os.environ.get("EMPIRE_USER") or "empireadmin",
        os.environ.get("EMPIRE_PASS") or "Password123!"
    )
    yield empire

@pytest.mark.asyncio
@pytest.fixture
async def agents(empire):
    agents = await empire.agents.get()
    yield agents
