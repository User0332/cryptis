import random
from cryptcommon import CommunicationChannel, xor_encrypt, xor_decrypt

PRIVKEY_MIN = 1

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

		ciphertext = xor_encrypt(message, self._shared_secret)
		channel.send("Message", ciphertext)

	def receive_message(self, channel: CommunicationChannel) -> str:
		assert self._shared_secret is not None, "No shared secret established!"

		ciphertext = channel.peek()[1] # non-validating
		message = xor_decrypt(ciphertext, self._shared_secret)

		return message