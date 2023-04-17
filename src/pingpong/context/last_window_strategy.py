from pingpong.pingpong import PPManager
from pingpong.context.strategy import CtxStrategy

class CtxLastWindowStrategy(CtxStrategy):
    def __init__(self, max_pingpongs: int):
        self.max_pingpongs = max_pingpongs
    
    def __call__(self, ppmanager: PPManager, build_uis=False, truncate_size=None):
        pps = ppmanager.pingpongs

        if len(pps) <= self.max_pingpongs:
            start_idx = 0
        else:
            start_idx = len(pps) - self.max_pingpongs

        if build_uis:
            return (
                ppmanager.build_prompts(from_idx=start_idx, truncate_size=truncate_size),
                ppmanager.build_uis(from_idx=start_idx)
            )
        else:
            return ppmanager.build_prompts(from_idx=start_idx, truncate_size=truncate_size)