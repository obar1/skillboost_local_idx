import pytest
from py_fetch_skillboost import fetch_page, save_html

import requests


def test_fetch_page_success(monkeypatch):
    class FakeResponse:
        text = "<html>test</html>"

        def raise_for_status(self):
            pass

    def fake_get(*args, **kwargs):
        return FakeResponse()

    monkeypatch.setattr(requests, "get", fake_get)
    assert fetch_page("abc", 123) == "<html>test</html>"


def test_fetch_page_http_error(monkeypatch):
    class FakeResponse:
        text = "<html></html>"

        def raise_for_status(self):
            raise requests.HTTPError("404")

        status_code = 404

    def fake_get(*args, **kwargs):
        return FakeResponse()

    monkeypatch.setattr(requests, "get", fake_get)
    with pytest.raises(requests.HTTPError):
        fetch_page("abc", 123)


def test_save_html(tmp_path):
    html_content = "<div>hello</div>"
    out_file = tmp_path / "test.html"
    save_html("abc", 123, html_content, out_file, True)
    content = out_file.read_text("utf-8")
    assert "hello" in content
    assert "Original page" in content


def test_save_html_recaptcha(tmp_path):
    html_content = "This site is protected by reCAPTCHA and the Google"
    out_file = tmp_path / "test.html"
    with pytest.raises(Exception):
        save_html("abc", 123, html_content, out_file)
