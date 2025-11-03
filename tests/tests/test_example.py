import pytest
from playwright.async_api import expect

from tests.src.utils.page_utils import PageContainer


@pytest.mark.asyncio()
async def test_foo1(user1_page):
    pages = PageContainer(user1_page)
    await pages.dashboard.go_to()
    await pages.dashboard.search_box.fill("Luke")
    await pages.dashboard.search_button.click()
    await expect(pages.dashboard.page.get_by_text("The Star Wars Search")).to_be_visible()


@pytest.mark.asyncio
async def test_foo2(user1_page):
    pages = PageContainer(user1_page)
    await pages.dashboard.go_to()
    await pages.dashboard.search_box.fill("Luke")
    await pages.dashboard.search_button.click()
    await expect(pages.dashboard.page.get_by_text("The Star Wars Search")).to_be_visible()


@pytest.mark.asyncio
async def test_foo3(user2_page):
    pages = PageContainer(user2_page)
    await pages.dashboard.go_to()
    await expect(pages.dashboard.page.get_by_role("searchbox")).to_be_visible()
