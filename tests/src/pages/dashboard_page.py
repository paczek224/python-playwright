from playwright.async_api import Page

from tests.src.config import config
from tests.src.pages.abstract_page import BasePage


class DashBoardPage(BasePage):
    def __init__(self, page:Page):
        super().__init__(page)
        self.people_radio_button = page.locator("input#people")
        self.planets_radio_button = page.locator("input#planets")
        self.search_box = page.get_by_role("searchbox")
        self.search_button = page.locator("//button[normalize-space()='Search']")

    async def go_to(self):
        await self.page.goto(config.settings.app_url)