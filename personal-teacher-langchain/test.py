from main import Agent
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults

from colorama import Fore, Style


class EarlyTests:
    def __init__(self):
        self.model = ChatOpenAI(model="gpt-3.5-turbo")  # reduce inference cost
        self.prompt = """Você é um assistente de pesquisa inteligente. Use a search \
            engine disponível para buscar por informações. \
            Você tem permissão para realizar multiplas chamadas (juntas \
            ou em sequência. Apenas busque a informação quando tiver certeza \
            do que precisa. Se você precisar procurar alguma informação antes \
            de fazer uma pergunta de acompanhamento, você tem permissão para \
            fazer isso!
        """
        self.tool = TavilySearchResults(max_results=4)  # increased number of results
        self.abot = Agent(self.model, [self.tool], system=self.prompt)

    def send_one_simple_question(self, query: str = "Qual o tempo em São Paulo?"):
        messages = [HumanMessage(content=query)]
        result = self.abot.graph.invoke({"messages": messages})

        # print(result)
        print(Fore.GREEN + result["messages"][-1].content)
        print(Style.RESET_ALL)


    def send_two_simple_questions(
        self,
        query: str = "Qual o tempo em São Paulo? Qual o tempo em Piracicaba?",
    ):
        messages = [HumanMessage(content=query)]
        result = self.abot.graph.invoke({"messages": messages})

        print(
            Fore.GREEN
            + "Última mensagem: {}".format(result["messages"][-1].content)
        )
        print(Style.RESET_ALL)


    # Note, the query was modified to produce more consistent results.
    # Results may vary per run and over time as search information and models change.
    def send_one_complex_question(
        self,
        query: str = "Quando foram as últimas olimpíadas? \
        Qual país ganhou mais medalhas de ouro? \
        Quantos habitantes possui este país? \
        Responda cada pergunta.",
    ):
        messages = [HumanMessage(content=query)]

        model = ChatOpenAI(model="gpt-4o")  # requires more advanced model
        abot = Agent(model, [self.tool], system=self.prompt)
        result = abot.graph.invoke({"messages": messages})

        print(
            Fore.GREEN
            + "Conteúdo da última mensagem: {}".format(
                result["messages"][-1].content
            )
        )
        print(Style.RESET_ALL)