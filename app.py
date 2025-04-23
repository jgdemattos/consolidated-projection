from flask import Flask, request, redirect
import requests
import math
import json
from dotenv import dotenv_values
from datetime import date
from calendar import monthrange

from message_builder import MessageBuilder
from apis.monday_api import request_client_data
from apis.meta_api import get_meta_adaccounts
from apis.meta_api import get_meta_adsets
from apis.meta_api import get_meta_campaigns
from classes.meta_businessmanager import MetaBusinessmanager
from apis.google_api import get_google_adaccounts
from flask import Request

import logging
logging.basicConfig(level=logging.DEBUG)

config=dotenv_values("./.env")
app = Flask(__name__)

@app.route('/get-full-report', methods=['POST'])
def get_full_report():
    id = request.form['id']
    client_data=request_client_data(id)

    message_builder=MessageBuilder(client_data['name'])

    get_platform_data(client_data, message_builder)

    return message_builder.build_message()

@app.route('/get-projection', methods=['POST'])
def get_projection():
    id = request.form['id']
    client_data=request_client_data(id)

    message_builder=MessageBuilder(client_data['name'])

    get_platform_data(client_data, message_builder)

    return message_builder.calculate_total_projection()

def get_platform_data(client_data, message_builder):
    if(client_data['meta_id'] or client_data['meta_adaccount_ids']):
        if(client_data['meta_id']):

            meta_businessmanager_data=get_meta_adaccounts(client_data['meta_id'])
            meta_adaccounts=meta_businessmanager_data['meta_adaccounts']
            meta_businessmanager=MetaBusinessmanager(meta_businessmanager_data['meta_businessmanager_name'],client_data['meta_id'])

        else:
            LARANJEIRA_BM_ID=config["agencies_bm_id"]
            meta_businessmanager_data=get_meta_adaccounts(LARANJEIRA_BM_ID)
            meta_adaccounts=meta_businessmanager_data['meta_adaccounts']
            meta_businessmanager=MetaBusinessmanager("LARANJEIRA",LARANJEIRA_BM_ID)

    meta_adaccounts_for_current_client=[]
    if(len(client_data['meta_adaccount_ids'])==0):
        meta_adaccounts_for_current_client=meta_adaccounts
    else:
        for meta_adaccount in meta_adaccounts:
            if(meta_adaccount.is_in_this_list(client_data['meta_adaccount_ids'])):
                meta_adaccounts_for_current_client.append(meta_adaccount)
            
    meta_businessmanager.set_meta_adaccounts(meta_adaccounts_for_current_client)

    
    for meta_adaccount in meta_businessmanager.adaccounts:
        meta_adsets=get_meta_adsets(meta_adaccount)
        meta_campaigns=get_meta_campaigns(meta_adaccount, meta_adsets)
        meta_adaccount.set_campaigns(meta_campaigns)

    message_builder.set_businessmanagers([meta_businessmanager]) 

    if(client_data['google_id']):
        google_adaccount=get_google_adaccounts(client_data['google_id'])
        message_builder.set_google_accounts([google_adaccount])