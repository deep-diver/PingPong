from pingpong.pingpong import PPManager
from pingpong.pingpong import PromptFmt

class DollyPromptFmt(PromptFmt):
  @classmethod
  def ctx(cls, context):
    if context is None or context == "":
      return ""
    else:
      return f"""
### Input:
{context}
"""

  @classmethod
  def prompt(cls, pingpong, truncate_size):
    return f"""### Instruction:
{pingpong.ping[:truncate_size]}

### Response:
{"" if pingpong.pong is None else pingpong.pong[:truncate_size]}"""

class DollyChatPPManager(PPManager):
  def add_ping(self, ping, fmt: PromptFmt=DollyPromptFmt):
    allowed = super().add_ping(ping, fmt)

    if allowed:
      prompts = f"""Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction:
{ping}
{fmt.ctx(self.ctx)}
"""
      return prompts

    return None

  def build_prompts(self, from_idx: int=0, to_idx: int=-1, fmt: PromptFmt=DollyPromptFmt, truncate_size: int=None):
    if to_idx == -1 or to_idx >= len(self.pingpongs):
      to_idx = len(self.pingpongs)

    results = fmt.ctx(self.ctx)

    for idx, pingpong in enumerate(self.pingpongs[from_idx:to_idx]):
      print(idx)
      results += fmt.prompt(pingpong)

      if from_idx+idx != to_idx-1:
        results += """

"""

    return results