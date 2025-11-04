from playwright.async_api import Page

from system_tests.ui.pages.dashboard_page import DashBoardPage


class PageContainer:
    def __init__(self, page: Page):
        self.dashboard = DashBoardPage(page)
