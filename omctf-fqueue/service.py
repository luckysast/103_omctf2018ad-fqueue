import redis
from models import *
from crypto import cipher
from keygenerator import generate_key
import time
import datetime
import base64
import operator


class Service:
    def __init__(self):
        self.db = redis.StrictRedis(host='omctf-redis', port=6379, db=0, charset='utf-8', decode_responses=True)

    def add_new_claim(self, claim):
        claim_id = self.db.incr("claim_id")
        key = generate_key()
        timestamp = time.mktime(datetime.datetime.today().timetuple())
        plaintext = 'team=' + claim.team + 'flag=' + claim.flag + 'timestamp=' + str(timestamp)
        cipher_text = cipher.encrypt(plaintext, key)

        mapping = {'claim_id': claim_id, 'cipher_text': cipher_text}
        self.db.hmset('claim:' + str(claim_id), mapping)
        self.db.hmset('key:' + str(claim_id), {'text': key})

        cipher_claim = CipherClaim(claim_id, base64.b64encode(cipher_text.encode('utf-8')).decode('utf-8'), key)
        return cipher_claim

    def get_recent(self):
        keys = self.db.keys('claim:*')
        recent_list = []

        for key in keys:
            claim = self.db.hmget(key, 'claim_id', 'cipher_text')
            claim[0] = int(claim[0])
            claim[1] = base64.b64encode(claim[1].encode('utf-8')).decode('utf-8')
            recent_list.append(claim)

        recent_list.sort(key=operator.itemgetter(0))
        recent_list = list(reversed(recent_list))
        if len(recent_list) <= 150:
            return recent_list
        else:
            return recent_list[-150:]
            

    def get_cipher_claim_by_id(self, claim_id):
        cipher_text = self.db.hget('claim:' + str(claim_id), 'cipher_text')
        cipher_claim = {'id': claim_id, 'cipher_text': base64.b64encode(cipher_text.encode('utf-8')).decode('utf-8')}
        return cipher_claim

    def decrypt_claim(self, cipher_text, key):
        decoded = base64.b64decode(cipher_text)
        decoded = decoded.decode('utf-8')
        return cipher.decrypt(decoded, key)

