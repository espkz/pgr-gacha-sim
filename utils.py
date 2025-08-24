

class gacha:
    def __init__(self, **kwargs):
        self.pity = 0
        self.acquire_construct = False
        self.bc = 0

    def single_pull(self):
        self.pity += 1
        self.bc += 250
        return 0

    def ten_pull(self):
        self.pity += 10
        self.bc += 2500
        return 0

    def check_pity(self):
        # if 60 pity is reached
        if self.pity == 60:
            self.acquire_construct = True
