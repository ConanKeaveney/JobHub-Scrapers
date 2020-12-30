
from . import scrape


def scrapeSIG():
    all = scrape.All()
    data = all.scrapeSIG()
    return data


def scrapeMongoDB():
    all = scrape.All()
    data = all.scrapeMongoDB()
    return data


def scrapeHubSpot():
    all = scrape.All()
    data = all.scrapeHubSpot()
    return data


def scrapeGoogle():
    all = scrape.All()
    data = all.scrapeGoogle()
    return data


def scrapeMicrosoft():
    all = scrape.All()
    data = all.scrapeMicrosoft()
    return data


def scrapeStripe():
    all = scrape.All()
    data = all.scrapeStripe()
    return data


def scrapeAmazon():
    all = scrape.All()
    data = all.scrapeAmazon()
    return data


def scrapeFacebook():
    all = scrape.All()
    data = all.scrapeFacebook()
    return data


def scrapeWalmart():
    all = scrape.All()
    data = all.scrapeWalmart()
    return data


def scrapeGuidewire():
    all = scrape.All()
    data = all.scrapeGuidewire()
    return data


# test that scraper returns at least one entry


def test_SIG():
    assert len(scrapeSIG().get("SIG")) > 0


def test_MongoDB():
    assert len(scrapeMongoDB().get("MongoDB")) > 0


def test_HubSpot():
    assert len(scrapeHubSpot().get("HubSpot")) > 0


def test_Google():
    assert len(scrapeGoogle().get("Google")) > 0


def test_Microsoft():
    assert len(scrapeMicrosoft().get("Microsoft")) > 0


def test_Stripe():
    assert len(scrapeStripe().get("Stripe")) > 0


def test_Amazon():
    assert len(scrapeAmazon().get("Amazon")) > 0


def test_Facebook():
    assert len(scrapeFacebook().get("Facebook")) > 0


def test_Walmart():
    assert len(scrapeWalmart().get("Walmart")) > 0


def test_Guidewire():
    assert len(scrapeGuidewire().get("Guidewire")) > 0
