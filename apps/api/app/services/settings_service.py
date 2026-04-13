from packages.profile.loader import load_operator_config


class SettingsService:
    def get_snapshot(self) -> dict:
        return load_operator_config()
