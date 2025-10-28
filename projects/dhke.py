# Demonstration of the Diffie-Hellman Key Exchange

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
		self.pub: int = (g^self._priv) % p
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

		self._shared_secret = (self.foreign_pub^self._priv) % self.p

	def send_message(self, message: str, channel: CommunicationChannel):
		assert self._shared_secret is not None, "No shared secret established!"

		ciphertext = encrypt(message, self._shared_secret)
		channel.send("Message", ciphertext)

	def receive_message(self, channel: CommunicationChannel) -> str:
		assert self._shared_secret is not None, "No shared secret established!"

		ciphertext = channel.peek()[1] # non-validating
		message = decrypt(ciphertext, self._shared_secret)

		return message

	
p = 104729
g = random.randint(2, p//2) # use p//2 to avoid a large shared secret 
default = CommunicationChannel()

default.send("g", g)
default.send("p", p)

alice = Agent("Alice", g, p)
bob = Agent("Bob", g, p)

alice.send_pubkey(default)
bob.receive_pubkey(default)

bob.send_pubkey(default)
alice.receive_pubkey(default)

alice.compute_shared_secret()
bob.compute_shared_secret()

alice.send_message("top secret white house gc message", default)

print(f"{bob.name} received {bob.receive_message(default)!r} from {alice.name}")
print(f"{alice.name} computed the shared secret: {alice._shared_secret}")
print(f"{bob.name} computed the shared secret: {bob._shared_secret}")

print(f"\n\nPublic info available:\n{default}\n\n")

known_pub = default.get_first(f"Public Key of {alice.name}")
other_known_pub = default.get_first(f"Public Key of {bob.name}")
print(f"Eve will now attempt to compute the shared secret given g={g}, p={p}, {alice.name}_pub={known_pub}, {bob.name}_pub={other_known_pub}")

print(f"Eve must solve s ≡ A^b (mod p). She knows A & p, so she must compute b via g^b ≡ B (mod p) [the DLP]. Since the private keys are bounded by [{PRIVKEY_MIN}, {p}], this can be trivially brute-forced.")

# doesn't a secure system require super large private keys?! even with PRIVKEY_MAX = 10^6 this is broken by PYTHON in milliseconds....
# also is there a way to quickly compute exp mod p because wouldn't these large private keys make stuff really slow
# and there should also be a higher min on private keys, right? but if privkey bounds were known then a key close to privkey min would be quickly found by naive iter...
# wait this is an O(n) problem... that's not hard... right?

for b in range(PRIVKEY_MIN, p + 1):
	if ((g^b) % p) == other_known_pub:
		print(f"Eve has cracked {bob.name}'s private key: {b}, {bob.name}'s actual private key is {bob._priv} [from a divine revelation]")
		break
else:
	raise ValueError("wait... this is impossible...") # ok, I realized the bug; this doesn't happen anymore because I forgot that modulo has higher operator precedence than xor so my public key and and shared secrets were actually not guaranteed to be mod p

s = (known_pub^b) % p

print(f"Eve has now successfully computed the shared secret {s}.")

message = default.get_first("Message")

print(f"Eve has decrypted the message {message!r} -> {decrypt(message, s)!r}")