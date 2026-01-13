# Demonstration of the Diffie-Hellman Key Exchange

from cryptcommon import CommunicationChannel, xor_decrypt
from dhke_common import Agent, PRIVKEY_MIN
from pohlig_hellman import pohlig_hellman
from babystep_giantstep import babystep_giantstep
import random

	
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
	if pow(g, b, p) == other_known_pub:
		print(f"Eve has cracked {bob.name}'s private key: {b}, {bob.name}'s actual private key is {bob._priv} [from a divine revelation]")
		break
else:
	raise ValueError("wait... this is impossible...") # ok, I realized the bug; this doesn't happen anymore because I forgot that modulo has higher operator precedence than xor so my public key and and shared secrets were actually not guaranteed to be mod p

s = pow(known_pub, b, p)

print(f"Eve has now successfully computed the shared secret {s}.")

message = default.get_first("Message")

print(f"Eve has decrypted the message {message!r} -> {xor_decrypt(message, s)!r}")


print("Attempting to crack the privkey with baby-step giant-step:")

N = p - 1 # worst possible case

privkey = babystep_giantstep(p, g, other_known_pub)

print(f"Eve has cracked the private key using babystep-giantstep: {privkey}")

s = pow(known_pub, privkey, p)

print(f"Eve has now successfully computed the shared secret {s}.")



print("Attempting to crack the privkey with pohlig-hellman X babystep-giantstep:")

privkey = pohlig_hellman(p, g, other_known_pub)

print(f"Eve has cracked the private key using pohlig-hellman X babystep-giantstep: {privkey}")

s = pow(known_pub, privkey, p)

print(f"Eve has now successfully computed the shared secret {s}.")


# note that we might get different solns for each result (real privkey, brute force, babystep-giantstep, pohlig-hellman) but the same shared secret
# because two exponents might be congruent mod p-1