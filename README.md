# PingPong

PingPong is a simple library to manage pings(prompt) and pongs(response). The main purpose of this library is to manage histories and contexts in LLM applied applications such as ChatGPT.

The basic motivations behind this project are:
- Abstract prompt and response so that any UIs and Prompt formats can be adopted
- Abstract context management strategies to apply any number of context managements

Below shows a simple example with Gradio(UI) and Alpaca(Prompt):
```python
ui_answers = [("ping-0", "pong-0"), ("ping-1", "pong-1")]
prompt_answers = f"""### Instruction: ping-0

### Response: pong-0

### Instruction: ping-1

### Response: pong-1"""

pp_manager = GradioAlpacaChatPPManager()
strategy = CtxAutoSummaryStrategy(2)

for i in range(2):
    pp = PingPong(f"ping-{i}", f"pong-{i}")
    pp_manager.add_pingpong(pp)

prompts = pp_manager.build_prompts()
assert prompts == prompt_answers

uis = pp_manager.build_uis()
assert uis == ui_answers

sum_req, to_summarize = strategy(pp_manager)
assert sum_req == True
assert to_summarize == prompt_answers
assert strategy.last_idx == 2
```