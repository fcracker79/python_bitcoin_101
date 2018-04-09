import bitcoin


def _mnemonic_to_seed(mnemonic_phrase, passphrase=b''):
    try:
        from hashlib import pbkdf2_hmac
        def pbkdf2_hmac_sha256(password, salt, iters=2048):
            return pbkdf2_hmac(hash_name='sha512', password=password, salt=salt, iterations=iters)
    except:
        try:
            from Crypto.Protocol.KDF import PBKDF2
            from Crypto.Hash import SHA512, HMAC

            def pbkdf2_hmac_sha256(password, salt, iters=2048):
                return PBKDF2(password=password, salt=salt, dkLen=64, count=iters,
                              prf=lambda p, s: HMAC.new(p, s, SHA512).digest())
        except:
            try:

                from pbkdf2 import PBKDF2
                import hmac
                def pbkdf2_hmac_sha256(password, salt, iters=2048):
                    return PBKDF2(password, salt, iterations=iters, macmodule=hmac, digestmodule=hashlib.sha512).read(
                        64)
            except:
                raise RuntimeError("No implementation of pbkdf2 was found!")

    return pbkdf2_hmac_sha256(password=mnemonic_phrase, salt=b'mnemonic' + passphrase)


def _derived_key(master_key: str, *path: int) -> str:
    k = master_key
    for p in path:
        k = bitcoin.bip32_ckd(k, p)
    return k


def _derive_and_print(master_key: str, *path: int, derive_pub_key: bool=True):
    master_pub_key = _derived_key(bitcoin.bip32_privtopub(master_key))
    derived_key = _derived_key(master_key, *path)
    if derive_pub_key:
        derived_pub_key = _derived_key(master_pub_key, *path)
    else:
        derived_pub_key = 'N.A.'
    derived_pub_key_from_key = bitcoin.bip32_privtopub(derived_key)
    print(
        '''Derivation path: {},
        Derived key: {},
        Derived public key: {},
        Derived public key from private: {}
    '''.format(
            master_key,
            ', '.join(str(x) if x <= 2**31 else str(x - 2**31) + '\'' for x in path),
            derived_key, derived_pub_key, derived_pub_key_from_key))


def _print_master_key_and_derived(vbytes: bytes):
    seed = _mnemonic_to_seed(b'This is a very funny mnemonic')
    master_key = bitcoin.bip32_master_key(seed, vbytes=vbytes)
    print('Master key:', master_key)
    _derive_and_print(master_key, 1, 2, 3)
    _derive_and_print(master_key, 1 + 2 ** 31, 2, 3, derive_pub_key=False)


if __name__ == '__main__':
    print('\nMAINNET\n')
    _print_master_key_and_derived(bitcoin.MAINNET_PRIVATE)
    print('\nTESTNET\n')
    _print_master_key_and_derived(bitcoin.TESTNET_PRIVATE)
