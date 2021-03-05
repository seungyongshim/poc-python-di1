from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide
import os
import sys


class ApiClient:
    def __init__(self, api_key: str, timeout: int):
        self.api_key = os.getenv("API_KEY")  # <-- dependency is injected
        self.timeout = os.getenv("TIMEOUT")  # <-- dependency is injected
        print("here1, OK!")


class Service:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client  # <-- dependency is injected


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    api_client = providers.Singleton(
        ApiClient, api_key=config.api_key, timeout=config.timeout.as_int()
    )
    service = providers.Factory(Service, api_client=api_client)


@inject
def main(service: Service = Provide[Container.service]):  # <-- dependency is injected
    pass


if __name__ == "__main__":
    container = Container()
    container.config.api_key.from_env("API_KEY")
    container.config.api_key.from_env("TIMEOUT")
    container.wire(modules=[sys.modules[__name__]])
    main()
