from typing import Literal

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import END, START, StateGraph

from agent_app.domain import AgentMessagesState, IntentEnum
from agent_app.nodes import setup_intent_detection

load_dotenv()

def detect_intent(state: AgentMessagesState):
    count = state.get("count", 0)
    intent_detection = setup_intent_detection()
    messages = state.get("messages",[])
    if len(messages) > 0:
        message = messages[-1]
        intent = intent_detection.invoke(
            {
                "question": message.content
            }
        )
        print(intent)
        return {
            "count": count + 1,
            "intent": intent,
            "messages": [AIMessage(content=f"{intent.value.value} intent detected")]
        }
    else:
        return {
            "count": count + 1,
            "messages": AIMessage("This AI requires a question to be asked.")

        }



def route_to_rag(state:AgentMessagesState)-> Literal["rag", "__end__"]:
    """ Use in conditional edge to decide whether to route to rag or exit """
    intent = state["intent"]
    if intent.value == IntentEnum.OFF_TOPIC:
        return "__end__"
    else:
        return "rag"



def rag(state:AgentMessagesState):
    count = state.get("count", 0)
    return {"count": count + 1, "intent":state.get("intent")}





if __name__ == "__main__":
    print("Hello World")
    builder = StateGraph(AgentMessagesState)
    builder.add_node("detect_intent", detect_intent)
    builder.add_edge(START, "detect_intent")
    builder.add_node("rag", rag)
    # builder.add_edge("detect_intent", "rag")
    builder.add_conditional_edges(
        "detect_intent",
        route_to_rag,
        {"rag": "rag", "__end__": END}
    )
    builder.add_edge("rag", END)
    flow = builder.compile()

    # resp = flow.invoke({"messages": [HumanMessage(
    #         content="Who is Nelson Mandela?")]},
    #     config = {"configurable": {"thread_id": 42}}
    # )
    resp = flow.invoke({"messages": [HumanMessage(
        content="Who is the owner of the restaurant?")]},
        config={"configurable": {"thread_id": 42}}
    )
    print(resp)
