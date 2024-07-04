from enum import Enum

import typer
from environs import Env

TService = Enum(  # type: ignore
    "Service",
    {
        k: k
        for k in [
            "server",
            "server:mail",
            "client",
            "mail",
        ]
    },
)

env = Env()
# Read .env into os.environ
env.read_env()


def main(service: TService = typer.Argument("server", help="Service to run")):  # noqa: B008
    if str(service) == "Service.server":
        import src.serverApp.app as serverApp

        serverApp.main()
    elif str(service) == "Service.server:mail":
        import src.mailServer.server as server

        server.main()
    elif str(service) == "Service.mail":
        import src.mailApp.app as mailApp

        mailApp.main()
    elif str(service) == "Service.client":
        import src.clientApp.app as clientApp

        clientApp.main()


if __name__ == "__main__":
    typer.run(main)
