from random import choices, choice
import json

def load_category(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def load_banner(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    rates = data["rates"]
    pity = data["pity"]
    return rates, pity

class Gacha:
    def __init__(self, gacha_banner='standard_themed_banner'):
        self.pity_count = 0
        self.acquire_construct = False
        self.bc = 0
        self.pulls = 0
        self.spoils = []
        self.gacha_banner = gacha_banner

        self.category_rates, self.pity = load_banner(f'data/banners/{gacha_banner}.json')

        self.category_files = {
            "S-Rank Omniframe": "data/category_rates/s_rank_omniframe.json",
            "A, B-Rank Omniframe": "data/category_rates/a_b_rank_omniframe.json",
            "Construct Shard": "data/category_rates/construct_shard.json",
            "4-star Equipment": "data/category_rates/four_star_equipment.json",
            "EXP Material": "data/category_rates/exp_material.json",
            "Cog Box": "data/category_rates/cog_box.json"
        }

    def single_pull(self):
        return self._pull(count=1)

    def ten_pull(self):
        return self._pull(count=10)

    def _pull(self, count: int):
        results = []
        for _ in range(count):
            self.pity_count += 1
            self.pulls += 1
            self.bc += 250
            # Hard pity check
            if self.pity_count >= self.pity:
                # hit pity
                item = self._get_six_star()
                self.pity_count = 0
            else:
                item = self._get_random_item()
                # if you won
                if item["rarity"] == 6:
                    self.pity_count = 0
            results.append(item)
            self.spoils.append(item)
        return results

    def check_pity(self):
        # if 60 pity is reached
        if self.pity_count == self.pity:
            self.acquire_construct = True

    def _get_random_item(self):
        pool = [category for category in self.category_rates]
        weights = [category["rate"] for category in pool]
        chosen_category = choices(pool, weights=weights, k=1)[0]
        chosen_category_name = chosen_category["name"]
        items = load_category(self.category_files[chosen_category_name])
        return choice(items)

    def _get_six_star(self):
        items = load_category(self.category_files['S-Rank Omniframe'])
        return choice(items)
