import binascii
import argparse
from bip_utils import Bip44, Bip44Coins, Bip44Changes
from mnemonic import Mnemonic

path = "data/5-characters/5-character-iteration-part-1.txt"

new_parser = argparse.ArgumentParser(description = "Create word list of combination a-z with number of character input.")

new_parser.add_argument("-a", "--address", help = "enter wallet address", type = int)

arguments = new_parser.parse_args()


mnemo = Mnemonic("english")
# Seed bytes
words = "winner equip edge stock junior kangaroo avocado wild escape never guide embody comfort slide account cycle hip unaware field view warfare toss soup small"
# seed_bytes = binascii.unhexlify(b"fbe985196b0792f303ffd84d12a19e2432e3970061b66bfd8d57f9ff71cb73fe")
seed = mnemo.to_seed(words,passphrase="hello")
# Create from seed
bip44_mst = Bip44.FromSeed(seed, Bip44Coins.BITCOIN)

# # Print master key in extended format
# print(bip44_mst.PrivateKey().ToExtended())
# # Print master key in hex format
# print(bip44_mst.PrivateKey().Raw().ToHex())

# # Print public key in extended format (default: Bip44PubKeyTypes.EXT_KEY)
# print(bip44_mst.PublicKey())
# # Print public key in raw uncompressed format
# print(bip44_mst.PublicKey().RawUncompressed().ToHex())
# # Print public key in raw compressed format
# print(bip44_mst.PublicKey().RawCompressed().ToHex())

# # Print the master key in WIF
# print(bip44_mst.PrivateKey().ToWif())

# Derive account 0 for Bitcoin: m/44'/0'/0'
bip44_acc = bip44_mst.Purpose().Coin().Account(0)
# Print keys in extended format
# print(bip44_acc.PrivateKey().ToExtended())
# print(bip44_acc.PublicKey().ToExtended())

# Derive the external chain: m/44'/0'/0'/0
bip44_change = bip44_acc.Change(Bip44Changes.CHAIN_EXT)
# Print again keys in extended format
# print(bip44_change.PrivateKey().ToExtended())
# print(bip44_change.PublicKey().ToExtended())

# Derive the first 20 addresses of the external chain: m/44'/0'/0'/0/i
for i in range(20):
    bip44_addr = bip44_change.AddressIndex(i)
    # Print extended keys and address
    # print(bip44_addr.PrivateKey().ToExtended())
    # print(bip44_addr.PublicKey().ToExtended())
    print(bip44_addr.PublicKey().ToAddress())