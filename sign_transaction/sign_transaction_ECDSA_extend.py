import eth_keys, os
import json

# Generate the private + public key pair (using the secp256k1 curve)
signerPrivKey = eth_keys.keys.PrivateKey(os.urandom(32))
signerPubKey = signerPrivKey.public_key
print('Private key (64 hex digits):', signerPrivKey)
print('Public key (uncompressed, 128 hex digits):', signerPubKey)

# JSON message to be signed
msg_dict = {
    "from": "0x937CDc3a7273269Fe43967E785D9e24D3C48C164",
    "gas": "0x3d0900",
    "gasPrice": 10000000000,
    "hash": "0x228c53215e5ad0f9d6114a4f4adeb8e5359fbee1283aacb7fedb2ab1b212871b",
    "data": "0x60fe47b10000000000000000000000000000000000000000000000000000000000000003",
    "nonce": 34,
    "to": "0x6b4A7a46ad065b5fb142DEe92E9F4546982510fD",
    "value": "0x"
}

# Convert JSON message to string then encode to bytes
msg_str = json.dumps(msg_dict)
msg = msg_str.encode('utf-8')

# ECDSA sign message (using the curve secp256k1 + Keccak-256)
signature = signerPrivKey.sign_msg(msg)
print('Message:', msg)
print('Signature: [r = {0}, s = {1}, v = {2}]'.format(
    hex(signature.r), hex(signature.s), hex(signature.v)))

# ECDSA public key recovery from signature + verify signature
recoveredPubKey = signature.recover_public_key_from_msg(msg)
print('Recovered public key (128 hex digits):', recoveredPubKey)
print('Public key correct?', recoveredPubKey == signerPubKey)
valid = signerPubKey.verify_msg(msg, signature)
print("Signature valid?", valid)
