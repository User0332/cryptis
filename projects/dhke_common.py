import random
from xorcrypt import encrypt, decrypt

PRIVKEY_MIN = 1

class CommunicationChannel:
	def __init__(self):
		self._messages: list[str | bytes | int] = []

	def send(self, label: str, message: str | bytes | int):
		self._messages.append((label, message))

	def peek(self) -> tuple[str, str | bytes | int]:
		return self._messages[-1]
	
	def get_first(self, label: str) -> str | bytes | int | None:
		for msg in self._messages:
			if msg[0] == label: return msg[1]

		return None
	
	def __str__(self):
		return "\n".join(f"{label}: {message}" for label, message in self._messages)

class Agent:
	def __init__(self, name: str, g: int, p: int):
		self.name = name
		self._priv = random.randint(PRIVKEY_MIN, p)
		self.pub: int = pow(g, self._priv, p)
		self._shared_secret: int = None
		self.foreign_pub: int = None
		self.g = g
		self.p = p

	def send_pubkey(self, channel: CommunicationChannel):
		channel.send(f"Public Key of {self.name}", self.pub)

	def receive_pubkey(self, channel: CommunicationChannel):
		self.foreign_pub = channel.peek()[1] # non-validating

	def compute_shared_secret(self):
		assert self.foreign_pub is not None, "No connection established!"

		self._shared_secret = pow(self.foreign_pub, self._priv, self.p)

	def send_message(self, message: str, channel: CommunicationChannel):
		assert self._shared_secret is not None, "No shared secret established!"

		ciphertext = encrypt(message, self._shared_secret)
		channel.send("Message", ciphertext)

	def receive_message(self, channel: CommunicationChannel) -> str:
		assert self._shared_secret is not None, "No shared secret established!"

		ciphertext = channel.peek()[1] # non-validating
		message = decrypt(ciphertext, self._shared_secret)

		return message