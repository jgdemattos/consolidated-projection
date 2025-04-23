import requests
import json
import csv

def request_client_data(id):
    client={}
    try:
        with open('clients.csv', 'r') as csvfile:
            reader = csv.DictReader(f=csvfile, delimiter=';')
            for row in reader:
                if row['id'] == id:
                    client = {
                        'id': row['id'],
                        'name': row['name'],
                        'meta_id': row['meta_id'],
                        'google_id': row['google_id'],
                        'meta_adaccount_ids': row['meta_adaccount_ids'],
                    }
        if not client: 
            print("ERROR: client not found")
            raise ValueError("client not found")
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    return client