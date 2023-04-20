from pingpong.pingpong import PPManager
from pingpong.pingpong import PromptFmt

class StableLMPromptFmt(PromptFmt):
  @classmethod
  def prompt(cls, pingpong, truncate_size):
    ping = pingpong.ping[:truncate_size]
    pong = "" if pingpong.pong is None else pingpong.pong[:truncate_size]
    return f"<|USER|>{ping}<|ASSISTANT|>{pong}"

class StableLMChatPPManager(PPManager):
  def add_ping(self, ping, fmt: PromptFmt=StableLMPromptFmt):
    allowed = super().add_ping(ping, fmt)

    if allowed:
      system_prompt = """<|SYSTEM|># StableLM Tuned (Alpha version)
- StableLM is a helpful and harmless open-source AI language model developed by StabilityAI.
- StableLM is excited to be able to help the user, but will refuse to do anything that could be considered harmful to the user.
- StableLM is more than just an information source, StableLM is also able to write poetry, short stories, and make jokes.
- StableLM will refuse to participate in anything that could harm a human.
"""      
      prompts = system_prompt
      prompts += f"<|USER|>{ping}<|ASSISTANT|>"
      return prompts

    return None

  def build_prompts(self, from_idx: int=0, to_idx: int=-1, fmt: PromptFmt=StableLMPromptFmt, truncate_size: int=None):
    if to_idx == -1 or to_idx >= len(self.pingpongs):
      to_idx = len(self.pingpongs)

    results = ""

    for idx, pingpong in enumerate(self.pingpongs[from_idx:to_idx]):
      results += fmt.prompt(pingpong, truncate_size=truncate_size)

    return results