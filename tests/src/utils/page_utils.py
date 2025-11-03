from playwright.async_api import Page

from tests.src.pages.dashboard_page import DashBoardPage


class PageContainer:
    def __init__(self, page: Page):
        self.dashboard = DashBoardPage(page)
