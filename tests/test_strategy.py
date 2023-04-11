from pingpong.pingpong import PingPong
from pingpong.gradio import GradioAlpacaChatPPManager
from context.auto_summary_strategy import CtxAutoSummaryStrategy
from context.last_window_strategy import CtxLastWindowStrategy


class TestStrategy():
	def test_last_window_strategy(self):
		pp_manager = GradioAlpacaChatPPManager()
		strategy = CtxLastWindowStrategy(2)

		for i in range(1):
			pp = PingPong(f"ping-{i}", f"pong-{i}")
			pp_manager.add_pingpong(pp)

		answers = f"""### Instruction: ping-0

### Response: pong-0"""
		assert strategy(pp_manager) == answers

		pp_manager = GradioAlpacaChatPPManager()
		for i in range(3):
			pp = PingPong(f"ping-{i}", f"pong-{i}")
			pp_manager.add_pingpong(pp)

		answers = f"""### Instruction: ping-1

### Response: pong-1

### Instruction: ping-2

### Response: pong-2"""
		assert strategy(pp_manager) == answers		


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
