import requests

from system_tests.api.utils.api_urls import url, DashboardUrl
from system_tests.api.utils.function_utils import all_match, any_match


def test_searching_people_by_name():
    search_param = "Ma"
    existing_planet_full_name = "Polis Massa"

    data = requests.get(url(DashboardUrl.PLANETS), params={"name": search_param}).json()

    all_match(data["result"], lambda r: search_param in r["properties"]["name"])
    any_match(data["result"], lambda r: r["properties"]["name"] == existing_planet_full_name)

