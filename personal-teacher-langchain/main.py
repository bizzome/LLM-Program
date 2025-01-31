from dotenv import load_dotenv
import argparse

from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
from langchain_core.messages import (
    AnyMessage,
    SystemMessage,
    ToolMessage,
)

from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults

from test import EarlyTests


_ = load_dotenv()

tool = TavilySearchResults(max_results=4)  # increased number of results
#print(type(tool))
#print(tool.name)


class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]


class Agent:

    def __init__(self, model, tools, system=""):
        self.system = system
        graph = StateGraph(AgentState)
        graph.add_node("llm", self.call_openai)
        graph.add_node("action", self.take_action)
        graph.add_conditional_edges(
            "llm", self.exists_action, {True: "action", False: END}
        )
        graph.add_edge("action", "llm")
        graph.set_entry_point("llm")
        self.graph = graph.compile()
        self.tools = {t.name: t for t in tools}
        self.model = model.bind_tools(tools)

    def exists_action(self, state: AgentState):
        result = state["messages"][-1]
        return len(result.tool_calls) > 0

    def call_openai(self, state: AgentState):
        messages = state["messages"]
        if self.system:
            messages = [SystemMessage(content=self.system)] + messages
        message = self.model.invoke(messages)
        return {"messages": [message]}

    def take_action(self, state: AgentState):
        tool_calls = state["messages"][-1].tool_calls
        results = []
        for t in tool_calls:
            print(f"Calling: {t}")
            if t["name"] not in self.tools:  # check for bad tool name from LLM
                print("\n ....bad tool name....")
                result = "bad tool name, retry"  # instruct LLM to retry if bad
            else:
                result = self.tools[t["name"]].invoke(t["args"])
            results.append(
                ToolMessage(
                    tool_call_id=t["id"], name=t["name"], content=str(result)
                )
            )
        print("Back to the model!")
        return {"messages": results}


prompt = """Você é um assistente de pesquisa inteligente. Use a search \
            engine disponível para buscar por informações. \
            Você tem permissão para realizar multiplas chamadas (juntas \
            ou em sequência. Apenas busque a informação quando tiver certeza \
            do que precisa. Se você precisar procurar alguma informação antes \
            de fazer uma pergunta de acompanhamento, você tem permissão para \
            fazer isso!
        """

model_35 = ChatOpenAI(model="gpt-3.5-turbo")  # reduce inference cost
abot_35 = Agent(model_35, [tool], system=prompt)

def main():
    function_tests = EarlyTests()
    parser = argparse.ArgumentParser(description="Run the agent with a query.")
    parser.add_argument(
        "--query",
        type=str,
        help="The query to send to the agent.",
    )
    args = parser.parse_args()

    if args.query:
        function_tests.send_one_complex_question(args.query)
    else:
        print("==== RUNNING DEFAULT EXAMPLES ====")
        function_tests.send_one_simple_question()
        function_tests.send_two_simple_questions()
        function_tests.send_one_complex_question()


if __name__ == "__main__":
    main()
