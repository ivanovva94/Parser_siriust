import requests
from lxml import html
from xpath_locators import UserDataLocators, WishlistLocators
from data_base import add_user_data, add_wishlist, display_data

URLS = {
    "main_url": "https://siriust.ru/",
    "profile_url": "https://siriust.ru/profiles-update/",
    "wishlist_url": "https://siriust.ru/wishlist/"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}


class Parser:

    def __init__(self, mail, password):
        self.already_login = False
        self.mail = mail
        self.password = password
        self.session = requests.Session()

    def login(self):
        payload = {
            "return_url": "index.php",
            "redirect_url": "index.php",
            "user_login": self.mail,
            "password": self.password,
            "dispatch[auth.login]": ""
        }
        response = self.session.post(URLS["main_url"], data=payload, headers=headers)
        response.raise_for_status()
        login_status = "Вы успешно авторизовались."

        if login_status in response.text:
            self.already_login = True
            print("Авторизация прошла успешно...")
            return True
        else:
            raise Exception("Ошибка авторизации")

    def get_html_tree(self, url):
        if not self.already_login:
            self.login()
        try:
            response = self.session.get(url, headers=headers)
            html_tree = html.fromstring(response.content.decode("utf-8"))
            return html_tree
        except Exception as e:
            print(f"Не удалось получить контент с {url}")
            print(e)

    @staticmethod
    def get_item_rating(html_tree):
        star = len(html_tree.xpath(WishlistLocators.STAR))
        star_half = len(html_tree.xpath(WishlistLocators.STAR_HALF))

        if star_half > 0:
            star += 0.5
            return star
        return star

    @staticmethod
    def count_of_available_shops(html_tree):
        count = 0
        shops = html_tree.xpath(WishlistLocators.SHOPS)

        for shop in shops:
            if "отсутствует" not in shop:
                count += 1
        return count

    @staticmethod
    def get_reviews_from_list(reviews_list):
        reviews_text = ""

        for reviews in reviews_list:
            reviews_text += reviews
        return reviews_text

    @staticmethod
    def get_price(html_tree):
        price_list = html_tree.xpath(WishlistLocators.PRICE)[0:2]
        convert_price = list(map(lambda x: float(x.replace("\xa0", "")), price_list))
        return convert_price

    def get_reviews_pagination(self, html_tree, reviews_list=None):
        if reviews_list is None:
            reviews_list = []

        button_pagination = html_tree.xpath(WishlistLocators.REVIEWS_PAGINATION)
        reviews_next_html = self.get_html_tree(button_pagination[0])
        reviews_next = reviews_next_html.xpath(WishlistLocators.REVIEWS)[0]
        reviews_list.append(reviews_next)
        button_pagination_next = reviews_next_html.xpath(WishlistLocators.REVIEWS_PAGINATION)

        if button_pagination_next:
            self.get_reviews_pagination(reviews_next_html, reviews_list=reviews_list)
        return reviews_list

    def parse_user_data(self):
        user_data = {}

        user_html = self.get_html_tree(URLS["profile_url"])
        user_data["mail"] = user_html.xpath(UserDataLocators.MAIL)[0]
        user_data["first_name"] = user_html.xpath(UserDataLocators.FIRST_NAME)[0]
        user_data["last_name"] = user_html.xpath(UserDataLocators.LAST_NAME)[0]
        user_data["city"] = user_html.xpath(UserDataLocators.CITY)[0]

        add_user_data(user_data)

    def parse_wishlist_data(self):
        wishlist_html = self.get_html_tree(URLS["wishlist_url"])
        items_hrefs = wishlist_html.xpath(WishlistLocators.ITEM_HREF)

        for href in items_hrefs:
            item_html = self.get_html_tree(href)
            name = item_html.xpath(WishlistLocators.ITEM_NAME)
            price = self.get_price(item_html)
            rating = self.get_item_rating(item_html)
            count_of_shops = self.count_of_available_shops(item_html)
            reviews_count = item_html.xpath(WishlistLocators.REVIEWS_COUNT)
            reviews = item_html.xpath(WishlistLocators.REVIEWS)

            if reviews_count and reviews:
                reviews_next_button = item_html.xpath(WishlistLocators.REVIEWS_PAGINATION)
                if reviews_next_button:
                    reviews_next = self.get_reviews_pagination(item_html)
                    for rev in reviews_next:
                        reviews.append(rev)
                reviews_text = self.get_reviews_from_list(reviews)

                wishlist_data = {
                    "item_name": name[0],
                    "retail_price": price[0],
                    "trade_price": price[1],
                    "reviews_count": reviews_count[0],
                    "rating": rating,
                    "count_of_shops": count_of_shops,
                    "reviews": reviews_text
                }
                add_wishlist(self.mail, wishlist_data)

            else:
                reviews_count = "0 отзывов"
                reviews = "Нет отзывов"
                wishlist_data = {
                    "item_name": name[0],
                    "retail_price": price[0],
                    "trade_price": price[1],
                    "reviews_count": reviews_count[0],
                    "rating": rating,
                    "count_of_shops": count_of_shops,
                    "reviews": reviews
                }
                add_wishlist(self.mail, wishlist_data)

        print("Данные по избранным товарам собраны!\n")


if __name__ == "__main__":
    mail = input("Enter your mail: ")
    password = input("Enter your password: ")
    parse = Parser(mail, password)
    parse.parse_user_data()
    parse.parse_wishlist_data()
    display_data()
