from typing import Annotated

from fastapi import Depends

from src.repositories import NNModelRepository
from src.services import NNModelService


def _get_nn_model_repo() -> NNModelRepository:
    return NNModelRepository()


def get_nn_model_service(
        nn_model_repo: Annotated[
            NNModelRepository, Depends(_get_nn_model_repo)
        ]
) -> NNModelService:
    return NNModelService(nn_model_repo)
