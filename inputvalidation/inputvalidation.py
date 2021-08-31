# crating a class for validating user input
from setuplogger import setup_logger


class InputValidation():
    def __init__(self, seacrch_query, num_of_images):
        self.log = setup_logger.setup_logger("inputValidation_LOG", "inputValidation.log")
        self.search_query = seacrch_query
        self.num_of_images = num_of_images


    def validate_search_query(self):
        """This method will validate search query"""
        try:
            self.log.info("Validating search query")
            if self.search_query is None or self.search_query == "":
                self.log.error("Search query is empty")
                raise ValueError("Search query cannot be empty")

            else:  
                self.log.info("Search query is valid")
        except ValueError as err:
            self.log.error(err)
            raise err

    def validate_num_of_images(self):
        """This method will validate number of images"""
        try:
            self.log.info("Validating number of images")
            if type(self.num_of_images) is not int:
                self.log.error("Number of images is not an integer")
                raise ValueError("Number of images not integer")
            else:
                self.log.info("Number of images is valid")
        except ValueError as err:
            self.log.error(err)
            raise err