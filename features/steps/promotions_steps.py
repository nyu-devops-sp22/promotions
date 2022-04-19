######################################################################
# Copyright 2016, 2021 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

"""
Promotion Steps

Steps file for Promotion.feature

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import json
import requests
from behave import given
from compare import expect


@given('the following promotions')
def step_impl(context):
    """ Delete all Promotions and load new ones """
    headers = {'Content-Type': 'application/json'}
    # list all of the promotions and delete them one by one
    context.resp = requests.get(
        context.base_url + '/promotions', headers=headers)
    expect(context.resp.status_code).to_equal(200)
    for promotion in context.resp.json():
        context.resp = requests.delete(
            context.base_url + '/promotions/' + str(promotion["_id"]), headers=headers)
        expect(context.resp.status_code).to_equal(204)

    # load the database with new promotions
    create_url = context.base_url + '/promotions'
    for row in context.table:
        data = {
            "name": row["name"],
            "start_date": row["start_date"],
            "end_date": row["end_date"],
            "type": row["type"],
            "value": row["value"],
            "ongoing": row["ongoing"] in ["True", "true", "1"],
            "product_id": row["product_id"]
        }
        payload = json.dumps(data)
        context.resp = requests.post(create_url, data=payload, headers=headers)
        expect(context.resp.status_code).to_equal(201)
