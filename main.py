from DTO.SimulationRequestDTO import SimulationRequest
from DTO.SimulationResponseDTO import SimulationResponse
from fastapi import FastAPI, HTTPException
from Mappers.SimulationResponseMapper import SimulationResponseMapper
from Mappers.SimulationRequestMapper import SimulationRequestMapper

app = FastAPI(
    title="qpy API",
    description="API to expose QPy funcionalities",
    version="0.1.0",
)

@app.post("/simulate")
async def simulate(request: SimulationRequest) -> SimulationResponse:
    """
    Recebe uma configuração de rede e executa a simulação da qpy.
    """

    try:
        request_mapper = SimulationRequestMapper(request)

        env = request_mapper.get_environemnt()

        results = env.simulate(float(request.networkParameters.simulationTime), float(request.networkParameters.warmupTime))

        response_mapper = SimulationResponseMapper(results)

        return response_mapper.get_response_object()

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
