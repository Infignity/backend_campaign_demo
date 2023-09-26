''' view libraries importations'''
import os
import json
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from celery.result import AsyncResult
from elasticsearch import Elasticsearch
from pymongo import MongoClient
from bson import json_util
from .tasks import scrape_data
from .open_ai import LangChainAI


class ScrapeDataAPIView(APIView):
    ''' scraping and analysis data class'''

    def post(self, request, *args, **kwargs):
        '''a post method to scrap data sent by the client and analyze it'''
        website_url = request.data.get('website_url')

        # check that the website url and linkedin_url data is sent
        if not (website_url):
            return Response(
                {"error": "The company urls are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # check if the url supplied has https and strip it
        if website_url.startswith("https://"):
            website_url = website_url.replace("https://", "")

        # Use Celery to execute the scraping task asynchronously
        task_result = scrape_data.delay(website_url)
        task_id = task_result.id
        if task_result.successful():
            # Get the result of the task
            data = task_result.result
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response(
                data=task_id,
                status=status.HTTP_200_OK
            )


class TaskStatusAPIView(APIView):
    ''' getting task status'''

    def get(self, request, task_id):
        ''' a get function to get celery task data'''
        task = AsyncResult(task_id)
        if task.ready():
            # Task has completed, return the result
            result = task.result
            return Response(
                {"status": "completed", "result": result},
                status=status.HTTP_200_OK)
        else:
            # Task is still running or pending
            return Response({"status": "pending"},
                            status=status.HTTP_202_ACCEPTED)


class GenerateEmailsAPI(APIView):
    '''Generate Email AI'''

    def post(self, request):
        """ a post function to AI emails generated for a user"""
        es = Elasticsearch(
            os.environ.get('ELASTIC_DB_URL'),
        )
        task_id = request.data.get('task_id')
        key_id = request.data.get('_id')

        # check if task_id and key_id is sent by the client or not
        if task_id is None or key_id is None:
            return JsonResponse(
                {"error": "kindly provide both the task_id and the \
                  selected user id"},
                status=status.HTTP_404_NOT_FOUND
            )

        task = AsyncResult(task_id)
        if task.ready():
            # Task has completed, return the result
            result = task.result['ai_analysis']
            print(result)
        else:
            return JsonResponse(
                {"error": f"wait for the pending task with the id\
                  {task_id} or restart the process"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Create the Elasticsearch query
        search_query = {
            "query": {
                "match": {
                    "_id": key_id
                }
            }
        }
        # Execute the search query
        resp_data = es.search(index="linked-in", body=search_query)
        # Extract the matched user data from the response
        person_json_data = json.dumps(resp_data['hits']['hits'], indent=4)

        # generate custom email for the user
        lang_chain_ai = LangChainAI()
        email = lang_chain_ai.email_generator(
            person_json_data=person_json_data,
            company_data=result
        )
        return Response(
            data=email,
            content_type='application/json',
            status=status.HTTP_200_OK
        )
    
class GenerateEmailAPI(APIView):
    """ generate email for the profiles"""

    def post(self, request):
        """get method for generating email"""

        email_ai = LangChainAI()
        person_json_data = request.data.get("person_json_data")
        company = request.data.get("company_data")

        if not (person_json_data
                or company
                ):
            return Response(
                {"error": "job title, user linkedin name are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = email_ai.email_generator(
            person_json_data=person_json_data,
            company_data=company
        )
        return Response(
            data=data,
            content_type='application/json',
            status=status.HTTP_200_OK
        )


class GetLinkedInData(APIView):
    '''get linkedin data'''

    def post(self, request):
        """get the linkedin data"""
        client = MongoClient(os.environ.get("MONGO_DB_URL"))['Linked_in_db']
        collection = client['Linked_in_1']
        # get the username
        person_name = request.data.get('job_title')
        profile_doc = collection.find({'data.job_title': 'senior'}).limit(10)

        # Check if the cursor is empty
        if not profile_doc or (profile_doc is None):
            return JsonResponse(
                {"error": f"user with the name {person_name} not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        # Convert the cursor to a list of dictionaries
        profile_data = [json.loads(json_util.dumps(dc)) for dc in profile_doc]

        # Return the serialized data as JSON response
        return JsonResponse(
            {"data": profile_data, "message": "Data retrieved successfully"},
            status=status.HTTP_200_OK
        )
    