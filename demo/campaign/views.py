# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests as req
from bs4 import BeautifulSoup
from langchain.prompts import PromptTemplate
# program defined functions
from .web_scraper import scrape_website, apolo_request_sesion
from .open_ai import get_ai_data, domain_related_route


class ScrapeDataAPIView(APIView):
    ''' scrawl urls and return the https body'''
    def post(self, request, *args, **kwargs):
        '''a post method to get url to crawl'''
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
        company_urls = [link.get('href') for link in links if link.get('href')]
        company_data = domain_related_route(
            urls=company_urls,
            target_domain= website_url
        )
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
        ''' a get method for data crawling'''
        data = scrape_website("https://mui.com/material-ui/icons/")
        print(data)
        return Response({"data": "welcome"}, status=status.HTTP_200_OK)


class PromptAPIView(APIView):
    ''' scrawl urls and return the https body'''
    def post(self, request, *args, **kwargs):
        '''a post method to get url to crawl'''
        website_url = request.data.get('website_url')

        prompt_templatex = PromptTemplate(
            input_variables=['url'],
            template="about us getter:\n"
                    "I want you to  provide an about for the company from"
                    "based on the following criteria and urls:\n"
                    "url: {url}\n"
        )

        data = get_ai_data(
            website_url,
            prompt_template=prompt_templatex
        )
        if data:
            return Response(
                data=data,
                status=status.HTTP_200_OK
                )
        else:
            return Response(
                {"error": "Failed to get URL data."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
    def get(self, request, *args, **kwargs):
        ''' a get method for data crawling'''
        return Response({"data": "welcome"}, status=status.HTTP_200_OK)