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
        """ This method gets the content of a given wiki page from the content bucket.

        Args:
            name: A string corresponding to the name of the wiki page (txt file).
        
        Returns:
            The content of the wiki page as a string.
        """
        blob = self.bucket_content.blob(name + ".txt")
        with blob.open("r") as f:
            return(f.read())
        

    def get_all_page_names(self):
        pages = []
        blobs = self.storage_client.list_blobs(self.bucketName_content) 
        for blob in blobs:
            pages.append(blob.name[:len(blob.name) - 4])
        return pages

    def upload(self, content, name):
        """This method uploads the content of a wiki page to the content bucket.

        Args:
            content: A string corresponding to the content of the wiki page.
            name: A string corresponding to the name of the wiki page.
        """      
        blob = self.bucket_content.blob(name)
        blob.upload_from_file(content)
        # with blob.open("w") as f:
        #     f.write(content)        





    def sign_up(self, username, password): 
        """This methods checks that a given the user matches the hashed password in bucket_users.

        Attributes:
            username: string indicading the blob to look for.
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
        """ This method adds a new user to the users and passwords bucket.

        Args:
            username: string corresponding to the username of the new user.
            password: A string corresponding to the hashed password of the new user.
        
        Returns:
            A boolean value indicating if the user was successfully added.
        """  
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
        """ This method retrieves the image with the given image name from the author_images bucket.

        Args:
            imageName: A string corresponding to the name of the image to retrieve.

        Returns:
            an object representing the image file.
        """

        blob = self.bucket_images.blob(imageName)
        image = None
        with blob.open("r") as f:
            print(f.read())
            image = f.read()
        return image
    


