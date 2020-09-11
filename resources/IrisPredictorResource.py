import pickle
import sklearn
from sklearn.neighbors import KNeighborsClassifier
import json
import numpy as np
import falcon


def error_output(resp, messsage):
    resp.status = falcon.HTTP_400
    resp.body = messsage
    return resp

def ok_output(resp, results):
    resp.status = falcon.HTTP_200
    resp.body = json.dumps(results) + '\n'
    return resp

def predict_knn(features, model):

    """
    This function gets the features and models and predicts the output
    Args:
        features(list): list of features. It must include 4 floating numbers
        model(sklearn model): knn sklearn model, loaded from models folder
    output:    
        prediceted_class(str)
    """
    
    classes = ['setosa', 'versicolor', 'virginica']
    listed_features = [features]
    predicted_class = model.predict(listed_features)[0]
    return classes[predicted_class]

### resource
class IrisPredictorResource():
    def __init__(self, model_path, logger):
        self.logger = logger
        self.model = pickle.load(open(model_path, 'rb'))
        self.logger.info("Starting: IrisPredictor")
    
    def on_post(self, req, resp):
        """
        This method checks: 
            0) read the json file
            1) check if 'features' exists 
            2) check if the feature list is valid
            3) predicts the results
            4) Sends back the results
        """
        try:
            self.logger.info("IrisPredictor: reading file")
            request_bytes = req.stream.read()

            try:
                request = json.loads(request_bytes.decode("utf-8"))
            
            except Exception as e:
                self.logger.error(e, exc_info=True)
                resp = error_output(resp, "Invalid JSON\n") 
                return
        
            if "features" not in request:
                resp = error_output(resp, "Invalid JSON\n") 
                return                

            features = request["features"]
            
            if not isinstance(features, list):
                resp = error_output(resp, "Invalid JSON. \
                                        'features' must be a list \n")  
                return  
            
            if len(features) != 4:
                resp = error_output(resp, "Invalid features list. 'features' length must be 4 \n")  
                return  

            prediction = predict_knn(features, self.model)
            self.logger.info('IrisPredictor: the prediction is %s' % prediction)
            results = {"predicted_class": prediction}
            self.logger.info('IrisPredictor: Sending the results \n')
            
            resp = ok_output(resp, results) 

        except Exception as e:
            self.logger.error(e, exc_info=True)
            resp.status = falcon.HTTP_500