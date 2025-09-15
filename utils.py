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
            "CUB Overclock Material" : "data/category_rates/cub_overclock_material.json",
            "Support Skill Component": "data/category_rates/support_skill_component.json",
            "CUB Shard" : "data/category_rates/cub_shard.json",
        }

        self.targets = {
            "type" : "",
            5 : "",
            6 : ""
        }

    # update target
    def change_target(self, rarity = 5, name = ""):
        self.targets[rarity] = name
        # update if target is there or not
        if rarity == 5:
            self.has_five_star_target = True if name != "" else False
        else:
            self.has_six_star_target = True if name != "" else False

    def change_target_type(self, type="unit"):
        # unit or cub
        self.targets["type"] = type

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
                item = self._get_six_star(self.targets["type"])
                self.pity_count = 0
                self.five_star_pity_count = 0
            # for five-star pity (base/cub)
            elif self.has_five_star_pity and self.five_star_pity_count >= 10:
                item = self._get_five_star_or_higher()
                self.five_star_pity_count = 0
                # if you won
                if item["rarity"] == 6:
                    self.pity_count = 0
            else:
                item = self._get_random_item()
                # if you won
                if item["rarity"] == 5:
                    self.five_star_pity_count = 0
                if item["rarity"] == 6:
                    self.pity_count = 0
                    self.five_star_pity_count = 0
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
        chosen_category_rarity = chosen_category["rarity"]
        chosen_category_name = chosen_category["name"]
        # account for base/target banners
        if chosen_category_rarity == 5:
            return self._get_five_star(self.targets["type"])
        elif chosen_category_rarity == 6:
            return self._get_six_star(self.targets["type"])

        items = load_category(self.category_files[chosen_category_name])
        return choice(items)

    def _get_five_star_or_higher(self):
        five_star = next(c for c in self.category_rates if c["rarity"] == 5)
        six_star = next(c for c in self.category_rates if c["rarity"] == 6)

        # base rates for weighting
        total = five_star["rate"] + six_star["rate"]
        weights = [five_star["rate"] / total, six_star["rate"] / total]

        chosen = choices([five_star, six_star], weights=weights, k=1)[0]

        if chosen["rarity"] == 5:
            return self._get_five_star(self.targets["type"])
        else:
            return self._get_six_star(self.targets["type"])

    def _get_six_star(self, type = "unit"):
        """
        get random six-star item
        :param type: unit (empty is also unit), cub, weapon
        :return:
        """
        types = {
            "": "S-Rank Omniframe",
            "unit": "S-Rank Omniframe",
            "cub": "S-Rank CUB",
        }
        key = types[type]

        items = load_category(self.category_files[key])
        # if it's the base banner and there's a check target
        if self.targets["type"] == 'unit':
            s_ranks = [i for i in items if "base" in i["banner"]]
            if self.has_six_star_target:
                return next(i for i in s_ranks if i["name"] == self.targets[6])
            non_target_s_ranks = [i for i in s_ranks if i["name"] != self.targets[6]]
            return choice(non_target_s_ranks)
        # if it's the cub banner and there's a target
        if self.targets["type"] == 'cub':
            s_ranks = [i for i in items if i["rarity"] == 6]
            if self.has_six_star_target and random() < 0.8:
                return next(i for i in s_ranks if i["name"] == self.targets[6])
            non_target_s_ranks = [i for i in s_ranks if i["name"] != self.targets[6]]
            return choice(non_target_s_ranks)
        # if it's the debut banner
        s_ranks = [i for i in items if "debut" in i["banner"]]
        return choice(s_ranks)

    def _get_five_star(self, type="unit"):
        """
        get random five-star item
        :param type: unit, cub, weapon
        :return:
        """
        types = {
            "" : "A, B-Rank Omniframe",
            "unit" : "A, B-Rank Omniframe",
            "cub": "A-Rank CUB",
        }
        key = types[type]

        items = load_category(self.category_files[key])
        # filter by rarity first
        five_star_items = [i for i in items if i.get("rarity") == 5]
        if any("rank" in i for i in five_star_items): # for the frames
            five_star_items = [i for i in five_star_items if (i.get("rank") == "A" and "base" in i["banner"])]

        if self.has_five_star_target and random() < 0.8:
            return next(i for i in five_star_items if i["name"] == self.targets[5])
        non_target_a_ranks = [i for i in five_star_items if i["name"] != self.targets[5]]
        return choice(non_target_a_ranks)
