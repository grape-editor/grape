class ActiveModel(object):

    def __init__(self, params):
        self.update_attributes(params)

    def update_attributes(self, params):
        for attr in self.__dict__:
            if attr in params:
                self.__dict__[attr] = params[attr]
    
