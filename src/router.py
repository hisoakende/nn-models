from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi import status

from src.api_schemas import NNModelCreateRequest, NNModelCreateResponse
from src.dependencies import get_nn_model_service
from src.services import NNModelService

router = APIRouter(prefix='/api/models')


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED
)
async def create_nn_model(
        nn_model_create: NNModelCreateRequest,
        nn_model_service: Annotated[
            NNModelService, Depends(get_nn_model_service)
        ]
) -> NNModelCreateResponse:
    return nn_model_service.create(nn_model_create)
