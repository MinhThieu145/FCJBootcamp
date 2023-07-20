from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct

# import the child stack
from workshop1.cicd_stack import CICDStack

from workshop1.run_task_stack import RunTaskStack

from workshop1.frontend_stack import FrontendStack

from workshop1.test_stack import TestStack



# load the environment variables
from dotenv import load_dotenv
load_dotenv()


class Workshop1Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # initilize the child stack CICDStack
        CICDStack(
            scope=self,
            construct_id="CICDStack",
            stack_name="CICDStack",

        )

        # initilize the child stack RunTaskStack
        RunTaskStack(
            scope=self,
            construct_id="RunTaskStack",
            stack_name="RunTaskStack",
        )

        # initilize the child stack FrontendStack
        FrontendStack(
            scope=self,
            construct_id="FrontendStack",
            stack_name="FrontendStack",
        )
