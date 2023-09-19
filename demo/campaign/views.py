# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .web_scraper import scrape_website, apolo_request_sesion
import requests as req
from bs4 import BeautifulSoup
import json


class ScrapeDataAPIView(APIView):
    def post(self, request, *args, **kwargs):
        website_url = request.data.get('website_url')
        linkedin_url = request.data.get('linkedin_url')

        if not (website_url and linkedin_url):
            return Response(
                {"error": "URL is required"},
                status=status.HTTP_400_BAD_REQUEST
                )
        
        # data = scrape_website(url)
        resp = req.get(url=website_url).text
        soup = BeautifulSoup(resp, 'html.parser')
        links = soup.find_all('a')
        # initial an empty 
        
        company_data = [link.get('href') for link in links if link.get('href')]
        # use apollo to data
        linkedin_data = apolo_request_sesion(linkedin_url=linkedin_url)

        data = {
            'company_data': company_data,
            'linkedin_data': linkedin_data
        }

        if company_data and linkedin_data:
            return Response(
                data=data,
                status=status.HTTP_200_OK
                )
        else:
            return Response(
                {"error": "Failed to scrape data from the URL."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
    def get(self, request, *args, **kwargs):
        data = scrape_website("https://mui.com/material-ui/icons/")
        print(data)
        return Response({"data": "welcome"}, status=status.HTTP_200_OK)