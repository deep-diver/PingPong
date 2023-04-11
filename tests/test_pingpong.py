import unittest

from pingpong.pingpong import PingPong
from pingpong.alpaca import AlpacaPromptFmt
from pingpong.gradio import GradioAlpacaChatPPManager

class TestPingpong():
    def test_single_gradio_alpaca_pingpong(self):
        pp = PingPong("hello", "world")
        pp_manager = GradioAlpacaChatPPManager()
        pp_manager.add_pingpong(pp)

        prompts = pp_manager.build_prompts()
        answers = f"""### Instruction: hello

### Response: world"""
        assert prompts == answers

        uis = pp_manager.build_uis()
        answers = [("hello", "world")]
        assert uis == answers

    def test_multi_gradio_pingpong(self):
        pp_manager = GradioAlpacaChatPPManager()

        for i in range(2):
            pp = PingPong(f"ping-{i}", f"pong-{i}")
            pp_manager.add_pingpong(pp)

        prompts = pp_manager.build_prompts()
        answers = f"""### Instruction: ping-0

### Response: pong-0

### Instruction: ping-1

### Response: pong-1"""
        assert prompts == answers

        uis = pp_manager.build_uis()
        answers = [("ping-0", "pong-0"), ("ping-1", "pong-1")]
        assert uis == answers        
            