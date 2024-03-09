import re
from typing import NamedTuple, TextIO

import aiohttp as aiohttp

from src.exceptions import InvalidReqsFileFormatError, RepeatedReqError, NonExistentReqError


class ValidatedReq(NamedTuple):
    package_name: str
    version: str


class ReqsFileValidator:

    def __init__(self, reqs_file: TextIO):
        self._reqs_file = reqs_file

    async def validate(self) -> set[ValidatedReq]:
        reqs = self._validate_reqs_file()
        await self._validate_reqs_existence_remote(reqs)
        return reqs

    def _validate_reqs_file(self) -> set[ValidatedReq]:
        validated_reqs = set()
        package_names = set()
        for index, line in enumerate(self._reqs_file.readlines()):
            if line.startswith('#') or line == '\n':
                continue

            # empty string, comment or string of the form 'package==6.6.6'
            regex = r'^$|^#.*|^[^=]+==\d+(\.\d+)*$'

            if re.match(regex, line) is None:
                raise InvalidReqsFileFormatError(index + 1)

            package_name, version = line.split('==')
            if package_name in package_names:
                raise RepeatedReqError(package_name)

            validated_reqs.add(ValidatedReq(package_name, version))
            package_names.add(package_name)

        return validated_reqs

    async def _validate_reqs_existence_remote(self, reqs: set[ValidatedReq]) -> None:
        async with aiohttp.ClientSession() as session:
            for req in reqs:
                # Pypi doesn't handle many requests asynchronously,
                # so it will be more efficient to send requests sequentially
                await self._validate_one_req_existence_remote(
                    req,
                    session
                )

    @staticmethod
    async def _validate_one_req_existence_remote(
            req: ValidatedReq,
            session: aiohttp.ClientSession
    ) -> None:
        package_name, version = req
        url = f'https://pypi.org/project/{package_name}/{version}/'
        async with session.get(url) as response:
            if response.status != 200:
                raise NonExistentReqError(package_name, version)


class ReqsInstaller:

    def install(self) -> None:
        pass
