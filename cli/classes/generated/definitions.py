# generated by datamodel-codegen:
#   filename:  definitions.json

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, RootModel, constr


class Model(RootModel):
    root: Any


class Api(RootModel):
    root: str = Field(..., description='The API version of the windfile.', examples=['v0.0.1'], title='API Version')


class Dictionary(RootModel):
    root: Dict[constr(pattern=r'.+'), Optional[Union[Any, str, float, bool]]]


class Target(Enum):
    """
    The CI platforms that are able to run this windfile.
    """

    cli = 'cli'
    jenkins = 'jenkins'
    bamboo = 'bamboo'


class ContactData(BaseModel):
    """
    Contact data of the author.
    """

    name: str = Field(..., description='The name of the author.', examples=['Andreas Resch'])
    email: Optional[str] = Field(None, description='The email of the author.', examples=['aeolus@resch.io'])


class Docker(BaseModel):
    """
    Docker configuration that is used to execute the actions
    """

    image: str = Field(..., description='The docker image that is used to execute the action', examples=['rust:latest'])
    tag: Optional[str] = Field(
        'latest', description='The tag of the docker image that is used to execute the action', examples=['latest']
    )
    volumes: Optional[List[str]] = Field(None, description='The volumes that are mounted into the docker container')
    parameters: Optional[List[str]] = Field(
        None, description='The parameters that are passed to the docker daemon, e.g. --cpus=2'
    )


class Lifecycle(Enum):
    """
    Defines a part of the lifecycle of a job.
    """

    preparation = 'preparation'
    working_time = 'working_time'
    post_deadline = 'post_deadline'
    evaluation = 'evaluation'
    all = 'all'


class Parameters(RootModel):
    root: Dictionary = Field(..., description='The parameters of an action.', title='Parameters of an action.')


class Repository(BaseModel):
    """
    Repository to be checked out during the execution of the actions
    """

    url: str = Field(..., description='The url of the repository', examples=['https://github.com/ls1intum/Aeolus.git'])
    branch: str = Field(..., description='The branch to check out', examples=['main'])
    path: str = Field(
        ..., description='The path where the content of the repository should be checked out', examples=['.', 'tests']
    )


class GitCredentials(BaseModel):
    """
    Git credentials that are used to clone the repositories.
    """

    username: str = Field(..., description='The username of the git credentials.', examples=['aeolus'])
    password: str = Field(..., description='The password of the git credentials.', examples=['aeolus'])


class Environment(RootModel):
    root: Dictionary = Field(..., description='Environment variables for actions.', title='Environment')


class Author(RootModel):
    root: Union[str, ContactData] = Field(..., description='The author of the windfile.', title='Author')


class ExternalAction(BaseModel):
    """
    External action that can be executed with or without parameters.
    """

    model_config = ConfigDict(
        extra='forbid',
    )
    name: str = Field(..., description='The name of the action.', examples=['rust-exercise-jobs'])
    use: str = Field(..., description='The name of the external action.', title='Name of the external action.')
    parameters: Optional[Parameters] = None
    excludeDuring: Optional[List[Lifecycle]] = Field(
        None,
        description='Exclude this action during the specified parts of the lifetime of an exercise.',
        title='Exclude during',
    )
    environment: Optional[Environment] = Field(None, description='Environment variables for this external action.')
    platform: Optional[Target] = Field(
        None,
        description="The platform that this action is defined for. If it's not set, the action is defined for all platforms.",
    )
    docker: Optional[Docker] = Field(None, description='The docker configuration that is used to execute the action')
    runAlways: Optional[bool] = Field(
        False, description='If this is set to true, the action is always executed, even if other actions fail.'
    )
    workdir: Optional[str] = Field(
        None, description='The working directory of the external action.', examples=['tests']
    )


class FileAction(BaseModel):
    """
    Action that is defined in a file.
    """

    model_config = ConfigDict(
        extra='forbid',
    )
    name: str = Field(..., description='The name of the action.', examples=['rust-exercise-jobs'])
    file: str = Field(..., description='The file that contains the action.')
    parameters: Optional[Parameters] = None
    excludeDuring: Optional[List[Lifecycle]] = Field(
        None,
        description='Exclude this action during the specified parts of the lifetime of an exercise.',
        title='Exclude during',
    )
    environment: Optional[Environment] = Field(None, description='Environment variables for this file action.')
    platform: Optional[Target] = Field(
        None,
        description="The platform that this action is defined for. If it's not set, the action is defined for all platforms.",
    )
    docker: Optional[Docker] = Field(None, description='The docker configuration that is used to execute the action')
    runAlways: Optional[bool] = Field(
        False, description='If this is set to true, the action is always executed, even if other actions fail.'
    )
    workdir: Optional[str] = Field(None, description='The working directory of the file action.', examples=['tests'])


