from pingpong.pingpong import PPManager
from pingpong.pingpong import PromptFmt

class RedPajamaChatPromptFmt(PromptFmt):
  @classmethod
  def ctx(cls, context):
    if context is None or context == "":
      return ""
    else:
      return f"""{context}

"""

  @classmethod
  def prompt(cls, pingpong, truncate_size):
    ping = pingpong.ping[:truncate_size]
    pong = "" if pingpong.pong is None or pingpong.pong == "" else f"{pingpong.pong[:truncate_size]}<|end|>\n"
    return f"""<human>: {ping}
<bot>: {pong}"""

class RedPajamaChatPPManager(PPManager):
  def build_prompts(self, from_idx: int=0, to_idx: int=-1, fmt: PromptFmt=RedPajamaChatPromptFmt, truncate_size: int=None):
    if to_idx == -1 or to_idx >= len(self.pingpongs):
      to_idx = len(self.pingpongs)

    results = fmt.ctx(self.ctx)

    for idx, pingpong in enumerate(self.pingpongs[from_idx:to_idx]):
      results += fmt.prompt(pingpong, truncate_size=truncate_size)

    return results