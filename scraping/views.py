import os
import json
import requests
import pandas as pd
import chromedriver_autoinstaller as chromedriver

from selenium import webdriver


from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from django.db.models import ObjectDoesNotExist

from .models import Clothing, Category
from .serializers import ClothingSerializer, CategorySerializer

HBX_URL = "https://hbx.com"


class ClothingApiView(APIView):

    def get(self, request, *args, **kwargs):
        query_params = request.query_params
        gender = query_params.get('gender', 'men')
        gender_choice = gender[0].upper()

        try:
            category = Category.objects.get(
                title=query_params.get('category', 'Clothing'),
                gender=gender_choice,
            )
        except ObjectDoesNotExist:
            return Response({
                "error": "Category isn't valid. Be sure you have scraped them "
                         "before and whether spelling is correct."
            })

        scraped_data = self.scrap_items(query_params)
        self.batch_create(scraped_data, gender_choice)

        clothing = Clothing.objects.filter(
            category__gender=gender_choice,
            category=category
        )[:int(query_params.get('limit', 50))]
        serializer = ClothingSerializer(clothing, many=True)

        if query_params.get('file'):
            data = pd.DataFrame(
                list(clothing.values())
            )
            data.to_csv('files/clothing_result.csv')
            file_path = os.path.join('files/clothing_result.csv')
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="text/csv")
            response['Content-Disposition'] = 'inline; ' \
                                              'filename=clothing_result.csv'
            return response

        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def scrap_items(query_params) -> dict:
        gender = query_params.get('gender', 'men')
        limit = query_params.get('limit', 50)
        page = query_params.get('page', 1)
        category = query_params.get('category', 'Clothing')

        chromedriver.install()  # for development without docker

        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("headless")

        # for docker container
        # driver = webdriver.Remote(
        #     "http://172.26.0.2:4444", options=options
        # )

        driver = webdriver.Chrome(options=options)

        driver.get(
            f'{HBX_URL}/{gender}/categories/{category}?'
            f'gender={gender}&page={page}&limit={limit}'
        )

        product_img_general_xpath = (
            "//div[@class='picture mb-md hbx:mb-lg block relative']"
        )
        product_url_xpath = f"{product_img_general_xpath}/a[1]"
        product_img_url_xpath = f"{product_url_xpath}/img[1]"

        brand_xpath = (
            f"//div[@class='hbx:font-bold berrics:font-medium hbx:uppercase "
            f"berrics:mb-xs hypebae:text-sm hypebae:font-medium']/a[1]"
        )
        product_name_xpath = (
            f"//div[@class='hbx:uppercase mb-md berrics:text-muted "
            f"hypebae:text-dark hypebae:text-sm']/a[1]"
        )
        price_xpath = (
            f"//div[@class='leading-none text-sm berrics:pb-sm']/span[1]"
        )

        products_urls = driver.find_elements_by_xpath(product_url_xpath)
        products_img_urls = driver.find_elements_by_xpath(
            product_img_url_xpath
        )
        products_brands = driver.find_elements_by_xpath(brand_xpath)
        products_names = driver.find_elements_by_xpath(product_name_xpath)
        products_prices = driver.find_elements_by_xpath(price_xpath)

        products_dict = {}  # sku: {...} – product data
        for i in range(len(products_urls)):
            url = products_urls[i].get_attribute('href')
            sku = url.split('/')[-1]
            products_dict[sku] = {
                "sku": sku,
                "title": products_names[i].text,
                "brand": products_brands[i].text,
                "price": products_prices[i].text,
                "category": Category.objects.get(
                    title=category,
                    gender=Category.MEN if gender[0] == 'm' else Category.WOMEN
                ),
                "url": url,
                "img": products_img_urls[i].get_attribute('src'),
            }
        driver.close()

        return products_dict

    @staticmethod
    def batch_create(data: dict, gender: str):
        existing_clothing_skus = set(Clothing.objects.filter(
            category__gender=gender
        ).values_list('sku', flat=True))
        skus_to_create = set(data.keys()) - existing_clothing_skus
        products_to_create = [
            Clothing(
                sku=value['sku'],
                title=value['title'],
                brand=value['brand'],
                price=value['price'],
                category=value['category'],
                url=value['url'],
                img=value['img'],
            )
            for key, value in data.items()
            if key in skus_to_create
        ]
        Clothing.objects.bulk_create(products_to_create)


class CategoriesApiView(APIView):

    def get(self, request, *args, **kwargs):
        query_params = request.query_params
        gender = query_params.get('gender', 'men')
        gender_choice = gender[0].upper()
        categories = Category.objects.filter(gender=gender_choice)
        if not categories.exists():
            response = requests.get(f'{HBX_URL}/{gender}/categories')
            self.batch_create_categories(
                json.loads(response.text), gender_choice
            )

        if query_params.get('file'):
            data = pd.DataFrame(
                list(Category.objects.filter(gender=gender_choice).values())
            )
            data.to_csv('files/result.csv')
            file_path = os.path.join('files/result.csv')
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="text/csv")
            response['Content-Disposition'] = 'inline; filename=result.csv'
            return response
        serializer = CategorySerializer(
            Category.objects.filter(gender=gender_choice), many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def batch_create_categories(data, gender):
        categories = []
        for category in data.get('categories'):
            categories.append(Category(
                title=category.get('name'),
                code=category.get('code'),
                url=category['_links']['self']['href'],
                gender=gender,
            ))
        Category.objects.bulk_create(categories)
