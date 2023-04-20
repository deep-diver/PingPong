from pingpong.pingpong import PromptFmt, UIFmt
from pingpong.alpaca import AlpacaChatPPManager
from pingpong.dolly import DollyChatPPManager
from pingpong.stablelm import StableLMChatPPManager

class GradioChatUIFmt(UIFmt):
  @classmethod
  def ui(cls, pingpong):
    return (pingpong.ping, pingpong.pong)

class GradioAlpacaChatPPManager(AlpacaChatPPManager):
  def build_uis(self, from_idx: int=0, to_idx: int=-1, fmt: UIFmt=GradioChatUIFmt):
    if to_idx == -1 or to_idx >= len(self.pingpongs):
      to_idx = len(self.pingpongs)

    results = []

    for pingpong in self.pingpongs[from_idx:to_idx]:
      results.append(fmt.ui(pingpong))

    return results

class GradioDollyChatPPManager(DollyChatPPManager):
  def build_uis(self, from_idx: int=0, to_idx: int=-1, fmt: UIFmt=GradioChatUIFmt):
    if to_idx == -1 or to_idx >= len(self.pingpongs):
      to_idx = len(self.pingpongs)

    results = []

    for pingpong in self.pingpongs[from_idx:to_idx]:
      results.append(fmt.ui(pingpong))

    return results

class GradioStableLMChatPPManager(StableLMChatPPManager):
    def build_uis(self, from_idx: int=0, to_idx: int=-1, fmt: UIFmt=GradioChatUIFmt):
      if to_idx == -1 or to_idx >= len(self.pingpongs):
        to_idx = len(self.pingpongs)

      results = []

      for pingpong in self.pingpongs[from_idx:to_idx]:
        results.append(fmt.ui(pingpong))

      return results
