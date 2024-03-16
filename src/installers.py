import asyncio
import os
import re
import shutil
import subprocess
import sys
from typing import Iterable, NamedTuple, TextIO

import aiohttp as aiohttp

from src.exceptions import (
    ImpossibleInstallReqsError, InvalidReqsFileFormatError,
    NonExistentReqError, RepeatedReqError
)


class ValidatedReq(NamedTuple):
    package_name: str
    version: str


class _InstallationReadyReq(NamedTuple):
    package_name: str
    version: str
    path: str


class ReqsFileValidator:

    def __init__(self, reqs_file: TextIO):
        self._reqs_file = reqs_file

    async def validate(self) -> Iterable[ValidatedReq]:
        reqs = self._validate_reqs_file()
        await self._validate_reqs_existence_remote(reqs)
        return reqs

    def _validate_reqs_file(self) -> Iterable[ValidatedReq]:
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

            validated_reqs.add(ValidatedReq(package_name, version.strip()))
            package_names.add(package_name)

        return validated_reqs

    async def _validate_reqs_existence_remote(
            self,
            reqs: Iterable[ValidatedReq]
    ) -> None:
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

    def __init__(self, reqs: Iterable[ValidatedReq], destination: str):
        self._reqs = self._prepare_reqs_for_installation(
            reqs, destination
        )
        self._destination = destination

    async def install(self) -> None:
        self._filter_existing_requirements()
        self._create_requirements_directories()
        await asyncio.to_thread(self._install_requirements)

    @staticmethod
    def _prepare_reqs_for_installation(
            reqs: Iterable[ValidatedReq],
            destination: str
    ) -> Iterable[_InstallationReadyReq]:
        return [
            _InstallationReadyReq(
                *req,
                os.path.join(destination, req.package_name, req.version)
            )
            for req in reqs
        ]

    def _filter_existing_requirements(self) -> None:
        self._reqs = list(filter(
            lambda req: not os.path.exists(req.path),
            self._reqs
        ))

    def _create_requirements_directories(self) -> None:
        for _, _, path in self._reqs:
            os.makedirs(path, exist_ok=True)

    def _install_requirements(self) -> None:
        try:
            for package_name, version, path in self._reqs:
                subprocess.check_call([
                    sys.executable,
                    '-m',
                    'pip',
                    'install',
                    f'{package_name}=={version}',
                    '--no-deps',
                    '--target',
                    path
                ])

        except subprocess.CalledProcessError:
            for _, _, path in self._reqs:
                shutil.rmtree(path)

            raise ImpossibleInstallReqsError
