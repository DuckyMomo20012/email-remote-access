from enum import Enum
from typing import Annotated

import typer
from environs import Env


class Service(str, Enum):
    server = "server"
    server_mail = "server:mail"
    client = "client"
    mail = "mail"


env = Env()
# Read .env into os.environ
env.read_env()


def main(
    service: Annotated[Service, typer.Argument()] = Service.server,
):
    if str(service) == "Service.server":
        import src.serverApp.app as serverApp

        serverApp.main()
    elif str(service) == "Service.server_mail":
        print("Starting mail server...")
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
