from pathlib import Path

class DotSettings:
    ...
    def __init__(self, dot_settings: Path):
        self.dot_settings = dot_settings

    @staticmethod
    def create(dot_settings: Path) -> 'DotSettings':
        return DotSettings(dot_settings)