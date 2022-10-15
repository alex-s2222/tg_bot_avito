from typing import NamedTuple, List
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


class Temporary_advertisement(NamedTuple):
    name: str
    href: str
    description: str
    price: int


class Advertisement:
    _advertisement: List[Temporary_advertisement]

    def __init__(self, url: str):
        self._advertisement = self._start_driver(url=url)

    def _start_driver(self, url: str) -> List[Temporary_advertisement]:
        # start driver
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(url)
        content = driver.page_source
        driver.close()
        return self._parse_url(content=content)

    def _parse_url(self, content: str) -> List[Temporary_advertisement]:
        result_advertisement = []

        soup = BeautifulSoup(content, features="lxml")

        # for i in range(3):
        name: str
        href: str
        description: str
        price: int

        # parse description
        for j, tag_div in enumerate(soup.findAll(attrs={'class': 'iva-item-root-_lk9K photo-slider-slider-S15A_ iva-item-list-rfgcH iva-item-redesign-rop6P iva-item-responsive-_lbhG items-item-My3ih items-listItem-Gd1jN js-catalog-item-enum'})):

            # search url and name product
            name, href = self._get_name_href(tag_div)

            # search description product
            description = self._get_descriptions(tag_div)

            # search price product
            price = self._get_price(tag_div)

            result_advertisement.append(Temporary_advertisement(
                name=name, href=href, description=description, price=price
            ))
            if j == 2: break

        return result_advertisement

    def _get_name_href(self, tag):
        HREF_AVITO = "https://www.avito.ru"

        for tag_div_a in tag.findAll(attrs={'class': 'iva-item-titleStep-pdebR'}):
            for tag_a in tag_div_a:
                href = HREF_AVITO + tag_a.attrs.get("href")
                print("URL:\t", href)
                name = tag_a['title']
                print("Name:\t", name)
                return name, href

    def _get_descriptions(self, tag):
        for tag_description in tag.findAll(attrs={'class': 'iva-item-text-Ge6dR iva-item-description-FDgK4 text-text-LurtD text-size-s-BxGpL'}):
            list_description = str(tag_description.text).split("\n")
            description = " ".join(list_description)
            print("description:\t", description)
            return description

    def _get_price(self, tag):
        for tag_name in tag.findAll(attrs={'itemprop': 'price'}):
            price = int(tag_name['content'])
            print("price:\t", price)
            return price

# &p=1 for speed
probe = Advertisement("https://www.avito.ru/sankt_peterburg_i_lo/audio_i_video/naushniki-ASgBAgICAUSIAtRO?cd=1&f=ASgBAQECAUSIAtROAUDqvA0U_NE0AUXGmgwUeyJmcm9tIjowLCJ0byI6NjAwMH0&q=airpods&p=1&s=104&user=1")