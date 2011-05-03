class ActionController(object):

    def __init__(self):
        pass
        
    def update(self, obj, params):
        obj.update_attributes(params)
    
    def destroy(self, obj):
        del(obj)
