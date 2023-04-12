from pingpong.pingpong import PPManager
from pingpong.context.strategy import CtxStrategy

class CtxAutoSummaryStrategy(CtxStrategy):
    def __init__(self, max_pingpongs: int):
        self.max_pingpongs = max_pingpongs
        self.last_idx = 0
    
    def __call__(self, ppmanager: PPManager):
        pps = ppmanager.pingpongs
        
        prev_idx = self.last_idx
        sum_req = False

        if len(pps[self.last_idx:]) >= self.max_pingpongs:
            sum_req = True
            self.last_idx = len(pps)

        return sum_req, ppmanager.build_prompts(from_idx=prev_idx)