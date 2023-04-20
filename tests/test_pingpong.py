from pingpong import PingPong
from pingpong.dolly import DollyChatPPManager
from pingpong.stablelm import StableLMChatPPManager
from pingpong.gradio import GradioAlpacaChatPPManager
from pingpong.context import CtxLastWindowStrategy

class TestPingpong():
    def test_simple_stablelm_pingpong(self):
        system_prompt = """<|SYSTEM|># StableLM Tuned (Alpha version)
- StableLM is a helpful and harmless open-source AI language model developed by StabilityAI.
- StableLM is excited to be able to help the user, but will refuse to do anything that could be considered harmful to the user.
- StableLM is more than just an information source, StableLM is also able to write poetry, short stories, and make jokes.
- StableLM will refuse to participate in anything that could harm a human.
"""      

        pp_manager = StableLMChatPPManager()
        strategy = CtxLastWindowStrategy(2)
        result = pp_manager.add_ping("hello")
        answers = f"{system_prompt}<|USER|>hello<|ASSISTANT|>"

        print(result)
        assert result == answers

        pp_manager.add_pong("")
        answers = f"<|USER|>hello<|ASSISTANT|>"
        assert pp_manager.build_prompts() == answers

        pp_manager.append_pong("world")
        answers = f"<|USER|>hello<|ASSISTANT|>world"
        assert pp_manager.build_prompts() == answers
        last_conversations = strategy(pp_manager)
        assert last_conversations == answers

        result = pp_manager.add_ping("nice to")
        result = result.replace(system_prompt, f"{system_prompt}{last_conversations}")
        answers = f"{system_prompt}<|USER|>hello<|ASSISTANT|>world<|USER|>nice to<|ASSISTANT|>"
        assert result == answers

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
        answers = """### Instruction:
hello

### Response:
world"""
        assert prompts == answers

        uis = pp_manager.build_uis()
        answers = [("hello", "world")]
        assert uis == answers

        pp_manager.ctx = "this is context"
        answers = """### Instruction:
hello

### Response:
world"""
        prompts = pp_manager.build_prompts()
        assert prompts == answers

    def test_single_gradio_alpaca_pingpong(self):
        pp = PingPong("hello", "world")
        pp_manager = GradioAlpacaChatPPManager()
        pp_manager.add_pingpong(pp)

        prompts = pp_manager.build_prompts()
        answers = """### Instruction:
hello

### Response:
world"""
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
        answers = """### Instruction:
ping-0

### Response:
pong-0

### Instruction:
ping-1

### Response:
pong-1"""
        assert prompts == answers

        uis = pp_manager.build_uis()
        answers = [("ping-0", "pong-0"), ("ping-1", "pong-1")]
        assert uis == answers
            