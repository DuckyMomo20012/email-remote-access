from enum import Enum

import typer
from environs import Env

import src.client.client as client
import src.server.server as server

TService = Enum("Service", {k: k for k in ["server", "client"]})  # type: ignore

env = Env()
# Read .env into os.environ
env.read_env()


def main(service: TService = typer.Argument("server", help="Service to run")):
    if str(service) == "Service.server":
        server.main()
    elif str(service) == "Service.client":
        client.main()


if __name__ == "__main__":
    typer.run(main)
