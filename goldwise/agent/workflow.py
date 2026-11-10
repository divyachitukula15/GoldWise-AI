import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition

from goldwise.agent.tools import tools

load_dotenv()

def build_workflow():
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("Missing OPENROUTER_API_KEY in .env")

    llm = ChatOpenAI(
        model="openrouter/free",
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        temperature=0.3,
    )
    llm_with_tools = llm.bind_tools(tools)

    def agent_node(state: MessagesState):
        system_prompt = SystemMessage(content="""
        You are GoldWise AI, a Kamareddy market analyst.
        Respond in Telugu-English using English letters only.
        All prices are per 10 grams. Mention actual rate dates.
        Use tools for market data. Never invent prices or predict future prices.
        """)
        response = llm_with_tools.invoke([system_prompt] + state["messages"])
        return {"messages": [response]}

    graph = StateGraph(MessagesState)
    graph.add_node("agent", agent_node)
    graph.add_node("tools", ToolNode(tools))
    graph.add_edge(START, "agent")
    graph.add_conditional_edges("agent", tools_condition)
    graph.add_edge("tools", "agent")
    return graph.compile()

def ask_goldwise(question: str) -> str:
    from langchain_core.messages import HumanMessage
    app = build_workflow()
    result = app.invoke({"messages": [HumanMessage(content=question)]})
    return result["messages"][-1].content
