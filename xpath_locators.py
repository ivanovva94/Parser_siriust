class UserDataLocators:
    MAIL = "//input[@name='user_data[email]']/@value"
    FIRST_NAME = "//input[@name='user_data[s_firstname]']/@value"
    LAST_NAME = "//input[@name='user_data[s_lastname]']/@value"
    CITY = "//input[@name='user_data[s_city]']/@value"


class WishlistLocators:
    ITEM_HREF = "//a[@class='abt-single-image']/@href"
    ITEM_NAME = "//h1[@class='ty-product-block-title']//bdi/text()"
    PRICE = "//span[@class='ty-price-num']/text()"
    STAR = "//div[@class='ty-discussion__rating-wrapper']/span/a/i[@class='ty-stars__icon ty-icon-star']"
    STAR_HALF = "//div[@class='ty-discussion__rating-wrapper']/span/a/i[@class='ty-stars__icon ty-icon-star-half']"
    SHOPS = "//div[@class='ty-product-feature']/div/text()"
    REVIEWS = "//div[@class='ty-discussion-post__message']/text()"
    REVIEWS_COUNT = "//a[@class='ty-discussion__review-a cm-external-click']/text()"
    REVIEWS_PAGINATION = "//a[@class='ty-pagination__item ty-pagination__btn ty-pagination__next cm-history cm-ajax ty-pagination__right-arrow']/@href"
