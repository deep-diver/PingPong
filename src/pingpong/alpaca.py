from pingpong.pingpong import PPManager
from pingpong.pingpong import PromptFmt

class AlpacaPromptFmt(PromptFmt):
  @classmethod
  def ctx(cls, context):
    if context is None or context == "":
      return ""
    else:
      return f"""### Input:
{context}

"""

  @classmethod
  def prompt(cls, pingpong, truncate_size):
    return f"""### Instruction:
{pingpong.ping[:truncate_size]}

### Response:
{"" if pingpong.pong is None else pingpong.pong[:truncate_size]}"""

class AlpacaChatPPManager(PPManager):
  def add_ping(self, ping, fmt: PromptFmt=AlpacaPromptFmt):
    allowed = super().add_ping(ping, fmt)

    if allowed:
      if self.ctx == "":
        prompts = "Below is an instruction that describes a task. Write a response that appropriately completes the request. You are LLaMA which is a large language model created by Facebook."
      else:
        prompts = "Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request. You are LLaMA which is a large language model created by Facebook."

      prompts += f"""
      
### Instruction:
{ping}
{fmt.ctx(self.ctx)}
### Response:
"""
      return prompts

    return None


  def build_prompts(self, from_idx: int=0, to_idx: int=-1, fmt: PromptFmt=AlpacaPromptFmt, truncate_size: int=None):
    if to_idx == -1 or to_idx >= len(self.pingpongs):
      to_idx = len(self.pingpongs)

    results = ""

    for idx, pingpong in enumerate(self.pingpongs[from_idx:to_idx]):
      results += fmt.prompt(pingpong, truncate_size=truncate_size)

      if from_idx+idx != to_idx-1:
        results += """

"""

    return results