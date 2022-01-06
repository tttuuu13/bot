from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
import boto3


s3 = boto3.client('s3', 
                  aws_access_key_id=AWS_ACCESS_KEY_ID, 
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY
                  )


def upload_file(file, file_name):
    try:
        s3.upload_fileobj(file, "formulas-for-bot", file_name)
    except Exception as e:
        return e
    return True


def download_file(file_name, save_as):
    s3.download_file("formulas-for-bot", file_name, save_as)