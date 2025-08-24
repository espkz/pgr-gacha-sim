from random import choices, choice
import json

category_rates = [
    {"name": "S-Rank Omniframe", "rarity": 6, "rate": 0.005},
    {"name": "A, B-Rank Omniframe", "rarity": 5, "rate": 0.1395},
    {"name": "Construct Shard", "rarity": 4, "rate": 0.2211},
    {"name": "4★ Equipment", "rarity": 4, "rate": 0.2839},
    {"name": "EXP Material", "rarity": 4, "rate": 0.0481},
    {"name": "Cog Box", "rarity": 4, "rate": 0.1442}
]

def load_category(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

class Gacha:
    def __init__(self, **kwargs):
        self.pity = 0
        self.acquire_construct = False
        self.bc = 0
        self.pulls = 0
        self.spoils = []

        self.category_files = {
            "S-Rank Omniframe": "data/category_rates/s_rank_omniframe.json",
            "A, B-Rank Omniframe": "data/category_rates/a_b_rank_omniframe.json",
            "Construct Shard": "data/category_rates/construct_shard.json",
            "4★ Equipment": "data/category_rates/four_star_equipment.json",
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
            self.pity += 1
            self.pulls += 1
            self.bc += 250
            # Hard pity check
            if self.pity >= 60:
                # hit pity
                item = self._get_six_star()
                self.pity = 0
            else:
                item = self._get_random_item()
                # if you won
                if item["rarity"] == 6:
                    self.pity = 0
            results.append(item)
            self.spoils.append(item)
        return results

    def check_pity(self):
        # if 60 pity is reached
        if self.pity == 60:
            self.acquire_construct = True

    def _get_random_item(self):
        pool = [category for category in category_rates]
        weights = [category["rate"] for category in pool]
        chosen_category = choices(pool, weights=weights, k=1)[0]
        chosen_category_name = chosen_category["name"]
        items = load_category(self.category_files[chosen_category_name])
        return choice(items)

    def _get_six_star(self):
        items = load_category(self.category_files['S-Rank Omniframe'])
        return choice(items)
