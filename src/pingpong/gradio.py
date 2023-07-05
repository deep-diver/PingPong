from pingpong.pingpong import PromptFmt, UIFmt
from pingpong.alpaca import AlpacaChatPPManager
from pingpong.koalpaca import KoAlpacaChatPPManager
from pingpong.dolly import DollyChatPPManager
from pingpong.stablelm import StableLMChatPPManager
from pingpong.flan import FlanAlpacaChatPPManager
from pingpong.os_stablelm import OSStableLMChatPPManager
from pingpong.vicuna import VicunaChatPPManager
from pingpong.stable_vicuna import StableVicunaChatPPManager
from pingpong.starchat import StarChatPPManager
from pingpong.mpt import MPTChatPPManager
from pingpong.redpajama import RedPajamaChatPPManager
from pingpong.baize import BaizeChatPPManager
from pingpong.xgen import XGenChatPPManager
from pingpong.orca_mini import OrcaMiniChatPPManager
from pingpong.guanaco import GuanacoChatPPManager
from pingpong.wizard_falcon import WizardFalconChatPPManager
from pingpong.kullm import KULLMChatPPManager

from pingpong.utils import gradio_build_uis

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

class GradioKoAlpacaChatPPManager(KoAlpacaChatPPManager):
  def build_uis(self, from_idx: int=0, to_idx: int=-1, fmt: UIFmt=GradioChatUIFmt):
    if to_idx == -1 or to_idx >= len(self.pingpongs):
      to_idx = len(self.pingpongs)

    results = []

    for pingpong in self.pingpongs[from_idx:to_idx]:
      results.append(fmt.ui(pingpong))

    return results

class GradioFlanAlpacaChatPPManager(FlanAlpacaChatPPManager):
  def build_uis(self, from_idx: int=0, to_idx: int=-1, fmt: UIFmt=GradioChatUIFmt):
    if to_idx == -1 or to_idx >= len(self.pingpongs):
      to_idx = len(self.pingpongs)

    results = []

    for pingpong in self.pingpongs[from_idx:to_idx]:
      results.append(fmt.ui(pingpong))

    return results

class GradioOSStableLMChatPPManager(OSStableLMChatPPManager):
  def build_uis(self, from_idx: int=0, to_idx: int=-1, fmt: UIFmt=GradioChatUIFmt):
    if to_idx == -1 or to_idx >= len(self.pingpongs):
      to_idx = len(self.pingpongs)

    results = []

    for pingpong in self.pingpongs[from_idx:to_idx]:
      results.append(fmt.ui(pingpong))

    return results

class GradioVicunaChatPPManager(VicunaChatPPManager):
  def build_uis(self, from_idx: int=0, to_idx: int=-1, fmt: UIFmt=GradioChatUIFmt):
    if to_idx == -1 or to_idx >= len(self.pingpongs):
      to_idx = len(self.pingpongs)

    results = []

    for pingpong in self.pingpongs[from_idx:to_idx]:
      results.append(fmt.ui(pingpong))

    return results
  
class GradioStableVicunaChatPPManager(StableVicunaChatPPManager):
  def build_uis(self, from_idx: int=0, to_idx: int=-1, fmt: UIFmt=GradioChatUIFmt):
    if to_idx == -1 or to_idx >= len(self.pingpongs):
      to_idx = len(self.pingpongs)

    results = []

    for pingpong in self.pingpongs[from_idx:to_idx]:
      results.append(fmt.ui(pingpong))

    return results  

class GradioStarChatPPManager(StarChatPPManager):
  def build_uis(self, from_idx: int=0, to_idx: int=-1, fmt: UIFmt=GradioChatUIFmt):
    if to_idx == -1 or to_idx >= len(self.pingpongs):
      to_idx = len(self.pingpongs)

    results = []

    for pingpong in self.pingpongs[from_idx:to_idx]:
      results.append(fmt.ui(pingpong))

    return results
  
class GradioMPTChatPPManager(MPTChatPPManager):
  def build_uis(self, from_idx: int=0, to_idx: int=-1, fmt: UIFmt=GradioChatUIFmt):
    if to_idx == -1 or to_idx >= len(self.pingpongs):
      to_idx = len(self.pingpongs)

    results = []

    for pingpong in self.pingpongs[from_idx:to_idx]:
      results.append(fmt.ui(pingpong))

    return results
  
class GradioRedPajamaChatPPManager(RedPajamaChatPPManager):
  def build_uis(self, from_idx: int=0, to_idx: int=-1, fmt: UIFmt=GradioChatUIFmt):
    if to_idx == -1 or to_idx >= len(self.pingpongs):
      to_idx = len(self.pingpongs)

    results = []

    for pingpong in self.pingpongs[from_idx:to_idx]:
      results.append(fmt.ui(pingpong))

    return results

class GradioBaizeChatPPManager(BaizeChatPPManager):
  def build_uis(self, from_idx: int=0, to_idx: int=-1, fmt: UIFmt=GradioChatUIFmt):
    if to_idx == -1 or to_idx >= len(self.pingpongs):
      to_idx = len(self.pingpongs)

    results = []

    for pingpong in self.pingpongs[from_idx:to_idx]:
      results.append(fmt.ui(pingpong))

    return results
  
class GradioXGenChatPPManager(XGenChatPPManager):
  def build_uis(self, from_idx: int=0, to_idx: int=-1, fmt: UIFmt=GradioChatUIFmt):
    return gradio_build_uis(self, from_idx, to_idx, fmt)
  
class GradioOrcaMiniChatPPManager(OrcaMiniChatPPManager):
  def build_uis(self, from_idx: int=0, to_idx: int=-1, fmt: UIFmt=GradioChatUIFmt):
    return gradio_build_uis(self, from_idx, to_idx, fmt)
  
class GradioGuanacoChatPPManager(GuanacoChatPPManager):
  def build_uis(self, from_idx: int=0, to_idx: int=-1, fmt: UIFmt=GradioChatUIFmt):
    return gradio_build_uis(self, from_idx, to_idx, fmt)
  
class GradioWizardChatPPManager(WizardFalconChatPPManager):
  def build_uis(self, from_idx: int=0, to_idx: int=-1, fmt: UIFmt=GradioChatUIFmt):
    return gradio_build_uis(self, from_idx, to_idx, fmt)
  
class GradioKULLMChatPPManager(KULLMChatPPManager):
  def build_uis(self, from_idx: int=0, to_idx: int=-1, fmt: UIFmt=GradioChatUIFmt):
    return gradio_build_uis(self, from_idx, to_idx, fmt)