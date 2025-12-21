class Validation:

    def nullOrEmpty(data):
        if data == "" or data == "null" or data == None:
            return None
        else:
            return data