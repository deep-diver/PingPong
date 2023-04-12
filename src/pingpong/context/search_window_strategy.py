from pingpong.pingpong import PPManager
from pingpong.context.strategy import CtxStrategy

class CtxSearchWindowStrategy(CtxStrategy):
    def __init__(self, window_size: int):
        self.window_size = window_size
    
    def __call__(self, ppmanager: PPManager):
        pps = ppmanager.pingpongs
        num_wins = len(pps) // self.window_size
        remainings = True if len(pps) % self.window_size != 0 else False

        for win_idx in range(num_wins):
            cur_win_start_idx = win_idx * self.window_size
            cur_win_end_idx = cur_win_start_idx + self.window_size
            yield ppmanager.build_prompts(from_idx=cur_win_start_idx, to_idx=cur_win_end_idx)

        if remainings:
            last_win_start_idx = (num_wins) * self.window_size
            yield ppmanager.build_prompts(from_idx=last_win_start_idx)