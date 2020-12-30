
import math
import os
import re
import shelve

import markdown
import pymongo
from flask import Flask, g, jsonify, request
from flask_restful import Api, Resource, reqparse
from pymongo import MongoClient

import scrape
from connect import Connect

# flask instance
app = Flask(__name__)

# Create the API
api = Api(app)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response


def connectmongo():
    connection = Connect.get_connection()
    return connection


def get_mongo_db():
    client = Connect.get_connection()
    db = client.scrapers
    return db

# Local


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open("./postings/postings.db")
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/api/scrapers/')
def index():
    """present documentation"""

    # Open README
    with open(os.path.dirname(app.root_path) + '/scrapers/README.md', 'r') as markdown_file:

        # read file content
        content = markdown_file.read()

        # convert to HTML
        return markdown.markdown(content)


class JobList(Resource):
    # Get All Postings
    def get(self):

        mongodb = get_mongo_db()

        if ('page' in request.args):

            if ('description' in request.args):
                searchJob = request.args['description']
            else:
                searchJob = '.*'

            if ('category' in request.args):
                searchCategory = request.args['category']
            else:
                searchCategory = '.*'

            if ('company' in request.args):
                searchCompany = request.args['company']
            else:
                searchCompany = '.*'

            limit = 20
            page = int(request.args['page'])
            offset = (page - 1) * limit

            search = searchJob
            search_expr = re.compile(f".*{search}.*", re.I)

            search2 = searchCompany
            search_expr2 = re.compile(f".*{search2}.*", re.I)

            search3 = searchCategory
            search_expr3 = re.compile(f".*{search3}.*", re.I)

            starting_id = mongodb.test.find({}).sort(
                '_id', pymongo.ASCENDING)
            last_id = starting_id[offset]['_id']

            search_request = {
                '$and': [{'_id': {'$gte': last_id}},
                         {'$and': [
                             {'job.company': {'$regex': search_expr2}},
                             {'job.category': {'$regex': search_expr3}},
                             {'$or': [{'job.description': {'$regex': search_expr}},
                                      {'job.experience': {'$regex': search_expr}},
                                      {'job.title': {'$regex': search_expr}}
                                      ]}]
                          }]

            }
            search_request2 = {

                '$and': [
                    {'job.company': {'$regex': search_expr2}},
                    {'job.category': {'$regex': search_expr3}},
                    {'$or': [{'job.description': {'$regex': search_expr}},
                             {'job.experience': {'$regex': search_expr}},
                             {'job.title': {'$regex': search_expr}}
                             ]}]
            }

            count = mongodb.test.count_documents({'$and': [
                {'job.company': {'$regex': search_expr2}},
                {'job.category': {'$regex': search_expr3}},
                {'$or': [{'job.description': {'$regex': search_expr}},
                         {'job.experience': {'$regex': search_expr}},
                         {'job.title': {'$regex': search_expr}}
                         ]}]
            })

            totalPages = math.ceil((count/limit))

            if (int(request.args['page']) > totalPages) or (int(request.args['page']) < 1):

                return {'message': 'Invalid Page, No Data'}, 404

            hasNextPage = True

            if (offset+limit) >= count:
                hasNextPage = False

            cursor = mongodb.test.find(search_request).sort(
                '_id', pymongo.ASCENDING).limit(limit)

            postings = []
            companies = []
            categories = []

            pageCount = 0
            for i in cursor:
                pageCount = pageCount + 1
                postings.append({str(i['_id']): i['job']})

            cursorNoLimit = mongodb.test.find(search_request2).sort(
                '_id', pymongo.ASCENDING)

            for i in cursorNoLimit:
                if not(i['job']['company'] in companies):
                    companies.append(i['job']['company'])
                if not(i['job']['category'] in categories):
                    categories.append(i['job']['category'])

            companies.sort()
            categories.sort()

            return {'message': 'Success',
                    'data': postings,
                    'hasNextPage': hasNextPage,
                    'totalJobs': count,
                    'totalJobsThisPage': pageCount,
                    'totalPages': totalPages,
                    'companies': companies,
                    'categories': categories}, 200

        else:

            cursor = mongodb.test.find({}).sort(
                '_id', pymongo.ASCENDING)
            postings = []

            pageCount = 0
            for i in cursor:
                postings.append({str(i['_id']): i['job']})
            # print(postings)

            return {'message': 'No Page Given', 'data': postings, }, 200

    # post request for testing, post data scraped from web scraper
    # todo : make async
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('identifier', required=False)
        try:
            all = scrape.All()
            data = all.scrape()
        except:
            print("Scrape Failed")
            return {'message': 'Scraper Failed :( Feature in Development'}, 202
        else:
            mongodb = get_mongo_db()

            # empty db
            mongodb.test.delete_many({})

            mongodb.test.insert_one({"data": data})

            return {'message': 'Jobs Added!', 'data': data}, 201


api.add_resource(JobList, '/api/scrapers/postings')
