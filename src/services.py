from src.api_schemas import NNModelCreateRequest, NNModelCreateResponse
from src.models import NNModel, NNModelStatus
from src.repositories import NNModelRepository


class NNModelService:

    def __init__(self, nn_model_repo: NNModelRepository):
        self._nn_model_repo = nn_model_repo

    def create(
            self,
            nn_model_create: NNModelCreateRequest
    ) -> NNModelCreateResponse:
        nn_model = NNModel(
            name=nn_model_create.name,
            description=nn_model_create.description,
            status=NNModelStatus.CREATED,
            requirements=[]
        )
        self._nn_model_repo.create(nn_model)

        return NNModelCreateResponse(
            id=nn_model.id,
            name=nn_model.name,
            description=nn_model.description,
            created_at=nn_model.created_at
        )
