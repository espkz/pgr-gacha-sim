from app.core.gacha import Gacha

class GachaService:

    def __init__(self):
        self.gacha_instances = {}

    def pull(self, patch: str, banner: str, times: int):

        key = f"{patch}_{banner}"

        if key not in self.gacha_instances:
            self.gacha_instances[key] = Gacha(
                patch=patch,
                gacha_banner=banner
            )

        gacha = self.gacha_instances[key]

        results = gacha._pull(times)

        return {
            "banner": banner,
            "results": results
        }