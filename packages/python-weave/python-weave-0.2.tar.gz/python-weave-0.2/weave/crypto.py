# Crypto implementation:
import logging
import base64
import json

from M2Crypto.EVP import Cipher, RSA, load_key_string
import M2Crypto.m2

from weave.PBKDF2 import PBKDF2
from weave import DEFAULT_PROTOCOL_VERSION

class WeaveCryptoContext(object):
    """Encapsulates the cryptographic context for a user and their
    collections."""

    def __init__(self, storageContext, passphrase,
                 version=DEFAULT_PROTOCOL_VERSION):
        self.ctx = storageContext
        self.passphrase = passphrase
        self.privateKey = None
        self.bulkKeys = {}

    def fetchPrivateKey(self):
        """Fetch the private key for the user and storage context
        provided to this object, and decrypt the private key
        by using my passphrase.  Store the private key in internal
        storage for later use."""

        # Retrieve encrypted private key from the server
        logging.debug("Fetching encrypted private key from server")
        privKeyObj = self.ctx.get_item("keys", "privkey")
        payload = json.loads(privKeyObj['payload'])
        self.privKeySalt = base64.decodestring(payload['salt'])
        self.privKeyIV = base64.decodestring(payload['iv'])
        self.pubKeyURI = payload['publicKeyUri']

        data64 = payload['keyData']
        encryptedKey = base64.decodestring(data64)

        # Now decrypt it by generating a key with the passphrase
        # and performing an AES-256-CBC decrypt.
        logging.debug("Decrypting encrypted private key")

        passKey = PBKDF2(self.passphrase, self.privKeySalt, iterations=4096).read(32)
        cipher = Cipher(alg='aes_256_cbc', key=passKey, iv=self.privKeyIV, op=0) # 0 is DEC
        cipher.set_padding(padding=1)
        v = cipher.update(encryptedKey)
        v = v + cipher.final()
        del cipher
        decryptedKey = v

        # Result is an NSS-wrapped key.
        # We have to do some manual ASN.1 parsing here, which is unfortunate.

        # 1. Make sure offset 22 is an OCTET tag; if this is not right, the decrypt
        # has gone off the rails.
        if ord(decryptedKey[22]) != 4:
            logging.debug("Binary layout of decrypted private key is incorrect; probably the passphrase was incorrect.")
            raise ValueError("Unable to decrypt key: wrong passphrase?")

        # 2. Get the length of the raw key, by interpreting the length bytes
        offset = 23
        rawKeyLength = ord(decryptedKey[offset])
        det = rawKeyLength & 0x80
        if det == 0: # 1-byte length
            offset += 1
            rawKeyLength = rawKeyLength & 0x7f
        else: # multi-byte length
            bytes = rawKeyLength & 0x7f
            offset += 1

            rawKeyLength = 0
            while bytes > 0:
                rawKeyLength *= 256
                rawKeyLength += ord(decryptedKey[offset])
                offset += 1
                bytes -= 1

        # 3. Sanity check
        if offset + rawKeyLength > len(decryptedKey):
            rawKeyLength = len(decryptedKey) - offset

        # 4. Extract actual key
        privateKey = decryptedKey[offset:offset+rawKeyLength]

        # And we're done.
        self.privateKey = privateKey
        logging.debug("Successfully decrypted private key")

    def fetchBulkKey(self, label):
        """Given a bulk key label, pull the key down from the network,
        and decrypt it using my private key.  Then store the key
        into self storage for later decrypt operations."""

        # Do we have the key already?
        if label in self.bulkKeys:
            return

        logging.debug("Fetching encrypted bulk key from %s" % label)

        # Note that we do not currently support any authentication model for bulk key
        # retrieval other than the usual weave username-password pair.  To support
        # distributed key models for the more advanced sharing scenarios, we will need
        # to revisit that.
        keyData = self.ctx.http_get(label)
        keyPayload = json.loads(keyData['payload'])

        keyRing = keyPayload['keyring']

        # In a future world where we have sharing, the keys of the keyring dictionary will
        # define public key domains for the symmetric bulk keys stored on the ring.
        # Right now, the first item is always the pubkey of a user, and we just grab the first value.

        # We should really make sure that the key we have here matches the private key
        # we're using to unwrap, or none of this makes sense.

        # Now, using the user's private key, we will unwrap the symmetric key.
        encryptedBulkKey = base64.decodestring(keyRing.items()[0][1]['wrapped'])

        # This is analogous to this openssl command-line invocation:
        # openssl rsautl -decrypt -keyform DER -inkey privkey.der -in wrapped_symkey.dat -out unwrapped_symkey.dat
        #
        # ... except that M2Crypto doesn't have an API for DER importing,
        # so we have to PEM-encode the key (with base64 and header/footer blocks).
        # So what we're actually doing is:
        #
        # openssl rsautl -decrypt -keyform PEM -inkey privkey.pem -in wrapped_symkey.dat -out unwrapped_symkey.dat

        logging.debug("Decrypting encrypted bulk key %s" % label)

        pemEncoded = "-----BEGIN RSA PRIVATE KEY-----\n"
        pemEncoded += base64.encodestring(self.privateKey)
        pemEncoded += "-----END RSA PRIVATE KEY-----\n"

        # Create an EVP, extract the RSA key from it, and do the decrypt
        evp = load_key_string(pemEncoded)
        rsa = M2Crypto.m2.pkey_get1_rsa(evp.pkey)
        rsaObj = RSA.RSA(rsa)
        unwrappedSymKey = rsaObj.private_decrypt(encryptedBulkKey, RSA.pkcs1_padding)

        # And save it for later use
        self.bulkKeys[label] = unwrappedSymKey
        logging.debug("Succesfully decrypted bulk key from %s" % label)

    def decrypt(self, encryptedObject):
        """Given an encrypted object, decrypt it and return the plaintext value.

        If necessary, will retrieve the private key and bulk encryption key
        from the storage context associated with self."""

        # Coerce JSON if necessary
        if isinstance(encryptedObject, basestring):
            encryptedObject = json.loads(encryptedObject)

        # An encrypted object has three relevant fields
        encryptionLabel = encryptedObject['encryption']
        ciphertext = base64.decodestring(encryptedObject['ciphertext'])
        iv = base64.decodestring(encryptedObject['IV'])

        # Go get the keying infromation if need it
        if self.privateKey is None:
            self.fetchPrivateKey()
        if not encryptionLabel in self.bulkKeys:
            self.fetchBulkKey(encryptionLabel)

        # In case you were wondering, this is the same as this operation at the openssl command line:
        # openssl enc -d -in data -aes-256-cbc -K `cat unwrapped_symkey.16` -iv `cat iv.16`

        # Do the decrypt
        logging.debug("Decrypting data record using bulk key %s" % encryptionLabel)
        cipher = Cipher(alg='aes_256_cbc', key=self.bulkKeys[encryptionLabel],
                        iv=iv, op=0) # 0 is DEC
        v = cipher.update(ciphertext)
        v = v + cipher.final()
        del cipher
        logging.debug("Successfully decrypted data record")
        return v

