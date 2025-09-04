def test_google_title(browser):
    browser.get("https://www.google.com/")
    assert "Google" in browser.title