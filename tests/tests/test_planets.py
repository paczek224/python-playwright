import pytest
from playwright.async_api import expect

from tests.src.utils.page_utils import PageContainer


@pytest.mark.asyncio
@pytest.mark.user("user2")
async def test_foo1(user2: PageContainer):
    await user2.dashboard.go_to()
    await expect(user2.dashboard.page.get_by_role("searchbox")).to_be_visible()


@pytest.mark.asyncio
@pytest.mark.user("user3")
async def test_foo2(user3: PageContainer):
    await user3.dashboard.go_to()
    await expect(user3.dashboard.page.get_by_role("searchbox")).to_be_visible()

@pytest.mark.asyncio
@pytest.mark.user("user3")
async def test_foo4(user3: PageContainer):
    await user3.dashboard.go_to()
    await expect(user3.dashboard.page.get_by_role("searchbox")).to_be_visible()

@pytest.mark.asyncio
@pytest.mark.user("user3")
async def test_foo5(user3: PageContainer):
    await user3.dashboard.go_to()
    await expect(user3.dashboard.page.get_by_role("searchbox")).to_be_visible()

