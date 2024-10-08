import re
import argparse

from chatbot.tools import wikipedia, calculate, google_search
from chatbot import ChatBot

prompt = """
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

Your available actions are:

calculate:
e.g. calculate: 4 * 7 / 3
Runs a calculation and returns the number - uses Python so be sure to use
floating point syntax if necessary

wikipedia:
e.g. wikipedia: Django
Returns a summary from searching Wikipedia

google_search:
e.g. google_search: Django
Search with google for that term

Always look things up on Wikipedia if you have the opportunity to do so.

Example session:

Question: What is the capital of France?
Thought: I should look up France on Wikipedia
Action: wikipedia: France
PAUSE

You will be called again with this:

Observation: France is a country. The capital is Paris.

You then output:

Answer: The capital of France is Paris
""".strip()


action_re = re.compile("^Action: (\w+): (.*)$")


known_actions = {
    "wikipedia": wikipedia,
    "calculate": calculate,
    "google_search": google_search,
}


def query(question, max_turns=6):
    i = 0
    bot = ChatBot(prompt)
    next_prompt = question
    while i < max_turns:
        i += 1
        result = bot(next_prompt)
        print(result)
        actions = [
            action_re.match(a)
            for a in result.split("\n")
            if action_re.match(a)
        ]
        if actions:
            # There is an action to run
            action, action_input = actions[0].groups()
            if action not in known_actions:
                raise Exception(
                    "Unknown action: {}: {}".format(action, action_input)
                )
            print(" -- running {} {}".format(action, action_input))
            observation = known_actions[action](action_input)
            print("Observation:", observation)
            next_prompt = "Observation: {}".format(observation)
        else:
            return


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--query",
        type=str,
        required=True,
        help=(
            "Query to search on chatbot, e.g. --query 'Python "
            "(programming language)'."
        ),
    )
    args = parser.parse_args()
    return args.query


if __name__ == "__main__":
    question = get_args()
    query(question)
