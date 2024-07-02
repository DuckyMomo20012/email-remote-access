from src.clientApp.pages.connect import ConnectPage
from src.clientApp.pages.index.index import IndexPage
from src.shared.pages.base import BasePage

routes: dict[str, BasePage] = {"/connect": ConnectPage, "/": IndexPage}
