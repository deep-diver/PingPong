# PingPong

<p align="center">
    <img width="200" src="https://raw.githubusercontent.com/deep-diver/PingPong/main/assets/logo.png">
</p>

PingPong is a simple library to manage pings(prompt) and pongs(response). The main purpose of this library is to manage histories and contexts in LLM applied applications such as ChatGPT.

The basic motivations behind this project are:
- Abstract prompt and response so that any UIs and Prompt formats can be adopted
- Abstract context management strategies to apply any number of context managements

## Installation

```shell
$ pip install bingbong
```

## Example usage

```python
from pingpong import PingPong
from pingpong.gradio import GradioAlpacaChatPPManager
from pingpong.context import CtxAutoSummaryStrategy
from pingpong.context import CtxLastWindowStrategy
from pingpong.context import CtxSearchWindowStrategy

```python
ppmanager = GradioAlpacaChatPPManager()
strategies = [
    CtxAutoSummaryStrategy(2),
    CtxLastWindowStrategy(1),
    CtxSearchWindowStrategy(1)
]

for i in range(3):
    ppmanager.add_pingpong(PingPong(f"ping-{i}", f"pong-{i}"))

    for strategy in strategies:
        if isinstanceof(strategy, CtxAutoSummaryStrategy):
            sum_req, to_sum_prompt = strategy(ppmanager)

            if sum_req is True:
                # enough prompts are accumulated
                ...
        elif isinstanceof(strategy, CtxLastWindowStrategy):
            last_convs = strategy(ppmanager)

            # I am only interested in the last 1 conversations
            ...
        elif isinstanceof(strategy, CtxSearchWindowStrategy):
            for cur_win in strategy(ppmanager):
                # looking the entire conversation through
                # a sliding window, size of 1
                # find out relevant history to the recent conversation
                ...
```