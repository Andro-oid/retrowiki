# TODO(Project 1): Implement Backend according to the requirements.
# Imports the Google Cloud client library
from google.cloud import storage


class Backend:

    def __init__(self):
        # Instantiates a client
        storage_client = storage.Client()
        # The name for the new bucket
        bucket_name1 = "group_wiki_content"
        bucket_name2 = "users_and_passwords"

        #Creating the buckets
        #The bucket already exists, it just needs a name
        self.bucket = storage_client.bucket(bucket_name1)
        self.bucket = storage_client.bucket(bucket_name2)
        
    def get_wiki_page(self, name):
        pass

    def get_all_page_names(self):
        pass

    def upload(self):
        pass

    def sign_up(self):
        pass

    def sign_in(self):
        pass

    def get_image(self):
        pass

