import cryptcommon

class PublisherAgent:
	def __init__(self, name: str):
		self.name = name
		
		self.e = 65537 # just use static exp
		
		# ensure e is coprime to (p-1)(q-1)
		while 1:
			self.p = cryptcommon.generate_prime()
			self.q = cryptcommon.generate_prime()

			if cryptcommon.gcd(self.e, (self.p-1)*(self.q-1)) == 1: break


		self.N = self.p*self.q

	def publish_pubkey(self, channel: cryptcommon.CommunicationChannel):
		channel.send("pubkey", (self.N, self.e))

	def receive_message(self, channel: cryptcommon.CommunicationChannel):
		ciphertext = channel.get_first("message")

		message = cryptcommon.exp_decrypt(ciphertext, self.e, self.p, self.q)

		return message
	
class SenderAgent:
	def __init__(self, name: str):
		self.name = name

	def receive_pubkey(self, channel: cryptcommon.CommunicationChannel):
		self.N, self.e = channel.get_first("pubkey")

	def send_message(self, message: str, channel: cryptcommon.CommunicationChannel):
		ciphertext = cryptcommon.exp_encrypt(message, self.e, self.N)

		channel.send("message", ciphertext)

default = cryptcommon.CommunicationChannel()

alice = SenderAgent("Alice")
bob = PublisherAgent("Bob")

bob.publish_pubkey(default)
alice.receive_pubkey(default)

sent_msg = "👋 i really hope utf-8 doesn't break this..."

alice.send_message(sent_msg, default)

received_msg = bob.receive_message(default)

print(f"{alice.name} sent: {sent_msg!r}. "
	  f"Eve saw: {cryptcommon.integer_to_str(default.get_first('message'))!r}. "
	  f"{bob.name} received: {received_msg!r}.")

if sent_msg == received_msg:
	print("The exchange worked!")
else:
	print("Something went wrong...")
	exit(1)