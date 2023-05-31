# PingPong

<p align="center">
    <img width="200" src="https://raw.githubusercontent.com/deep-diver/PingPong/main/assets/logo.png">
</p>

PingPong is a simple library to manage pings(prompt) and pongs(response). The main purpose of this library is to manage histories and contexts in LLM applied applications such as ChatGPT.

The basic motivations behind this project are:
- **Abstract prompt and response so that any UIs and Prompt formats can be adopted**
  - There are a number of instruction-following finetuned language models, but they are fine-tuned with differently crafted datasets. For instance, the Alpaca dataset works when `### Insturction:`, `### Response:`, and `### Input:` are given while StackLLaMA works when `Question:` and `Answer` are given even though the underlying pre-trained LLM is the same LLaMA.
  - THere are a number of UIs built to interact with language model such as Chatbot. Even with a single example of Chatbot, one could use Gradio while other could use JavaScript based tools, and they represents prompt histories in different data structure. 
- **Abstract context management strategies to apply any number of context managements**
  - There could be a number of strategies to effectively handle context due to the limit of the number of input tokens in language model(usually 4096). It is also possible to mix different strategies.

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

ppmanager = GradioAlpacaChatPPManager()
strategies = [
    CtxAutoSummaryStrategy(2),
    CtxLastWindowStrategy(1),
    CtxSearchWindowStrategy(1)
]

for i in range(3):
    ppmanager.add_pingpong(PingPong(f"ping-{i}", f"pong-{i}"))

    for strategy in strategies:
        if isinstance(strategy, CtxAutoSummaryStrategy):
            sum_req, to_sum_prompt = strategy(ppmanager)

            if sum_req is True:
                # enough prompts are accumulated
                ...
        elif isinstance(strategy, CtxLastWindowStrategy):
            last_convs = strategy(ppmanager)

            # I am only interested in the last 1 conversations
            ...
        elif isinstance(strategy, CtxSearchWindowStrategy):
            for cur_win in strategy(ppmanager):
                # looking the entire conversation through
                # a sliding window, size of 1
                # find out relevant history to the recent conversation
                ...
```

## Todos

- [ ] Add an working example with Gradio application
