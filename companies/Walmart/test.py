from scraper import Scraper

walmart = Scraper(
    'Walmart', 'https://careers.walmart.com/results?q=&page=1&sort=rank&jobCity=Dublin&jobState=IRELAND&expand=department,0000015e-b97d-d143-af5e-bd7da8ca0000,brand,type,rate&jobCareerArea=all')

data = walmart.start()
