# pull all web scaper data here
from companies import *


class All:
    def scrape(self):

        sig = SIGScraper(
            'SIG', 'https://careers.sig.com/search-results?keywords=dublin')
        mongodb = MongoDBScraper(
            'MongoDB', 'https://www.mongodb.com/careers/locations/dublin')

        hubspot = HubSpotScraper(
            'HubSpot', 'https://www.hubspot.com/careers/jobs?hubs_signup-url=www.hubspot.com/careers/dublin-ireland&hubs_signup-cta=careers-location-bottom&page=1#office=dublin')

        googleEngineering = GoogleScraper(
            'Google', 'https://careers.google.com/jobs/results/?category=DATA_CENTER_OPERATIONS&category=DEVELOPER_RELATIONS&category=HARDWARE_ENGINEERING&category=MANUFACTURING_SUPPLY_CHAIN&category=NETWORK_ENGINEERING&category=PRODUCT_MANAGEMENT&category=PROGRAM_MANAGEMENT&category=SOFTWARE_ENGINEERING&category=TECHNICAL_INFRASTRUCTURE_ENGINEERING&category=TECHNICAL_SOLUTIONS&category=TECHNICAL_WRITING&company=Google&company=YouTube&hl=en&jlo=en-US&location=Dublin,%20Ireland&page=1&sort_by=date', "Engineering")

        googleSales = GoogleScraper(
            'Google', 'https://careers.google.com/jobs/results/?company=Google&company=Google%20Fiber&company=YouTube&employment_type=FULL_TIME&hl=en&jlo=en-US&location=Dublin,%20Ireland&page=1&q=Sales&sort_by=date', "Sales")

        microsoft = MicrosoftScraper(
            'Microsoft', 'https://careers.microsoft.com/us/en/search-results?qcity=Dublin&qstate=Dublin&qcountry=Ireland&from=0&s=0')

        stripe = StripeScraper(
            'Stripe', 'https://stripe.com/jobs/search?l=dublin')

        amazon = AmazonScraper(
            'Amazon', 'https://www.amazon.jobs/en/search?offset=0&result_limit=10&sort=recent&cities[]=Dublin, IRL&distanceType=Mi&radius=Anykm&latitude=53.34807&longitude=-6.24827&loc_group_id=&loc_query=Dublin, Ireland&base_query=&city=Dublin&country=IRL&region=&county=County Dublin&query_options=&')

        facebook = FacebookScraper(
            'Facebook', 'https://www.facebook.com/careers/jobs/?page=1&results_per_page=100&offices[0]=Dublin, Ireland#search_result')

        walmart = WalmartScraper(
            'Walmart', 'https://careers.walmart.com/results?q=&page=1&sort=rank&jobCity=Dublin&jobState=IRELAND&expand=department,0000015e-b97d-d143-af5e-bd7da8ca0000,brand,type,rate&jobCareerArea=all')

        guidewire = GuidewireScraper(
            'Guidewire', 'https://careers.guidewire.com/job_search?dept=all&loc=dublin')

        d = {"Guidewire": guidewire.start(), "Walmart": walmart.start(), "Facebook": facebook.start(), "Amazon": amazon.start(), "Microsoft": microsoft.start(), "SIG": sig.scrape(), "MongoDB": mongodb.scrape(),
             "HubSpot": hubspot.start(), "Google": googleEngineering.start() + googleSales.start(), "Stripe": stripe.start()}
        data = d
        return data
