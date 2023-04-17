from typing import List

from pingpong import PingPong
from pingpong.gradio import GradioAlpacaChatPPManager
from pingpong.context import CtxAutoSummaryStrategy
from pingpong.context import CtxLastWindowStrategy

class TestScenarios():
    def test_basic_chat_workflow(self):
        ppmanager = GradioAlpacaChatPPManager()
        strategies = [
            CtxAutoSummaryStrategy(max_pingpongs=3),
            CtxLastWindowStrategy(max_pingpongs=2)
        ]

        conv1 = PingPong("Hello", "Hi, Nice to meet you!")
        ppmanager.add_pingpong(conv1)

        for strategy in strategies:
            if isinstance(strategy, CtxAutoSummaryStrategy):
                sum_req, _ = strategy(ppmanager)
                assert sum_req is False
            elif isinstance(strategy, CtxLastWindowStrategy):
                answers = """### Instruction:
Hello

### Response:
Hi, Nice to meet you!"""
                assert strategy(ppmanager) == answers

        conv2 = PingPong("How are you?", "I am fine. Thank you, and you?")
        ppmanager.add_pingpong(conv2)

        for strategy in strategies:
            if isinstance(strategy, CtxAutoSummaryStrategy):
                sum_req, _ = strategy(ppmanager)
                assert sum_req is False
            elif isinstance(strategy, CtxLastWindowStrategy):
                answers = """### Instruction:
Hello

### Response:
Hi, Nice to meet you!

### Instruction:
How are you?

### Response:
I am fine. Thank you, and you?"""
                assert strategy(ppmanager) == answers

        conv3 = PingPong("I am doing well.", "Good to know :)")
        ppmanager.add_pingpong(conv3)

        for strategy in strategies:
            if isinstance(strategy, CtxAutoSummaryStrategy):
                answers = """### Instruction:
Hello

### Response:
Hi, Nice to meet you!

### Instruction:
How are you?

### Response:
I am fine. Thank you, and you?

### Instruction:
I am doing well.

### Response:
Good to know :)"""
                sum_req, to_summarize = strategy(ppmanager)
                assert sum_req is True
                assert to_summarize == answers
            elif isinstance(strategy, CtxLastWindowStrategy):
                answers = """### Instruction:
How are you?

### Response:
I am fine. Thank you, and you?

### Instruction:
I am doing well.

### Response:
Good to know :)"""
                assert strategy(ppmanager) == answers

        conv4 = PingPong("What do you want to do today?", "I feel like I want to stay at home")
        ppmanager.add_pingpong(conv4)

        for strategy in strategies:
            if isinstance(strategy, CtxAutoSummaryStrategy):
                sum_req, to_summarize = strategy(ppmanager)
                assert sum_req is False
            elif isinstance(strategy, CtxLastWindowStrategy):
                answers = """### Instruction:
I am doing well.

### Response:
Good to know :)

### Instruction:
What do you want to do today?

### Response:
I feel like I want to stay at home"""
                assert strategy(ppmanager) == answers