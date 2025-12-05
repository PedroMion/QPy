import os
from DTO.SimulationRequestDTO import SimulationRequest
from DTO.SimulationResponseDTO import SimulationResponse
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from Mappers.SimulationResponseMapper import SimulationResponseMapper
from Mappers.SimulationRequestMapper import SimulationRequestMapper
from middlewares.api_key import api_key_middleware

app = FastAPI(
    title="qpy API",
    description="API to expose QPy funcionalities",
    version="0.1.0",
)

allowed_origins = os.getenv("ALLOWED_ORIGINS", "")
origins = [o.strip() for o in allowed_origins.split(",") if o.strip()]

app.middleware("http")(api_key_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

        response_mapper = SimulationResponseMapper(results, request_mapper.get_ids_map())

        return response_mapper.get_response_object()

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
