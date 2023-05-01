import hashlib
import bitcoin


def generate_public_key(private_key, model):
    # generate valid public key not exist in databse
    if private_key:

        public_key = hashlib.sha256(private_key).digest()
        while model.objects.filter(public_key=str(public_key)).exists():
            public_key = hashlib.sha256(public_key).digest()
        return public_key
    else:
        return False


def generate_address_for_currency(public_key, currency):
    # generate address from public
    if public_key:
        if currency == 'BTC':
            address = bitcoin.pubkey_to_address(public_key)
            return address
        elif currency == 'ETH':
            address = '0x' + hashlib.sha3_256(public_key).digest()[-20:].hex()
            return address
        else:
            return False
    else:
        return False
