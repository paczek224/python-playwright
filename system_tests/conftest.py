import os


def pytest_configure(config):

    project_root = os.path.dirname(os.path.abspath(__file__))
    html_report_path = os.path.join(project_root, "TestReport.html")
    config.option.htmlpath = html_report_path
    config._metadata = getattr(config, "_metadata", {})

