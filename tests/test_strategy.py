from pingpong.pingpong import PingPong
from pingpong.gradio import GradioAlpacaChatPPManager
from context.strategy import CtxAutoSummaryStrategy

class TestStrategy():
    def test_auto_summary_strategy(self):
        pp_manager = GradioAlpacaChatPPManager()
        strategy = CtxAutoSummaryStrategy(2)

        pp = PingPong("hello", "world")
        pp_manager.add_pingpong(pp)

        sum_req, to_summarize = strategy(pp_manager)
        assert sum_req == False

        pp = PingPong("hello2", "world2")
        pp_manager.add_pingpong(pp)

        sum_req, to_summarize = strategy(pp_manager)
        to_summarize_answer = """### Instruction: hello

### Response: world

### Instruction: hello2

### Response: world2"""
        assert sum_req == True
        assert to_summarize == to_summarize_answer
        assert strategy.last_idx == 2

        pp = PingPong("hello3", "world3")
        pp_manager.add_pingpong(pp)

        sum_req, to_summarize = strategy(pp_manager)
        assert sum_req == False

        pp = PingPong("hello4", "world4")
        pp_manager.add_pingpong(pp)

        sum_req, to_summarize = strategy(pp_manager)
        to_summarize_answer = """### Instruction: hello3

### Response: world3

### Instruction: hello4

### Response: world4"""
        assert sum_req == True
        assert to_summarize == to_summarize_answer
        assert strategy.last_idx == 4