class PlatformAction(BaseModel):
    """
    Action that is defined for a specific platform.
    """

    model_config = ConfigDict(
        extra='forbid',
    )
    name: str = Field(..., description='The name of the action.', examples=['rust-exercise-jobs'])
    file: Optional[str] = Field(None, description='The file of the platform action. Written in Python')
    parameters: Optional[Parameters] = None
    function: Optional[constr(pattern=r'^[a-zA-Z0-9._-]+$')] = Field(
        'run', description='The function of the platform action.', examples=['run']
    )
    excludeDuring: Optional[List[Lifecycle]] = Field(
        None,
        description='Exclude this action during the specified parts of the lifetime of an exercise.',
        title='Exclude during',
    )
    environment: Optional[Environment] = Field(None, description='Environment variables for this platform action.')
    platform: Optional[Target] = Field(None, description='Ignored for this action.')
    kind: Optional[str] = Field(None, description='The kind of the platform action.', examples=['junit'])
    docker: Optional[Docker] = Field(None, description='The docker configuration that is used to execute the action')
    runAlways: Optional[bool] = Field(
        False, description='If this is set to true, the action is always executed, even if other actions fail.'
    )
    workdir: Optional[str] = Field(
        None, description='The working directory of the platform action.', examples=['tests']
    )


class ScriptAction(BaseModel):
    """
    Internally defined action that can be executed.
    """

    model_config = ConfigDict(
        extra='forbid',
    )
    name: str = Field(..., description='The name of the action.', examples=['rust-exercise-jobs'])
    script: str = Field(..., description='The script of the internal action. Written in aeolus DSL')
    excludeDuring: Optional[List[Lifecycle]] = Field(
        None,
        description='Exclude this action during the specified parts of the lifetime of an exercise.',
        title='Exclude during',
    )
    parameters: Optional[Parameters] = None
    environment: Optional[Environment] = Field(None, description='Environment variables for this internal action.')
    platform: Optional[Target] = Field(
        None,
        description="The platform that this action is defined for. If it's not set, the action is defined for all platforms.",
    )
    docker: Optional[Docker] = Field(None, description='The docker configuration that is used to execute the action')
    runAlways: Optional[bool] = Field(
        False, description='If this is set to true, the action is always executed, even if other actions fail.'
    )
    workdir: Optional[str] = Field(
        None, description='The working directory of the platform action.', examples=['tests']
    )


class WindfileMetadata(BaseModel):
    """
    Metadata of the windfile.
    """

    name: str = Field(..., description='The name of the windfile.', examples=['rust-exercise-jobs'])
    id: Optional[str] = Field(
        None,
        description='The id of the resulting job in the CI system.',
        examples=['rust-exercise-jobs', 'AEOLUS-BASE', 'jenkins/job/path'],
    )
    description: str = Field(
        ...,
        description='Description of what this list of actions is supposed to achieve',
        examples=['This windfile contains the jobs that are executed during the CI of the rust-exercise.'],
    )
    author: Author = Field(..., description='The author of the windfile.')
    targets: Optional[List[Target]] = Field(None, description='The targets of the windfile.')
    gitCredentials: Optional[Union[str, GitCredentials]] = Field(
        None, description='The git credentials that are used to clone the repositories'
    )
    docker: Optional[Docker] = Field(None, description='The docker configuration that is used to execute the actions')
    resultHook: Optional[str] = Field(
        None,
        description='The result hook that is called after the execution of the actions, always. This can be used to send the results to a server.',
        examples=['https://example.com/hey-i-got-news-for-you'],
    )


class Action(RootModel):
    root: Union[FileAction, ScriptAction, PlatformAction, ExternalAction] = Field(
        ..., description='Action that can be executed.', title='Action'
    )


class ActionMetadata(BaseModel):
    """
    Metadata of the actionfile.
    """

    name: str = Field(..., description='The name of the windfile.', examples=['rust-exercise-jobs'])
    description: str = Field(
        ...,
        description='Description of what this list of actions is supposed to achieve',
        examples=['This windfile contains the jobs that are executed during the CI of the rust-exercise.'],
    )
    author: Author = Field(..., description='The author of the actionfile.')
    targets: Optional[List[Target]] = Field(None, description='The targets of the windfile.')
