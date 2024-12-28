from src.app.models import ModelArtefact, ModelName, ModelProvider, ModelSchema

# from src.utils.paths import MODELS_DIR


class SimpleModelProvider(ModelProvider):
    def __init__(self, model_registry: str, model_schemas: list[ModelSchema]) -> None:
        self.__model_registry = model_registry

        self.__download_models()

        self.__models: dict[ModelName, ModelSchema] = {}
        for model_schema in model_schemas:
            self.__models[model_schema.name] = f"{model_registry}/{model_schema.slug()}"

    def get(self, model: ModelSchema) -> ModelArtefact:
        return ModelArtefact(model_schema=model, uri="")

    def __download_models(self) -> None:
        _ = self.__model_registry
        pass

    def list(self) -> list[ModelSchema]:
        return list(self.__models.values())


def build_simple_model_provider() -> SimpleModelProvider:
    return SimpleModelProvider(
        model_registry="",
        model_schemas=[
            ModelSchema(ModelName.MULTIPLIER),
        ],
    )
