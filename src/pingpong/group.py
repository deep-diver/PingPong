from pingpong.pingpong import PPManager

class MirrorGroupPPManager:
    def __init__(self, ppms: List[PPManager]):
        self.ppmanagers = ppms

    def append_pong(self, piece_pong, at=0):
        self.ppmanagers[at].append_pong(piece_pong)

    def add_pingpong(self, pingpong, at=None):
        if at == None:
            for ppm in self.ppmanagers:
                ppm.add_pingpong(copy.deepcopy(pingpong))
        else:      
            self.ppmanagers[at].add_pingpong(copy.deepcopy(pingpong))

    def replace_pong(self, pong, at=None):
        if at == None:
            for ppm in self.ppmanagers:
                ppm.pingpongs[-1].pong = pong
        else:
            self.ppmanagers[at].pingpongs[-1].pong = pong
            
    def build_prompts(self, from_idx: int=0, to_idx: int=-1, truncate_size: int=None):
        results = []
        for ppm in self.ppmanagers:
            results.append(
                ppm.build_prompts(
                    from_idx=from_idx, 
                    to_idx=to_idx, 
                    truncate_size=truncate_size
                )
            )
        return results

    def build_uis(self, from_idx: int=0, to_idx: int=-1):
        return self.ppmanagers[0].build_uis(
            from_idx=from_idx, to_idx=to_idx
        )