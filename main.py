from DTO import SimulationRequest
from fastapi import FastAPI, HTTPException
from Mappers.SimulationRequestMapper import SimulationRequestMapper

app = FastAPI(
    title="qpy API",
    description="API to expose QPy funcionalities",
    version="0.1.0",
)

@app.post("/simulate", response_model=None)
async def simulate(request) -> dict:
    """
    Recebe uma configuração de rede e executa a simulação da qpy.
    """

    try:
        smr = SimulationRequestMapper(request)

        env = smr.getEnvironment()

        results = env.simulate(float(request.networkParameters.simulationTime), float(request.networkParameters.warmupTime))

        return {"Status": "Ok"}

    except Exception as e:
        return {"Status": "error"}
