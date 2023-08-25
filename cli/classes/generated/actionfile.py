# generated by datamodel-codegen:
#   filename:  actionfile.json

from __future__ import annotations

from typing import Dict, Optional, Union

from pydantic import BaseModel, Field, RootModel, constr

from . import definitions


class Step(RootModel):
    root: Union[
        definitions.FileAction,
        definitions.InternalAction,
        definitions.PlatformAction,
    ] = Field(..., description='Action that can be executed.', title='Step')


class ActionFile(BaseModel):
    """
    Defines an action that can be used in a windfile
    """

    api: definitions.Api
    metadata: definitions.Metadata
    environment: Optional[definitions.Environment] = None
    steps: Dict[constr(pattern=r'^[a-zA-Z0-9._-]+$'), Step] = Field(
        ...,
        description='The actions that are executed during a CI job in a target system. When a job is executed, the actions are executed in the order they are defined in the action.',
        title='Steps',
    )