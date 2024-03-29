import abc
from enum import Enum


class ErrorCode(Enum):
    INVALID_REQS_FILE_FORMAT = 1
    REPEATED_REQ = 2
    NON_EXISTENT_REQ = 3
    IMPOSSIBLE_INSTALL_REQS = 4


class _Exception(Exception, abc.ABC):

    @property
    @abc.abstractmethod
    def code(self) -> ErrorCode:
        pass


class InputError(_Exception, abc.ABC):
    pass


class InternalError(_Exception, abc.ABC):
    pass


class InvalidReqFileError(InputError, abc.ABC):
    pass


class ReqsInstallationError(InternalError, abc.ABC):
    pass


class InvalidReqsFileFormatError(InvalidReqFileError):
    """Invalid format of requirements in the requirements file error."""

    code = ErrorCode.INVALID_REQS_FILE_FORMAT

    def __init__(self, line_number: int):
        self._line_number = line_number

    def __str__(self) -> str:
        return f"""The requirements file contains an invalid
                   line under the {self._line_number} number"""


class RepeatedReqError(InvalidReqFileError):
    """Repeated requirement in the requirements file error."""

    code = ErrorCode.REPEATED_REQ

    def __init__(self, package_name: str):
        self._package_name = package_name

    def __str__(self) -> str:
        return f"""The requirements file contains an repeated
                   requirement with the "{self._package_name}" name"""


class NonExistentReqError(InvalidReqFileError):
    """Non-existent requirement in the requirements file error."""

    code = ErrorCode.NON_EXISTENT_REQ

    def __init__(self, package_name: str, version: str):
        self._package_name = package_name
        self._version = version

    def __str__(self) -> str:
        return f"""The requirements file contains
                   a non-existent requirement
                   with the "{self._package_name}" name
                   and "{self._version}" version"""


class ImpossibleInstallReqsError(ReqsInstallationError):
    """Requirements cannot be installed for internal reasons error."""

    code = ErrorCode.IMPOSSIBLE_INSTALL_REQS

    def __str__(self) -> str:
        return """Requirements cannot be established
                  for technical reasons. As soon
                  as the problem is resolved,
                  the requirements will be installed"""
