from pingpong.pingpong import PPManager
from pingpong.context.strategy import CtxStrategy

class CtxLastWindowStrategy(CtxStrategy):
    def __init__(self, max_pingpongs: int):
        self.max_pingpongs = max_pingpongs
    
    def __call__(self, ppmanager: PPManager):
        pps = ppmanager.pingpongs

        if len(pps) <= self.max_pingpongs:
            start_idx = 0
        else:
            start_idx = len(pps) - self.max_pingpongs

        return ppmanager.build_prompts(from_idx=start_idx)