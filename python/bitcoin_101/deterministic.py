import bitcoin
from hashlib import pbkdf2_hmac

from bitcoin_101 import bitprint


def _mnemonic_to_seed(mnemonic_phrase, passphrase=b''):
    return pbkdf2_hmac(hash_name='sha512', password=mnemonic_phrase, salt=b'mnemonic' + passphrase, iterations=2048)


def _derived_key(master_key: str, *path: int) -> str:
    k = master_key
    for p in path:
        k = bitcoin.bip32_ckd(k, p)
    return k


def _derive_and_print(master_key: str, *path: int, derive_pub_key: bool=True, magicbyte: int=0):
    master_pub_key = _derived_key(bitcoin.bip32_privtopub(master_key))
    derived_key = _derived_key(master_key, *path)
    if derive_pub_key:
        derived_bip32_pub_key = _derived_key(master_pub_key, *path)
        derived_pub_key = bitcoin.bip32_extract_key(derived_bip32_pub_key)
    else:
        derived_bip32_pub_key = derived_pub_key = 'N.A.'
    derived_pub_key_from_key = bitcoin.bip32_privtopub(derived_key)
    print(
        '''    Derivation path: ({}),
    Derived BIP32 key: {},
    Derived BIP32 public key: {},
    BIP32 public key from derived BIP32 private: {},
    Derived key: {},
    Derived public key: {},
    Public key from derived key: {},
    BTC address: {}
    '''
        .format(
            ', '.join(str(x) if x <= 2 ** 31 else str(x - 2 ** 31) + '\'' for x in path),
            derived_key, derived_bip32_pub_key, derived_pub_key_from_key,
            bitcoin.bip32_extract_key(derived_key),
            derived_pub_key,
            bitcoin.privtopub(bitcoin.bip32_extract_key(derived_key)),
            bitcoin.pubtoaddr(bitcoin.privtopub(bitcoin.bip32_extract_key(derived_key)), magicbyte=magicbyte)
        )
    )


def _print_master_key_and_derived(vbytes: bytes, magicbyte: int):
    seed = _mnemonic_to_seed(b'This is a very funny mnemonic')
    master_key = bitcoin.bip32_master_key(seed, vbytes=vbytes)
    bitprint('Master key:', master_key)
    _derive_and_print(master_key, 1, 2, 3, magicbyte=magicbyte)
    _derive_and_print(master_key, 1 + 2 ** 31, 2, 3, derive_pub_key=False, magicbyte=magicbyte)


if __name__ == '__main__':
    bitprint('\nMAINNET\n')
    _print_master_key_and_derived(bitcoin.MAINNET_PRIVATE, 0)
    bitprint('\nTESTNET\n')
    _print_master_key_and_derived(bitcoin.TESTNET_PRIVATE, 111)
