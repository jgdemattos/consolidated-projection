import requests
import json
from datetime import datetime
from datetime import date
from calendar import monthrange
from classes.meta_adset import MetaAdset
from classes.meta_campaign import MetaCampaign
from classes.meta_adaccount import MetaAdaccount
from dotenv import dotenv_values #pip

config=dotenv_values("./.env")

def get_meta_adaccounts(meta_id):
    fields="fields=name,owned_ad_accounts{name},client_ad_accounts{name}"
    url=f'https://graph.facebook.com/v16.0/{meta_id}/?{fields}&access_token={config["access_token"]}'
    ret = requests.get(url)
    meta_adaccounts_data=json.loads(ret.text)

    meta_adaccounts=create_meta_adaccounts(meta_adaccounts_data)

    return {'meta_businessmanager_name':meta_adaccounts_data['name'],'meta_adaccounts':meta_adaccounts}

def create_meta_adaccounts(meta_adaccounts_data):
    adaccounts=[]

    for meta_adaccount_data in meta_adaccounts_data['owned_ad_accounts']['data']:
        new_meta_adaccount=MetaAdaccount(meta_adaccount_data['id'],meta_adaccount_data['name'])
        adaccounts.append(new_meta_adaccount)
    if 'client_ad_accounts' in meta_adaccounts_data:
        for meta_adaccount_data in meta_adaccounts_data['client_ad_accounts']['data']:
            new_meta_adaccount=MetaAdaccount(meta_adaccount_data['id'], meta_adaccount_data['name'], False)
            adaccounts.append(new_meta_adaccount)

    return adaccounts

def get_meta_adsets(meta_adaccount):
    #get days left in month
    today = date.today()
    last_day_this_month=monthrange(today.year, today.month)[1]

    days_left_this_month=((date(today.year, today.month, today.day) - date(today.year, today.month, last_day_this_month)).days)*-1

    #request adsets from insights API per adset with spend data  
    timerange=f'{{"since":"{str(date(today.year, today.month, 1))}","until":"{str(date(today.year, today.month, today.day))}"}}'

    url=f'https://graph.facebook.com/v16.0/{meta_adaccount.id}/insights?fields=campaign_name,campaign_id,adset_name,adset_id,spend&level=adset&time_increment=all_days&limit=150&time_range={timerange}&access_token={config["access_token"]}'

    meta_adset_data = requests.get(url)
    meta_adsets=get_all_adsets_from_insightsAPI(json.loads(meta_adset_data.text)["data"])

    return meta_adsets

def get_meta_campaigns(meta_adaccount, meta_adsets):

    meta_campaigns=[]
    for meta_adset in meta_adsets:
        if(not check_if_campaign_exists(meta_campaigns, meta_adset.campaign_id)):
            new_meta_campaign=MetaCampaign(meta_adset.campaign_id,meta_adset.campaign_name)
            meta_campaigns.append(new_meta_campaign)

    # add adsets to corresponding campaigns
    for meta_campaign in meta_campaigns:
        new_meta_adsets=[]
        for meta_adset in meta_adsets:
            if(meta_campaign.id==meta_adset.campaign_id):
                new_meta_adsets.append(meta_adset)
        meta_campaign.adsets=new_meta_adsets
    
    for meta_campaign in meta_campaigns:
        #request adset data from campaign API
        url=f'https://graph.facebook.com/v16.0/{meta_campaign.id}/?fields=start_time,stop_time,lifetime_budget,name,daily_budget,effective_status,adsets{{name,id,daily_budget,effective_status}}&limit=50&date_preset=this_month&access_token={config["access_token"]}'

        ret = requests.get(url)
        meta_campaign_data=json.loads(ret.text)
        add_budget_from_adsetsAPI(meta_campaign_data,meta_campaigns)

    return meta_campaigns

def get_all_adsets_from_insightsAPI(adsets):
    all_adsets=[]

    for adset in adsets:

        new_adset = MetaAdset(adset['adset_id'],adset['adset_name'],adset['campaign_id'],adset['campaign_name'])
        if('spend' in adset):
            new_adset.add_spend(float(adset['spend']))
        all_adsets.append(new_adset)
    return all_adsets

def check_if_campaign_exists(campaigns,campaign_id):
    for campaign in campaigns:
        if(campaign_id==campaign.id):
            return True
    return False

def add_budget_from_adsetsAPI(insights_campaign,meta_campaigns):
    for meta_campaign in meta_campaigns:
        if(meta_campaign.id==insights_campaign['id']):
                meta_campaign.setEffectiveStatus(insights_campaign['effective_status'])

                #CBO ou impulsionado
                if 'daily_budget' in insights_campaign:
                    meta_campaign.set_budget(float("{:.2f}".format(float(insights_campaign['daily_budget'])/100.00)),True)
                    meta_campaign.cbo=True

                #campanha CBO com programacao nos conjuntos
                elif 'lifetime_budget' in insights_campaign: 
                    lifetime_budget=float("{:.2f}".format(float(insights_campaign['lifetime_budget'])/100.00))
                    start_time=datetime.fromisoformat(insights_campaign['start_time'])
                    stop_time=datetime.fromisoformat(insights_campaign['stop_time'])
                    days_campaign_duration=((datetime.date(start_time) - datetime.date(stop_time)).days)*-1
                    meta_campaign.set_budget(lifetime_budget,True)
                    meta_campaign.cbo=True

                #campanha normal                
                else:
                    if 'adsets' in insights_campaign: 
                        for insights_adset in insights_campaign['adsets']['data']:
                            for meta_adset in meta_campaign.adsets:
                                if(meta_adset.id==insights_adset['id']):
                                    meta_adset.setEffectiveStatus(insights_adset['effective_status'])
                                    meta_adset.set_budget(float("{:.2f}".format(float(insights_adset['daily_budget'])/100.00)))

    return 'ok'