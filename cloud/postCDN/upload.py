from fileinput import filename
import os
import boto3

def main(args):

    class FileName:
        name = ''

        def __init__(self, name):
            self.name = name
    
    file = args.file
    fileName = FileName(args.file)
    tags = args.tags

    session = boto3.session.Session()
    client = session.client('s3',
                            endpoint_url='https://nyc3.digitaloceanspaces.com',
                            region_name='nyc3', 
                            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

    client.put_object(Bucket='do-example', 
                    Key='videos/' + fileName, 
                    Body=open(file,'rb'), 
                    ACL='private', 
                    Metadata={ 
                        'x-amz-meta-my-key': tags
                    }
                    )
    
    return {"body": {
        "201": "You have successfully uploaded the file"
        }}
