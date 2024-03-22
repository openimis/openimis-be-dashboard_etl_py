from django.core.cache import cache


class ETLProgress:
    def __init__(self, indicator) -> None:
        self.indicator = indicator
        self.stage = "Not Started"
        self.cache_key = f"{indicator}_progress"

    def update_stage(self, new_stage):
        self.stage = new_stage
        cache.set(self.cache_key, new_stage)

    def get_stage(self):
        return cache.get(self.cache_key, "Not Started")
