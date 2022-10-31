# Step 1: Import the all necessary libraries and SDK commands.
import os
import boto3
from dotenv import load_dotenv

load_dotenv()

accessKeyId = os.getenv('AWS_ACCESS_KEY_ID')
secretKey = os.getenv('AWS_SECRET_ACCESS_KEY')


# Step 2: The new session validates your request and directs it to your Space's specified endpoint using the AWS SDK.
session = boto3.session.Session()
client = session.client('s3',
                        endpoint_url='https://nyc3.digitaloceanspaces.com', # Find your endpoint in the control panel, under Settings. Prepend "https://".
                        region_name='nyc3', # Use the region in your endpoint.
                        aws_access_key_id=accessKeyId, # Access key pair. You can create access key pairs using the control panel or API.
                        aws_secret_access_key=secretKey) # Secret access key defined through an environment variable.

# Step 3: Call the put_object command and specify the file to upload.
client.put_object(Bucket='do-example', # The path to the directory you want to upload the object to, starting with your Space name.
                  Key='videos/sammy.png', # Object key, referenced whenever you want to access this file later.
                  Body=open('sammy.png','rb'), # The object's contents.
                  ACL='private', # Defines Access-control List (ACL) permissions, such as private or public.
                  Metadata={ # Defines metadata tags.
                      'x-amz-meta-my-key': 'your-value'
                  }
                )