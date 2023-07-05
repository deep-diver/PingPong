from pingpong.pingpong import PPManager
from pingpong.pingpong import PromptFmt
from pingpong.utils import build_prompts

class KULLMPromptFmt(PromptFmt):
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
		pong = "" if pingpong.pong is None else pingpong.pong[:truncate_size]
		return f"""### 명령어:
{ping}
### 응답:
{pong}
"""
  
class KULLMChatPPManager(PPManager):
	def build_prompts(self, from_idx: int=0, to_idx: int=-1, fmt: PromptFmt=KULLMPromptFmt, truncate_size: int=None):
		return build_prompts(self, from_idx, to_idx, fmt, truncate_size)