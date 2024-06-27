from src.newClientApp.pages.connect import ConnectPage
from src.newClientApp.pages.index.index import IndexPage
from src.shared.pages.base import BasePage

routes: dict[str, BasePage] = {"/connect": ConnectPage, "/": IndexPage}
