import unittest

from pingpong.pingpong import PingPong
from pingpong.alpaca import AlpacaPromptFmt
from pingpong.gradio import GradioChatPPManager

class TestPingpong():
    def test_single_gradio_pingpong(self):
        pp = PingPong("hello", "world")
        pp_manager = GradioChatPPManager()
        pp_manager.add_pingpong(pp)

        prompts = pp_manager.build_prompts(AlpacaPromptFmt)
        answers = f"""### Instruction: hello

### Response: world"""
        assert prompts == answers

        uis = pp_manager.build_uis()
        answers = [("hello", "world")]
        assert uis == answers

    def test_multi_gradio_pingpong(self):
        pp_manager = GradioChatPPManager()

        for i in range(2):
            pp = PingPong(f"ping-{i}", f"pong-{i}")
            pp_manager.add_pingpong(pp)
        
        prompts = pp_manager.build_prompts(AlpacaPromptFmt)
        answers = f"""### Instruction: ping-0

### Response: pong-0

### Instruction: ping-1

### Response: pong-1"""
        assert prompts == answers
            