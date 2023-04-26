from enum import Enum

import typer
from environs import Env

import src.client.app as clientApp
import src.mail.app as mailApp
import src.server.app as serverApp

TService = Enum("Service", {k: k for k in ["server", "client", "mail"]})  # type: ignore

env = Env()
# Read .env into os.environ
env.read_env()


def main(service: TService = typer.Argument("server", help="Service to run")):
    if str(service) == "Service.server":
        serverApp.main()
    elif str(service) == "Service.client":
        clientApp.main()
    elif str(service) == "Service.mail":
        mailApp.main()


if __name__ == "__main__":
    typer.run(main)
