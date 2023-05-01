from django.test import TestCase
from .models import ValidAddress
from .addresses_generator import *
PRIVKEY_HEX = "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"



class UtilsTestCase(TestCase):
    def test_generate_public_key(self):

        # Test that generate_public_key returns a 32-byte hash value as expected
        private_key = bytes.fromhex(PRIVKEY_HEX)
        public_key = generate_public_key(private_key, ValidAddress)
        self.assertEqual(len(public_key), 32)

        # Test that generate_public_key generates a unique public key for each call when the model already has a public key
        existing_public_key = hashlib.sha256().digest()
        ValidAddress.objects.create(public_key=str(existing_public_key))
        new_public_key = generate_public_key(private_key, ValidAddress)
        self.assertNotEqual(existing_public_key, new_public_key)

    def test_generate_address_for_currency(self):
        # Test that generate_address_for_currency returns a Bitcoin address when given a valid public key and currency "BTC"
        private_key = bytes.fromhex(PRIVKEY_HEX)
        public_key = hashlib.sha256(private_key).digest()
        address = generate_address_for_currency(public_key, "BTC")
        self.assertTrue(bitcoin.is_address(address))

        # Test that generate_address_for_currency returns an Ethereum address when given a valid public key and currency "ETH"
        public_key = hashlib.sha3_256(private_key).digest()[-20:]
        address = generate_address_for_currency(public_key, "ETH")
        self.assertTrue(address.startswith("0x") and len(address) == 42)

        # Test that generate_address_for_currency returns False when given an invalid or unsupported currency
        public_key = hashlib.sha256(private_key).digest()
        self.assertFalse(generate_address_for_currency(public_key, "XYZ"))

    def test_generate_public_key_and_generate_address_for_currency(self):
        # Test that generate_public_key and generate_address_for_currency work together to generate a valid Bitcoin address
        private_key = bytes.fromhex(PRIVKEY_HEX)
        public_key = generate_public_key(private_key, ValidAddress)
        address = generate_address_for_currency(public_key, "BTC")
        self.assertTrue(bitcoin.is_address(address))

        # Test that generate_public_key and generate_address_for_currency work together to generate a valid Ethereum address
        private_key = private_key
        public_key = generate_public_key(private_key, ValidAddress)
        address = generate_address_for_currency(public_key, "ETH")
        self.assertTrue(address.startswith("0x") and len(address) == 42)

    def test_generate_public_key_and_generate_address_for_currency_handles_unexpected_inputs(self):
        # Test that generate_public_key and generate_address_for_currency handle unexpected inputs gracefully
        private_key = bytes.fromhex(PRIVKEY_HEX)
        self.assertFalse(generate_public_key(None, ValidAddress))
        self.assertFalse(generate_address_for_currency(None, "BTC"))
        self.assertFalse(generate_address_for_currency(hashlib.sha256(private_key).digest(), ""))
