from scraper import Scraper

stripe = Scraper(
    'Stripe', 'https://stripe.com/jobs/search?l=dublin')

data = stripe.start()
