# TODO(Project 1): Implement Backend according to the requirements.
from google.cloud import storage


class Backend:

    def __init__(self, opener = open):
        self.storage_client = storage.Client()
        self.bucketName_content = "group_wiki_content"
        self.bucketName_users = "users_and_passwords"
        self.bucket_content = self.storage_client.bucket(self.bucketName_content)
        self.bucket_users = self.storage_client.bucket(self.bucketName_users)      
        
    def get_wiki_page(self, name):
        blob = self.bucket_content.blob(self.bucketName_content+"/"+name)
        with blob.open("r") as f:
            print(f.read())

    def get_all_page_names(self):
        blobs = self.bucket_content.list_blobs(self.bucketName_content)        
        for blob in blobs:
            print(blob.name)

    def upload(self, content, name):
        """Uploads content into the group_wiki_content bucket

        It should be able to store text and pictures
        Attributes
            content: 
        """  
        #The blob will be the name of the object the bucket will use to identify it
        blob = self.bucket_content.blob(self.bucketName_content+"/"+name)
        print(f"Bucket {self.bucketName_content} created.")
        with blob.open("w") as f:
            print(f"Bucket {self.bucketName_content} created.")
            f.write(content)        
        print(f"Bucket {self.bucketName_content} created.")



    def sign_up(self, username, password):
        blob = self.bucket_users.blob(self.bucketName_users+"/"+username)
        with blob.open("w") as f:
            f.write(password)

    def sign_in(self, username, password):
        blob = self.bucket_content.blob(self.bucketName_content+"/"+username)
        matched = False
        with blob.open("r") as f:
            retrievedPassword = f.read()
            print(retrievedPassword)
            if retrievedPassword is password:
                matched = True
        return matched


    def get_image(self, imageName):
        blob = self.bucket_content.blob(self.bucketName_content+"/"+imageName)
        image = None
        with blob.open("r") as f:
            image = f.read()
        return image



