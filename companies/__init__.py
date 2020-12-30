from .Amazon.scraper import Scraper as AmazonScraper
from .Facebook.scraper import Scraper as FacebookScraper
from .Google.scraper import Scraper as GoogleScraper
from .Guidewire.scraper import Scraper as GuidewireScraper
from .HubSpot.scraper import Scraper as HubSpotScraper
from .Microsoft.scraper import Scraper as MicrosoftScraper
from .MongoDB.scraper import Scraper as MongoDBScraper
from .SIG.scraper import Scraper as SIGScraper
from .Stripe.scraper import Scraper as StripeScraper
from .Walmart.scraper import Scraper as WalmartScraper

__all__ = ['AmazonScraper', 'FacebookScraper', 'GoogleScraper', 'GuidewireScraper', 'HubSpotScraper',
           'MicrosoftScraper', 'MongoDBScraper', 'SIGScraper', 'StripeScraper', 'WalmartScraper']
