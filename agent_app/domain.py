import operator
from enum import Enum
from typing import TypedDict, Union, Annotated

from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

from langgraph.managed.base import ManagedValue
from pydantic import BaseModel


class IntentEnum(str, Enum):
    OFF_TOPIC = "off-topic"
    DATABASE = "database"
    CHAT = "chat"

class Intent(BaseModel):
    value: IntentEnum

class AgentState(TypedDict):
    input: str
    agent_outcome: Union[AgentAction, AgentFinish, None]
    intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]


class IsLastOrSecondToLastStepManager(ManagedValue[bool]):
    def __call__(self, step: int) -> bool:
        limit = self.config.get("recursion_limit", 0)
        return step >= limit - 2


class AgentMessagesState(TypedDict):
    question: str
    intent: IntentEnum
    messages: Annotated[list[AnyMessage], add_messages]
    count: int
    is_last_step: Annotated[bool, IsLastOrSecondToLastStepManager]
