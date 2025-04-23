from datetime import date
from datetime import datetime
from calendar import monthrange

class MessageBuilder:
    client_name=''
    businessmanagers=[]
    google_accounts=[]
    CANAL_SLACK="C05TGRE3C3Y"


    def __init__(self, client_name):
        self.client_name = client_name
        self.businessmanagers=[]
        self.google_accounts=[]

    def count_meta_adaccounts(self):
        number_adaccounts=0
        for  businessmanager in self.businessmanagers:
            for adaccount in businessmanager.adaccounts:
                number_adaccounts=number_adaccounts+1
        return number_adaccounts

    def count_meta_campaigns(self):
        number_campaigns=0
        for  businessmanager in self.businessmanagers:
            for adaccount in businessmanager.adaccounts:
                for camapign in adaccount.campaigns:
                    number_campaigns=number_campaigns+1
        return number_campaigns

    def count_google_campaigns(self):
        number_campaigns=0
        for  adaccount in self.google_accounts:
            for campaign in adaccount.campaigns:
                if(campaign.effectiveStatus==2):
                    number_campaigns=number_campaigns+1
        return number_campaigns

    def set_businessmanagers(self, businessmanagers):
        for  businessmanager in businessmanagers:
            self.businessmanagers.append(businessmanager)

    def set_google_accounts(self, google_accounts):
        for  google_account in google_accounts:
            self.google_accounts.append(google_account)

    def calculate_total_projection(self):
        absolute_total_spend=0
        absolute_total_budget=0

        for businessmanager in self.businessmanagers:
            absolute_total_spend=absolute_total_spend+businessmanager.calculate_total_spend()
            absolute_total_budget=absolute_total_budget+businessmanager.calculate_total_budget()

        for google_account in self.google_accounts:
            absolute_total_spend=absolute_total_spend+google_account.get_total_cost()
            absolute_total_budget=absolute_total_budget+google_account.get_total_budget()  

        today = date.today()
        last_day_this_month=monthrange(today.year, today.month)[1]

        days_left_this_month=((date(today.year, today.month, today.day) - date(today.year, today.month, last_day_this_month)).days)*-1
        total_spend_projected=0


        total_spend_projected=absolute_total_spend+(absolute_total_budget*days_left_this_month)

        return {
            "account_budget":"{:.2f}".format(float(absolute_total_budget)),
            "account_cost":"{:.2f}".format(float(absolute_total_spend)),
            "total_spend_projected":"{:.2f}".format(float(total_spend_projected))
        }


    def build_message(self):
        message=""
        today_date=date.today().strftime("%d/%m/%y")
        if(len(self.google_accounts)==0 and len(self.businessmanagers)==0):
            message+= f"[🔴 No google account set up for {self.client_name} - {today_date} 🍊] \n"

            return message

        projection=self.calculate_total_projection()

        message+= f"[🍊 Consolidated Projection {self.client_name} - {today_date} 🍊] \n \n"
        message+= f"👥 Daily Budget: R$ {projection['account_budget']}; \n"
        message+= f"💸 Total spent: R$ {projection['account_cost']}; \n"
        message+= f"📈 Spend Projection: R$ {projection['total_spend_projected']}; \n"

        if(len(self.businessmanagers)==0):
            message+= "\n [🔴 No Meta accounts set up] \n"
        else:
            message+="\n [Meta Ads] \n"

            message+=f"{len(self.businessmanagers)} Business Managers watched: \n"

            for bm in self.businessmanagers:                                
                message+= f"➡️ {bm.meta_businessmanager_name} \n"
                total_spend=float("{:.2f}".format(float(bm.calculate_total_spend())))
                total_budget=float("{:.2f}".format(float(bm.calculate_total_budget())))
                message+= f"💸 Total spent: R$ {total_spend} \n"
                message+= f"💰 Current budget: R$ {total_budget} \n"

            message+= f"\n {self.count_meta_adaccounts()} ad accounts: \n"

            for bm in self.businessmanagers:
                for adaccount in bm.adaccounts:
                    message+= f"\n ➡️ {adaccount.name} - {len(adaccount.campaigns)} campaigns \n"

                    total_spend=float("{:.2f}".format(float(adaccount.get_total_spend())))
                    total_budget="{:.2f}".format(float(adaccount.get_total_budget()))
                    message+= f"💸 Total spent: R$ {total_spend} \n"
                    message+= f"💰 Current budget: R$ {total_budget} \n"

                    campaigns_list=""
                    for campaign in adaccount.campaigns:
                        campaign_total_spend=float("{:.2f}".format(float(campaign.get_total_spend())))
                        campaign_total_budget=float("{:.2f}".format(float(campaign.get_total_budget())))
                        if campaign.effectiveStatus=="ACTIVE":
                            status="🟢: ACTIVE"
                        else:
                            status="🔴: PAUSED"
                            
                        campaigns_list=campaigns_list+f"➡️ {campaign.name} \n 💸: R$ {campaign_total_spend} - 💰: R$ {campaign_total_budget} - {status} \n"

                    if campaigns_list=="":
                        campaigns_list="no campaigns \n"
                    message+= campaigns_list

        #Google
        if(len(self.google_accounts)==0):
            message+= "\n [🔴 No Google Accounts set up] \n\n",
        else:

            message+= "\n [Google Ads] \n"

            message+= f"{len(self.google_accounts)} Google accounts: \n"
            for account in self.google_accounts:
                message+= f"➡️ {account.account_id} - {self.count_google_campaigns()} campaigns \n"
                total_spend=float("{:.2f}".format(float(account.get_total_cost())))
                message+= f"💸 Total spent: R$ {total_spend} \n"
                message+=   f"💰 Current budget: R$ {account.get_total_budget()} \n"

                campaigns_list=""
                for campaign in account.campaigns:
                    if(campaign.effectiveStatus==2):
                        campaign_total_spend=float("{:.2f}".format(float(campaign.get_total_cost())))
                        campaign_total_budget=float("{:.2f}".format(float(campaign.get_total_budget())))
                        campaigns_list=campaigns_list+f"➡️ {campaign.campaign_name} \n 💸: R$ {campaign_total_spend} 💰: R$ {campaign_total_budget} \n\n"

                if campaigns_list=="":
                    campaigns_list="no campaigns \n"
                message+=campaigns_list
            
        return message