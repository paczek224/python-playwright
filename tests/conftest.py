import json
import os
import pathlib
import re

import pytest
from playwright.async_api import async_playwright
from pytest_html import extras
from xdist.scheduler import LoadScopeScheduling

from tests.src.config import config
from tests.src.utils.page_utils import PageContainer

PROJECT_ROOT = pathlib.Path(__file__).parent.resolve()
TRACES_DIR = PROJECT_ROOT / "test-results"
STATES_DIR = PROJECT_ROOT / "context" / "state"


def get_trace_path(node_id):
    safe_name = re.sub(r"[:_/\[.]+", "-", str(node_id)).strip("-")
    test_directory_name = safe_name.replace("_", "-").replace("::", "-").replace("[", "-").replace("]", "")
    return TRACES_DIR / test_directory_name / "trace.zip"


async def start_browser(pw):
    match config.settings.browser:
        case "chromium" | "edge" | "chrome":
            return await pw.chromium.launch(headless=config.settings.headless)
        case "firefox":
            return await pw.firefox.launch(headless=config.settings.headless)
        case "webkit":
            return await pw.webkit.launch(headless=config.settings.headless)
        case _:
            return "Unknown browser"


async def start_context(browser, state_file_name):
    file_path = STATES_DIR / state_file_name

    if not os.path.exists(file_path):
        pathlib.Path.touch(file_path, exist_ok=True)
        file_path.write_text(json.dumps({"cookies": [], "origins": []}, indent=2), encoding="utf-8")

    return await browser.new_context(storage_state=file_path)


async def start_tracing(page):
    await page.context.tracing.start(screenshots=True, snapshots=True, sources=True)


async def tear_down_user_page_fixture(page, request):
    trace_path = get_trace_path(request.node.nodeid)
    await page.context.tracing.stop(path=str(trace_path))
    if request.node.rep_call.passed:
        os.remove(trace_path)
        os.removedirs(trace_path.parent)
    await page.close()


async def tear_down_user_fixture(context, browser):
    await context.close()
    await browser.close()


@pytest.fixture(scope="function")
async def user1(request):
    async with async_playwright() as pw:
        browser = await start_browser(pw)
        context = await start_context(browser, "user1_state.json")
        page = await context.new_page()
        await start_tracing(page)
        page_container = PageContainer(page)
        yield page_container
        await tear_down_user_page_fixture(page, request)
        await tear_down_user_fixture(context, browser)


@pytest.fixture(scope="function")
async def user2(request):
    async with async_playwright() as pw:
        browser = await start_browser(pw)
        context = await start_context(browser, "user2_state.json")
        page = await context.new_page()
        await start_tracing(page)
        page_container = PageContainer(page)
        yield page_container
        await tear_down_user_page_fixture(page, request)
        await tear_down_user_fixture(context, browser)


@pytest.fixture(scope="function")
async def user3(request):
    async with async_playwright() as pw:
        browser = await start_browser(pw)
        context = await start_context(browser, "user3_state.json")
        page = await context.new_page()
        await start_tracing(page)
        page_container = PageContainer(page)
        yield page_container
        await tear_down_user_page_fixture(page, request)
        await tear_down_user_fixture(context, browser)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    trace = get_trace_path(str(rep.nodeid))

    if rep.when == "call" and rep.failed:

        if not hasattr(rep, "extra"):
            rep.extra = []
        rep.extra.append(extras.url(os.path.relpath(trace, PROJECT_ROOT), name=f"playwright show-trace {trace}"))


class PerUserScheduler(LoadScopeScheduling):
    def _split_scope(self, nodeid):
        parts = nodeid.split("::")
        if len(parts) > 2 and parts[0] == "user":
            return "::".join(parts[:2])
        return super()._split_scope(nodeid)


def pytest_xdist_make_scheduler(config, log):
    return PerUserScheduler(config, log)


def pytest_collection_modifyitems(config, items):
    for item in items:
        user_marker = item.get_closest_marker("user")
        if user_marker:
            user_id = user_marker.args[0]
            item._nodeid = f"user::{user_id}::{item.nodeid}"
