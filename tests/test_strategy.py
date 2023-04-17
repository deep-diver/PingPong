from pingpong import PingPong
from pingpong.gradio import GradioAlpacaChatPPManager
from pingpong.context import CtxAutoSummaryStrategy
from pingpong.context import CtxLastWindowStrategy
from pingpong.context import CtxSearchWindowStrategy


class TestStrategy():
	def test_search_window_strategy(self):
		pp_manager = GradioAlpacaChatPPManager()
		strategy = CtxSearchWindowStrategy(2)

		for i in range(5):
			pp = PingPong(f"ping-{i}", f"pong-{i}")
			pp_manager.add_pingpong(pp)

		answer1 = """### Instruction:
ping-0

### Response:
pong-0

### Instruction:
ping-1

### Response:
pong-1"""

		answer2 = """### Instruction:
ping-2

### Response:
pong-2

### Instruction:
ping-3

### Response:
pong-3"""

		answer3 = """### Instruction:
ping-4

### Response:
pong-4"""

		for idx, win in enumerate(strategy(pp_manager)):
			if idx == 0:
				assert win == answer1
			elif idx == 1:
				assert win == answer2
			elif idx == 2:
				assert win == answer3
			else:
				assert True is False

	def test_last_window_strategy_w_truncate(self):
		pp_manager = GradioAlpacaChatPPManager()
		strategy = CtxLastWindowStrategy(2)

		pp_manager = GradioAlpacaChatPPManager()
		for i in range(3):
			pp = PingPong(f"ping-{i}", f"pong-{i}")
			pp_manager.add_pingpong(pp)

		answers = """### Instruction:
pi

### Response:
po

### Instruction:
pi

### Response:
po"""
		assert strategy(pp_manager, truncate_size=2) == answers

	def test_last_window_strategy(self):
		pp_manager = GradioAlpacaChatPPManager()
		strategy = CtxLastWindowStrategy(2)

		for i in range(1):
			pp = PingPong(f"ping-{i}", f"pong-{i}")
			pp_manager.add_pingpong(pp)

		answers = """### Instruction:
ping-0

### Response:
pong-0"""
		assert strategy(pp_manager) == answers

		pp_manager = GradioAlpacaChatPPManager()
		for i in range(3):
			pp = PingPong(f"ping-{i}", f"pong-{i}")
			pp_manager.add_pingpong(pp)

		answers = """### Instruction:
ping-1

### Response:
pong-1

### Instruction:
ping-2

### Response:
pong-2"""
		assert strategy(pp_manager) == answers


	def test_auto_summary_strategy(self):
		pp_manager = GradioAlpacaChatPPManager()
		strategy = CtxAutoSummaryStrategy(2)

		pp = PingPong("hello", "world")
		pp_manager.add_pingpong(pp)

		sum_req, to_summarize = strategy(pp_manager)
		assert sum_req is False

		pp = PingPong("hello2", "world2")
		pp_manager.add_pingpong(pp)

		sum_req, to_summarize = strategy(pp_manager)
		to_summarize_answer = """### Instruction:
hello

### Response:
world

### Instruction:
hello2

### Response:
world2"""
		assert sum_req is True
		assert to_summarize == to_summarize_answer
		assert strategy.last_idx == 2

		pp = PingPong("hello3", "world3")
		pp_manager.add_pingpong(pp)

		sum_req, to_summarize = strategy(pp_manager)
		assert sum_req is False

		pp = PingPong("hello4", "world4")
		pp_manager.add_pingpong(pp)

		sum_req, to_summarize = strategy(pp_manager)
		to_summarize_answer = """### Instruction:
hello3

### Response:
world3

### Instruction:
hello4

### Response:
world4"""

		assert sum_req is True
		assert to_summarize == to_summarize_answer
		assert strategy.last_idx == 4
