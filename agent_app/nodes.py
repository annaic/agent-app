from enum import Enum

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import AIMessage
from pydantic import BaseModel

from agent_app.domain import Intent
from agent_app.model import get_model
from agent_app.prompts import intent_prompt


def setup_intent_detection():
    prompt = intent_prompt
    return prompt | get_model().with_structured_output(Intent)

# from agent_app.domain import OverallState
# from agent_app.prompts import split_questions_prompt, intent_detection_prompt
#
#
# class IntentEnum(str, Enum):
#     GREETING = "greeting"
#     SPECIFIC_QUESTION = "specific_question"
#     METADATA_QUERY = "metadata_query"
#     FOLLOW_UP_QUESTION = "follow_up_question"
#
# class Intent(BaseModel):
#     intent: IntentEnum
#
# def _setup_intent_detection():
#     prompt = intent_detection_prompt
#     llm = ChatAnthropic(model_name="claude-3-5-sonnet-20240620")
#     llm_with_tools = llm.bind_tools(tools=[Intent])
#     return prompt | llm_with_tools
#
# async def detect_intent(state :OverallState, config):
#     messages = state["messages"]
#     question = messages[-1].content
#     chat_history = messages[:-1]
#     intent_detection = _setup_intent_detection()
#     response = await intent_detection.ainvoke({"chat_history": chat_history, "question": question})
#     # logger.info(f"Intent detection response: {response['intent']}")
#     return {"intent": response['intent']}
#
# class QuestionList(BaseModel):
#     questions: list[str]
#
# def _setup_question_detection():
#     llm = ChatAnthropic(model_name="claude-3-5-sonnet-20240620")
#     llm_with_tools = llm.bind_tools(tools=[QuestionList])
#     return split_questions_prompt | llm_with_tools
#
# async def split_question_list(state: OverallState, config):
#     split_questions = _setup_question_detection()
#     question = state['messages'][-1].content
#
#     questions = await split_questions.ainvoke({"QUESTION": question})
#     # logger.info("Question was split into %s parts", len(questions))
#     return {"question_list": questions}
#
#
#
#
# async def llm_answer(state :OverallState, config):
#     messages = state["messages"]
#     llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
#     response = await llm.ainvoke(messages)
#     response = AIMessage(content=response.content)
#     return {"messages": response}










