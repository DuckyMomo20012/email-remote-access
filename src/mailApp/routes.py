from src.mailApp.pages.connect import ConnectPage
from src.mailApp.pages.index.index import IndexPage
from src.mailApp.pages.oauth import OAuthPage
from src.shared.pages.base import BasePage

routes: dict[str, BasePage] = {
    "/connect": ConnectPage,
    "/auth": OAuthPage,
    "/": IndexPage,
}
