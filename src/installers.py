import abc
from io import FileIO
from typing import NamedTuple


class _ValidatedReq(NamedTuple):
    package: str
    version: str


class ReqsInstaller(abc.ABC):

    def __init__(
            self,
            reqs_file: FileIO,
            destination: str,
    ):
        self._reqs_file = reqs_file
        self._destination = destination

    @abc.abstractmethod
    def install(self):
        pass


class SimpleReqsInstaller(ReqsInstaller):

    def install(self):
        validated_reqs = self._validate()
        self._install(validated_reqs)

    def _validate(self) -> set[_ValidatedReq]:
        reqs = self._validate_reqs_file()
        self._validate_reqs_existence_remote(reqs)
        self._remove_locally_existing_req(reqs)
        return reqs

    def _validate_reqs_file(self) -> set[_ValidatedReq]:
        pass

    @staticmethod
    def _validate_reqs_existence_remote(reqs: set[_ValidatedReq]):
        pass

    def _remove_locally_existing_req(self, reqs: set[_ValidatedReq]):
        pass

    def _install(self, requirements: set[_ValidatedReq]):
        pass
