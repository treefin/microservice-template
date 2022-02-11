import os

import git
from fastapi import APIRouter
from pydantic.schema import datetime as pydantic_datetime

from xxx_service.patterns import Singleton
from xxx_service.serialization_util import CamelCaseModel


class InfoDto(CamelCaseModel):
    """Info about micro service e.g. version, git metadata, etc."""

    git_tag: str
    git_commit_time: pydantic_datetime
    git_branch: str


info_router = APIRouter()


@info_router.get("/", response_model=InfoDto)
async def info() -> InfoDto:
    """Service version"""
    ver = ApiVersion()
    return InfoDto(
        git_tag=ver.tag,
        git_commit_time=ver.commit_time,
        git_branch=ver.commit_branch,
    )


class ApiVersion(metaclass=Singleton):
    """Contains misc data concerning api version"""

    def __init__(self) -> None:
        api_version_file = os.path.dirname(__file__) + os.sep + "api_version"
        # file is added in build process
        if os.path.exists(api_version_file):
            with open(api_version_file, encoding='utf-8') as fp:
                lines = fp.readlines()
                self.tag = lines[0].strip()
                self.commit_time = lines[1].strip()
                self.commit_branch = lines[2].strip()
        # for local development
        else:
            git_repo = git.Repo(os.path.dirname(__file__) + os.sep + "../")
            self.tag = git_repo.git.describe("--tags")
            self.commit_time = git_repo.head.commit.committed_datetime  # type: ignore
            self.commit_branch = git_repo.active_branch.name
