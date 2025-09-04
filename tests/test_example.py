def test_python_org(browser):
    browser.get("https://www.python.org/")
    assert "Python" in browser.title