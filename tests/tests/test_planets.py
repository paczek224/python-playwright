import pytest
from playwright.async_api import expect


@pytest.mark.asyncio
async def test_foo1(user2):
    await user2.dashboard.go_to()
    await expect(user2.dashboard.page.get_by_role("searchbox")).to_be_visible()

