# TODO(Project 1): Implement Backend according to the requirements.
from google.cloud import storage
from google.cloud.storage.blob import Blob


class Backend:
    def __init__(self, opener = open):
        self.storage_client = storage.Client()

        
        self.bucketName_content = "group_wiki_content"
        self.bucketName_users = "users_and_passwords"


        self.bucket_content = self.storage_client.bucket(self.bucketName_content)
        self.bucket_users = self.storage_client.bucket(self.bucketName_users)      
        
    def get_wiki_page(self, name):
        blob = self.bucket_content.blob(name)
        with blob.open("r") as f:
            print(f.read())
        

    def get_all_page_names(self):
        pages = []
        blobs = self.storage_client.list_blobs(self.bucketName_content) 
        for blob in blobs:
            pages.append(blob.name)
        return pages

    def upload(self, content, name):
        """Uploads content into the group_wiki_content bucket

        It should be able to store text and pictures
        Attributes
            content: the wikipage
            name:  the id of the wikipage 
        """          
        blob = self.bucket_content.blob(name)
        blob.upload_from_file(content)
        # with blob.open("w") as f:
        #     f.write(content)        



    def sign_up(self, username, password):        
        if self.user_exists(username):
            return False

        blob = self.bucket_users.blob(username)
        with blob.open("w") as f:
            f.write(password)
        return True

    def user_exists(self, username):
        blobs = self.storage_client.list_blobs(self.bucketName_users) 
        for blob in blobs:
            if blob.name == username:
                return True
        return False


    def sign_in(self, username, password):
            
        if not self.user_exists(username):
            return False

        blobContent = self.bucket_users.blob(username) 

        #compare passwords
        with blobContent.open("r") as f:
            blobPassword = f.read()
            for line in blobPassword:
                if blobPassword == password:
                    return True
        return False

    def get_image(self, imageName):
        blob = self.bucket_content.blob(self.bucketName_content+"/"+imageName)
        image = None
        with blob.open("r") as f:
            image = f.read()
        return image



