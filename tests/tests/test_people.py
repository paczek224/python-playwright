import pytest
from playwright.async_api import expect

from tests.src.utils.page_utils import PageContainer


@pytest.mark.asyncio()
async def test_foo1(user1):
    await user1.dashboard.go_to()
    await user1.dashboard.search_box.fill("Luke")
    await user1.dashboard.search_button.click()
    await expect(user1.dashboard.page.get_by_text("The Star Wars Search")).to_be_visible()


@pytest.mark.asyncio
async def test_foo2(user1: PageContainer):
    await user1.dashboard.go_to()
    await user1.dashboard.search_box.fill("Luke")
    await user1.dashboard.search_button.click()
    await expect(user1.dashboard.page.get_by_text("The Star Wars Search")).to_be_visible()
