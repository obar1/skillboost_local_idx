import pytest
import requests
from py_fetch_skillboost import fetch_page, save_html  # Replace with actual module name
from http.cookiejar import MozillaCookieJar


def test_fetch_page_http_error(monkeypatch):
    class FakeResponse:
        text = "<html></html>"

        def raise_for_status(self):
            raise requests.HTTPError("404")

        status_code = 404

    def fake_get(*args, **kwargs):
        return FakeResponse()

    def fake_cookie_load(self, filename, ignore_discard=True, ignore_expires=True):
        pass

    monkeypatch.setattr(MozillaCookieJar, "load", fake_cookie_load)
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
        save_html("abc", 123, html_content, out_file, True)
