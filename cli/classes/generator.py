from typing import Optional

from classes.generated.definitions import (
    Target,
)
from classes.generated.windfile import WindFile
from classes.input_settings import InputSettings
from classes.merger import Merger
from classes.output_settings import OutputSettings
from classes.pass_settings import PassSettings
from classes.validator import Validator
from generators.cli import CliGenerator
from generators.jenkins import JenkinsGenerator
from utils import logger


class Generator(PassSettings):
    target: Target

    def __init__(
        self,
        input_settings: InputSettings,
        output_settings: OutputSettings,
        target: Target,
    ):
        validator: Validator = Validator(
            output_settings=output_settings, input_settings=input_settings
        )
        validated: Optional[WindFile] = validator.validate_wind_file()
        if validated:
            self.windfile = validated
        merger: Merger = Merger(
            windfile=validated,
            input_settings=input_settings,
            output_settings=output_settings,
            metadata=validator.metadata,
        )
        windfile: Optional[WindFile] = merger.merge()
        if not windfile:
            logger.error(
                "❌", "Merging failed. Aborting.", output_settings.emoji
            )
            raise ValueError("Merging failed.")

        super().__init__(
            input_settings,
            output_settings,
            windfile=windfile,
            metadata=merger.metadata,
        )
        self.target = target

    def generate(self) -> None:
        if not self.windfile:
            logger.error(
                "❌", "Merging failed. Aborting.", self.output_settings.emoji
            )
            return None
        # current_action: FileAction | InternalAction | PlatformAction |
        # ExternalAction = self.windfile.jobs[
        #     "hello-world_0"
        # ].root
        # if not isinstance(current_action, InternalAction):
        #     logger.error(
        #         "❌",
        #         "Merging did not result in all internal actions",
        #         self.output_settings.emoji,
        #     )
        #     return
        # action: InternalAction = current_action
        # code: str = action.script
        # print(code)
        # print("calling:")
        # execute_arbitrary_code(code, "build", "hello-world_0")
        actual_generator: Optional[Generator] = None
        if self.target == Target.cli.name:
            actual_generator = CliGenerator(
                windfile=self.windfile,
                input_settings=self.input_settings,
                output_settings=self.output_settings,
                metadata=self.metadata,
            )
        if self.target == Target.jenkins.name:
            actual_generator = JenkinsGenerator(
                windfile=self.windfile,
                input_settings=self.input_settings,
                output_settings=self.output_settings,
                metadata=self.metadata,
            )
        if actual_generator:
            result: str = actual_generator.generate()
            print(result)
        return None