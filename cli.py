from enum import Enum

import typer
from environs import Env

import src.mailApp.app as mailApp
import src.mailServer.server as server
import src.newClientApp.app as newClientApp
import src.serverApp.app as serverApp

TService = Enum(  # type: ignore
    "Service",
    {
        k: k
        for k in [
            "server",
            "server:mail",
            "server:legacy",
            "client",
            "client:new",
            "mail",
        ]
    },
)

env = Env()
# Read .env into os.environ
env.read_env()


def main(service: TService = typer.Argument("server", help="Service to run")):  # noqa: B008
    if str(service) == "Service.server":
        serverApp.main()
    elif str(service) == "Service.server:mail":
        server.main()
    elif str(service) == "Service.mail":
        mailApp.main()
    elif str(service) == "Service.client:new":
        newClientApp.main()


if __name__ == "__main__":
    typer.run(main)
