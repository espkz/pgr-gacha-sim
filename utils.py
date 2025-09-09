from random import choices, choice, random
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

def check_five_star_pity(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    return data["has_five_star_pity"]


class Gacha:
    def __init__(self, gacha_banner='standard_themed_banner'):
        self.pity_count = 0
        self.five_star_pity_count = 0  # five-star pity is 10 for all base banners
        self.acquire_construct = False
        self.bc = 0
        self.pulls = 0
        self.spoils = []

        self.gacha_banner = gacha_banner
        self.gacha_banner_json = f'data/banners/{gacha_banner}.json'

        self.category_rates, self.pity = load_banner(self.gacha_banner_json)
        self.has_five_star_pity = True if check_five_star_pity(self.gacha_banner_json) else False
        self.has_five_star_target = False
        self.has_six_star_target = False


        self.category_files = {
            "S-Rank Omniframe": "data/category_rates/s_rank_omniframe.json",
            "A, B-Rank Omniframe": "data/category_rates/a_b_rank_omniframe.json",
            "Construct Shard": "data/category_rates/construct_shard.json",
            "4-star Equipment": "data/category_rates/four_star_equipment.json",
            "EXP Material": "data/category_rates/exp_material.json",
            "Cog Box": "data/category_rates/cog_box.json",

            "S-Rank CUB" : "data/category_rates/cub.json",
            "A-Rank CUB" : "data/category_rates/cub.json",
            "CUB EXP Material" : "data/category_rates/cub_exp_material.json",
        }

        self.targeted_units = {
            5 : "",
            6 : ""
        }


    # update target
    def change_target(self, rarity = 5, name = ""):
        self.targeted_units[rarity] = name
        # update if target is there or not
        if rarity == 5:
            self.has_five_star_target = True if name != "" else False
        else:
            self.has_six_star_target = True if name != "" else False

    def single_pull(self):
        return self._pull(count=1)

    def ten_pull(self):
        return self._pull(count=10)

    def _pull(self, count: int):
        results = []
        for _ in range(count):
            self.pity_count += 1
            self.five_star_pity_count += 1

            self.pulls += 1
            self.bc += 250
            # Hard pity check
            if self.pity_count >= self.pity:
                # hit pity
                item = self._get_six_star()
                self.pity_count = 0
            # for five-star pity (base)
            elif self.has_five_star_pity and self.five_star_pity_count >= 10:
                item = self._get_five_star()
                self.five_star_pity_count = 0
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
        # account for base/target banners
        if chosen_category_name == "A, B-Rank Omniframe":
            return self._get_five_star()
        elif chosen_category_name == "S-Rank Omniframe":
            return self._get_six_star()

        items = load_category(self.category_files[chosen_category_name])
        return choice(items)

    def _get_six_star(self):
        items = load_category(self.category_files['S-Rank Omniframe'])
        # if it's the base banner and there's a check target
        if self.gacha_banner == 'member_target_banner':
            s_ranks = [i for i in items if "base" in i["banner"]]
            if self.has_six_star_target:
                return next(i for i in s_ranks if i["name"] == self.targeted_units[6])
            non_target_s_ranks = [i for i in s_ranks if i["name"] != self.targeted_units[6]]
            return choice(non_target_s_ranks)
        # if it's the debut banner
        s_ranks = [i for i in items if "debut" in i["banner"]]
        return choice(s_ranks)

    def _get_five_star(self):
        # currently using for A-ranks from base banner
        items = load_category(self.category_files["A, B-Rank Omniframe"])
        a_ranks = [i for i in items if i["rank"] == "A"]
        if self.has_five_star_target and random() < 0.8:
            return next(i for i in a_ranks if i["name"] == self.targeted_units[5])
        non_target_a_ranks = [i for i in a_ranks if i["name"] != self.targeted_units[5]]
        return choice(non_target_a_ranks)
