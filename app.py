from enum import Enum

import typer
from environs import Env

TService = Enum("Service", {k: k for k in ["server", "client"]})  # type: ignore

env = Env()
# Read .env into os.environ
env.read_env()


def main(service: TService = typer.Argument("server", help="Service to run")):
    if str(service) == "Service.server":
        exec(open("src/server/server.py").read())
    elif str(service) == "Service.client":
        exec(open("src/client/client.py").read())


if __name__ == "__main__":
    typer.run(main)
