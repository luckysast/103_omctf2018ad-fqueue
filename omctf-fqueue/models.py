class Claim:
    def __init__(self, flag, team):
        self.flag = flag
        self.team = team


class CipherClaim:
    def __init__(self, claim_id, cipher_text, key):
        self.id = claim_id
        self.cipher_text = cipher_text
        self.key = key
