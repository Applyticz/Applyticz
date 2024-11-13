import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv('GOOGLE_CLOUD_API_KEY')
API_URL = 'https://kgsearch.googleapis.com/v1/entities:search'


def get_company_info(text):
    params = {
        'query': text,
        'limit': 1,
        'indent': True,
        'key': API_KEY,
    }
    response = requests.get(API_URL, params=params)
    
    # Print the request URL to debug
    print("Request URL:", response.url)
    
    if response.status_code == 200:
        data = response.json()
        
        if 'itemListElement' in data and len(data['itemListElement']) > 0:
            entity = data['itemListElement'][0].get('result', {})
            company_name = entity.get('name')
            description = entity.get('description', 'No description available')
            detailed_description = entity.get('detailedDescription', {}).get('articleBody', 'No details available')
            entity_id = entity.get('@id', 'No ID available')
            
            return {
                'company_name': company_name,
                'description': description,
                'detailed_description': detailed_description,
                'entity_id': entity_id,
            }
        else:
            return {'error': 'No results found'}
    else:
        return {'error': f"Failed to fetch data. Status code: {response.status_code}"}


# Test with a simpler query
sample_text = "Thank you for applying to Twitter. We are excited to review your application."
company_info = get_company_info(sample_text)

print("Company Information:", company_info)
