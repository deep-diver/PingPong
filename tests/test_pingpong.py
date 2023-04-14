from pingpong import PingPong
from pingpong.dolly import DollyChatPPManager
from pingpong.gradio import GradioAlpacaChatPPManager

class TestPingpong():
    def test_context_dolly_pingpong(self):
        pp_manager = DollyChatPPManager()
        pp_manager.ctx = "this is context"
        result = pp_manager.add_ping("hello")
        answers = """Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction:
hello

### Input:
this is context

"""
        print(result)
        assert result == answers

    def test_simple_dolly_pingpong(self):
        pp_manager = DollyChatPPManager()
        result = pp_manager.add_ping("hello")
        answers = """Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction:
hello

"""
        assert result == answers
        assert pp_manager.add_ping("hello2") is None

        pp_manager.add_pong("world")
        result = pp_manager.add_ping("hello2")
        answers = """Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction:
hello2

"""
        assert result == answers
        assert pp_manager.add_ping("hello3") is None


    def test_ctx_alpaca_pingpong(self):
        pp = PingPong("hello", "world")
        pp_manager = GradioAlpacaChatPPManager()
        pp_manager.add_pingpong(pp)        

        prompts = pp_manager.build_prompts()
        answers = """### Instruction: hello

### Response: world"""
        assert prompts == answers

        uis = pp_manager.build_uis()
        answers = [("hello", "world")]
        assert uis == answers

        pp_manager.ctx = "this is context"
        answers = """### Instruction: hello

### Response: world"""
        prompts = pp_manager.build_prompts()
        assert prompts == answers

    def test_single_gradio_alpaca_pingpong(self):
        pp = PingPong("hello", "world")
        pp_manager = GradioAlpacaChatPPManager()
        pp_manager.add_pingpong(pp)

        prompts = pp_manager.build_prompts()
        answers = """### Instruction: hello

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
        answers = """### Instruction: ping-0

### Response: pong-0

### Instruction: ping-1

### Response: pong-1"""
        assert prompts == answers

        uis = pp_manager.build_uis()
        answers = [("ping-0", "pong-0"), ("ping-1", "pong-1")]
        assert uis == answers
            