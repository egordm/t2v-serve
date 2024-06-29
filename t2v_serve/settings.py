from pydantic_settings import BaseSettings, SettingsConfigDict


class SettingsSchema(BaseSettings):
    model_config = SettingsConfigDict(protected_namespaces=('settings_',))

    model_name: str = 'BAAI/bge-base-en-v1.5'

    batch_size: int = 64
    use_gpu: bool = False


Settings = SettingsSchema()
