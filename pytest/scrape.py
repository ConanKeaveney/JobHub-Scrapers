# pull all web scaper data here
from ..companies.Amazon.scraper import Scraper as AmazonScraper
from ..companies.Facebook.scraper import Scraper as FacebookScraper
from ..companies.Google.scraper import Scraper as GoogleScraper
from ..companies.Guidewire.scraper import Scraper as GuidewireScraper
from ..companies.HubSpot.scraper import Scraper as HubSpotScraper
from ..companies.Microsoft.scraper import Scraper as MicrosoftScraper
from ..companies.MongoDB.scraper import Scraper as MongoDBScraper
from ..companies.SIG.scraper import Scraper as SIGScraper
from ..companies.Stripe.scraper import Scraper as StripeScraper
from ..companies.Walmart.scraper import Scraper as WalmartScraper


class All:
    def scrapeSIG(self):

        sig = SIGScraper(
            'SIG', 'https://careers.sig.com/search-results?keywords=dublin')

        d = {"SIG": sig.scrape()}
        data = d
        return data

    def scrapeMongoDB(self):

        mongodb = MongoDBScraper(
            'MongoDB', 'https://www.mongodb.com/careers/locations/dublin')

        d = {"MongoDB": mongodb.scrape()}
        data = d
        return data

    def scrapeHubSpot(self):

        hubspot = HubSpotScraper(
            'HubSpot', 'https://www.hubspot.com/careers/jobs?hubs_signup-url=www.hubspot.com/careers/dublin-ireland&hubs_signup-cta=careers-location-bottom&page=1#office=dublin')

        d = {
            "HubSpot": hubspot.start()}
        data = d
        return data

    def scrapeGoogle(self):

        googleEngineering = GoogleScraper(
            'Google', 'https://careers.google.com/jobs/results/?category=DATA_CENTER_OPERATIONS&category=DEVELOPER_RELATIONS&category=HARDWARE_ENGINEERING&category=MANUFACTURING_SUPPLY_CHAIN&category=NETWORK_ENGINEERING&category=PRODUCT_MANAGEMENT&category=PROGRAM_MANAGEMENT&category=SOFTWARE_ENGINEERING&category=TECHNICAL_INFRASTRUCTURE_ENGINEERING&category=TECHNICAL_SOLUTIONS&category=TECHNICAL_WRITING&company=Google&company=YouTube&hl=en&jlo=en-US&location=Dublin,%20Ireland&page=1&sort_by=date', "Engineering")

        googleSales = GoogleScraper(
            'Google', 'https://careers.google.com/jobs/results/?company=Google&company=Google%20Fiber&company=YouTube&employment_type=FULL_TIME&hl=en&jlo=en-US&location=Dublin,%20Ireland&page=1&q=Sales&sort_by=date', "Sales")

        d = {"Google": googleEngineering.start() + googleSales.start()}
        data = d
        return data

    def scrapeMicrosoft(self):

        microsoft = MicrosoftScraper(
            'Microsoft', 'https://careers.microsoft.com/us/en/search-results?qcity=Dublin&qstate=Dublin&qcountry=Ireland&from=0&s=0')

        d = {"Microsoft": microsoft.start()}
        data = d
        return data

    def scrapeStripe(self):

        stripe = StripeScraper(
            'Stripe', 'https://stripe.com/jobs/search?l=dublin')

        d = {"Stripe": stripe.start()}
        data = d
        return data

    def scrapeAmazon(self):

        amazon = AmazonScraper(
            'Amazon', 'https://www.amazon.jobs/en/search?offset=0&result_limit=10&sort=recent&cities[]=Dublin, IRL&distanceType=Mi&radius=Anykm&latitude=53.34807&longitude=-6.24827&loc_group_id=&loc_query=Dublin, Ireland&base_query=&city=Dublin&country=IRL&region=&county=County Dublin&query_options=&')

        d = {"Amazon": amazon.start()}
        data = d
        return data

    def scrapeFacebook(self):

        facebook = FacebookScraper(
            'Facebook', 'https://www.facebook.com/careers/jobs/?page=1&results_per_page=100&offices[0]=Dublin, Ireland#search_result')

        d = {"Facebook": facebook.start()}
        data = d
        return data

    def scrapeWalmart(self):

        walmart = WalmartScraper(
            'Walmart', 'https://careers.walmart.com/results?q=&page=1&sort=rank&jobCity=Dublin&jobState=IRELAND&expand=department,0000015e-b97d-d143-af5e-bd7da8ca0000,brand,type,rate&jobCareerArea=all')

        d = {"Walmart": walmart.start()}
        data = d
        return data

    def scrapeGuidewire(self):

        guidewire = GuidewireScraper(
            'Guidewire', 'https://careers.guidewire.com/job_search?dept=all&loc=dublin')

        d = {"Guidewire": guidewire.start()}
        data = d
        return data
