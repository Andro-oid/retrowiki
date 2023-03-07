# TODO(Project 1): Implement Backend according to the requirements.
from google.cloud import storage
from google.cloud.storage.blob import Blob

class Backend:
    def __init__(self, st = storage ):
        self.storage_client = st.Client()
        
        self.bucketName_content = "group_wiki_content"
        self.bucketName_users = "users_and_passwords"
        self.bucketName_images = "author_images"


        self.bucket_content = self.storage_client.bucket(self.bucketName_content)
        self.bucket_users = self.storage_client.bucket(self.bucketName_users)   
        self.bucket_images = self.storage_client.bucket(self.bucketName_images)  
        #self.readContent = opener      
        #self.writeContent = opener      
        #self.readUser = opener      
        #self.writeUser = opener

            
        
    def get_wiki_page(self, name):
        blob = self.bucket_content.blob(name)
        with blob.open("r") as f:
            return(f.read())
        

    def get_all_page_names(self):
        pages = []
        blobs = self.storage_client.list_blobs(self.bucketName_content) 
        for blob in blobs:
            pages.append(blob.name)
        return pages

    def upload(self, content, name):         
        blob = self.bucket_content.blob(name)
        blob.upload_from_file(content)
        # with blob.open("w") as f:
        #     f.write(content)        





    def sign_up(self, username, password): 
        """This methods checks that a given the user matches the hashed password in bucket_users.

        Attributes:
            username: A string indicading the blob to look for.
            password: A string corresponding to the content of the blob.
        
        Returns:
            A boolean value indicating if the hashed password matches the user
        """
        if self.user_exists(username):
            return False

        blob = self.bucket_users.blob(username)
        #with self.writeUser( blob, "w") as f:
        with blob.open("w") as f:
            f.write(password)
        return True

    def user_exists(self, username):
        """This methods checks if an user exists in the data base in bucket_users.

        Attributes:
            username: A string indicading the blob to look for.
        
        Returns:
            A boolean value that indicates if the username is already registered.
        """
        blobs = self.storage_client.list_blobs(self.bucketName_users) 
        
        for blob in blobs:
            if blob.name == username:
                return True
        return False


    def sign_in(self, username, password):
            
        if not self.user_exists(username):
            return False

        blobUsers = self.bucket_users.blob(username)

        #compare passwords
        with blobUsers.open("r") as f:
            blobPassword = f.read()
            #for line in blobPassword:
            if blobPassword == password:
                return True
        return False

    def get_image(self, imageName):
        blob = self.bucket_images.blob(imageName)
        image = None
        
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        with blob.open("rb") as f:
            # print(f.read())
            image = f.read()
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return image
    


