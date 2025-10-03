from random import choices, choice, random
import json

def load_json(file_path):
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
    def __init__(self, gacha_banner='standard_themed_banner', patch = 'glb_through_the_tide_home_integrated'):
        self.pity_count = 0
        self.five_star_pity_count = 0  # five-star pity is 10 for all base banners
        self.acquire_construct = False
        self.bc = 0
        self.pulls = 0
        self.spoils = []

        self.gacha_banner = gacha_banner
        self.gacha_banner_json = f'data/banners/{gacha_banner}.json'

        self.patch = patch
        self.patch_json = f'data/patches/{patch}.json'

        # load frames and cubs for updating
        self.s_ranks = load_json("data/category_rates/s_rank_omniframe.json")
        self.uniframes = load_json("data/category_rates/uniframe.json")
        self.a_ranks = load_json("data/category_rates/a_b_rank_omniframe.json")
        self.six_star_weapons = load_json("data/category_rates/six_star_weapon.json")
        self.five_star_weapons = load_json("data/category_rates/five_star_weapon.json")
        self.s_cubs = [i for i in load_json("data/category_rates/cub.json") if i.get("rarity") == 6]
        self.a_cubs = [i for i in load_json("data/category_rates/cub.json") if i.get("rarity") == 5]

        # update banner type and patch if applicable
        self.category_rates, self.pity = load_banner(self.gacha_banner_json)
        self.has_five_star_pity = True if check_five_star_pity(self.gacha_banner_json) else False
        self.has_five_star_target = False
        self.has_six_star_target = False

        self.category_files = {
            "S-Rank Omniframe": self.s_ranks,
            "A, B-Rank Omniframe": self.a_ranks,
            "Construct Shard": "data/category_rates/construct_shard.json",
            "4-star Equipment": "data/category_rates/four_star_equipment.json",
            "Overclock Material": "data/category_rates/overclock_material.json",
            "EXP Material": "data/category_rates/exp_material.json",
            "Cog Box": "data/category_rates/cog_box.json",

            "S-Rank Uniframe" : self.uniframes,

            "S-Rank CUB" : self.s_cubs,
            "A-Rank CUB" : self.a_cubs,
            "CUB EXP Material" : "data/category_rates/cub_exp_material.json",
            "CUB Overclock Material" : "data/category_rates/cub_overclock_material.json",
            "Support Skill Component": "data/category_rates/support_skill_component.json",
            "CUB Shard" : "data/category_rates/cub_shard.json",

            "6-star Weapon" : self.six_star_weapons,
            "5-star Weapon" : self.five_star_weapons,
            "4-star Weapon" : "data/category_rates/four_star_weapon.json",
            "3-star Weapon" : "data/category_rates/three_star_weapon.json"

        }

        self.targets = {
            "type" : "",
            5 : "",
            6 : ""
        }

    def update_patch(self, patch):
        # new patch information
        self.patch = patch
        self.patch_json = f'data/patches/{patch}.json'

        patch_info = load_json(self.patch_json)
        # reset
        self.s_ranks = load_json("data/category_rates/s_rank_omniframe.json")
        self.a_ranks = load_json("data/category_rates/a_b_rank_omniframe.json")
        self.s_cubs = [i for i in load_json("data/category_rates/cub.json") if i.get("rarity") == 6]
        self.six_star_weapons = load_json("data/category_rates/six_star_weapon.json")

        # apply patch
        s_construct_map = {c["name"]: c for c in self.s_ranks}
        a_construct_map = {c["name"]: c for c in self.a_ranks}
        s_cub_map = {c["name"]: c for c in self.s_cubs}
        for banner in patch_info["banners"]:
            unit_name = banner["unit"]
            if banner["name"] in ["Themed Banner", "Fate Themed Banner"]:
                unit = s_construct_map.get(unit_name)
                unit["banner"] = ["debut"]
            elif banner["name"] == "Base Member Target":
                a_patch_included = patch_info.get("a_rank_patch_included", 0)
                # A-rank patch debut/if integrated patch
                if (patch_info["patch_type"] == "A" and banner["rank"] == "A") or (patch_info["patch_type"] == "S" and a_patch_included and banner["rank"] == "A"):
                    unit = a_construct_map.get(unit_name)
                    unit["banner"] = ["debut"]
                # other (S-rank/A-rank added to banner)
                else:
                    unit = s_construct_map.get(unit_name) if banner["rank"] == "S" else a_construct_map.get(unit_name)
                    unit["banner"] = ["base"]
            elif "CUB Target" in banner["name"]:
                unit = s_cub_map.get(unit_name)
                # if debut patch with S-rank, 100%
                signature_unit = next(i for i in self.s_ranks if unit["unit"] in i["name"])
                if "debut" in signature_unit["banner"]:
                    unit["banner"] = ["debut"]
                else:
                    unit["banner"] = ["base"]
            elif "Target Weapon" in banner["name"]:
                weapon = { "name": banner["weapon"],
                           "unit" : banner["unit"],
                           "rarity": 6 ,
                           "img" : banner["img"],
                           "off-pity" : banner["off-pity"]}
                self.six_star_weapons.append(weapon)
        # update
        self.category_files["A, B-Rank Omniframe"].clear()
        self.category_files["A, B-Rank Omniframe"].extend(self.a_ranks)
        self.category_files["S-Rank Omniframe"].clear()
        self.category_files["S-Rank Omniframe"].extend(self.s_ranks)
        self.category_files["S-Rank CUB"].clear()
        self.category_files["S-Rank CUB"].extend(self.s_cubs)
        self.category_files["6-star Weapon"].clear()
        self.category_files["6-star Weapon"].extend(self.six_star_weapons)
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
        print(chosen_category_name)
        items = load_json(self.category_files[chosen_category_name])
        if chosen_category_name == "4-star Equipment":
            if "uniframe" in self.gacha_banner:
                items = [i for i in items if i.get("banner") == "uniframe"]
            else:
                items = [i for i in items if i.get("banner") == "base"]
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
            "debut" : "S-Rank Omniframe",
            "uniframe": "S-Rank Uniframe",
            "cub": "S-Rank CUB",
            "weapon" : "6-star Weapon"
        }
        key = types[type]

        items = self.category_files[key]
        # if it's the base banner and there's a check target
        if self.targets["type"] == 'unit':
            s_ranks = [i for i in items if "base" in i["banner"]]
            if self.has_six_star_target:
                return next(i for i in s_ranks if i["name"] == self.targets[6])
            non_target_s_ranks = [i for i in s_ranks if i["name"] != self.targets[6]]
            return choice(non_target_s_ranks)
        # if it's the uniframe banner (80%)
        if self.targets["type"] == 'uniframe':
            s_ranks = items
            if self.has_six_star_target:
                target_item = next((i for i in s_ranks if i["name"] == self.targets[6]), None)
                if target_item:
                    # probably should account for a debuting uniframe (but it's likely they won't release one lmao)
                    # otherwise, 80%
                    if random() < 0.8:
                        return target_item
                    else:
                        non_target_items = [i for i in s_ranks if i["name"] != self.targets[6]]
                        return choice(non_target_items)
        # if it's the cub banner and there's a target
        if self.targets["type"] == 'cub':
            if self.has_six_star_target:
                target_item = next((i for i in items if i["name"] == self.targets[6]), None)
                if target_item:
                    # if debut CUB, 100%
                    if "debut" in target_item["banner"]:
                        return target_item
                    # otherwise, 80%
                    if random() < 0.8:
                        return target_item
            non_target_s_ranks = [i for i in items if i["name"] != self.targets[6]]
            return choice(non_target_s_ranks)
        # if it's a weapon banner (80%)
        if self.targets["type"] == 'weapon':
            s_ranks = items
            if self.has_six_star_target:
                target_item = next((i for i in s_ranks if i["name"] == self.targets[6]), None)
                if random() < 0.8:
                    return target_item
                else:
                    non_target_items = [i for i in s_ranks if i["name"] in target_item["off-pity"]]
                    return choice(non_target_items)

        # if it's the debut banner - targets["type"] == "debut"
        s_ranks = [i for i in items if i["name"] == self.targets[6]]
        return choice(s_ranks)

    def _get_five_star(self, type="unit"):
        """
        get random five-star item
        :param type: unit, cub, weapon
        :return:
        """
        types = {
            "" : "A, B-Rank Omniframe",
            "debut": "A, B-Rank Omniframe", # because even with a debut S-rank A-rank should stay the same
            "unit" : "A, B-Rank Omniframe",
            "cub": "A-Rank CUB",
            "weapon" : "5-star Weapon"
        }
        key = types[type]

        items = self.category_files[key]
        # filter by rarity first
        five_star_items = [i for i in items if i.get("rarity") == 5]
        if any("rank" in i for i in five_star_items): # for the frames
            five_star_items = [i for i in five_star_items if (i.get("rank") == "A" and ("base" in i["banner"]) or "debut" in i["banner"])]
        if self.has_five_star_target:
            target_item = next((i for i in five_star_items if i["name"] == self.targets[5]), None)
            if target_item:
                # if debut A-rank, 100%
                if "debut" in target_item["banner"]:
                    return target_item
                # otherwise, 80%
                if random() < 0.8:
                    return target_item
        # pick random A-rank/non-targeted
        non_target_a_ranks = [i for i in five_star_items if i["name"] != self.targets[5]]
        return choice(non_target_a_ranks)
