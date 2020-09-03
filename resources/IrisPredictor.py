import pickle
import sklearn
from sklearn.neighbors import KNeighborsClassifier
import json
import numpy as np
import falcon



def predict_knn(features, model):
    classes = ['setosa', 'versicolor', 'virginica']
    listed_features = [features]
    predicted_class = model.predict(listed_features)[0]
    return classes[predicted_class]

### resource
class IrisPredictor():
    def __init__(self, model_path, logger):
        self.logger = logger
        self.model = pickle.load(open(model_path, 'rb'))
        self.logger.info("Starting: IrisPredictor")
    
    def on_post(self, req, resp):
        try:
            self.logger.info("IrisPredictor: reading file")
            request_bytes = req.stream.read()

            try:
                request = json.loads(request_bytes.decode("utf-8"))
            
            except Exception as e:
                self.logger.error(e, exc_info=True)
                resp.status = falcon.HTTP_400
                resp.body = "Invalid JSON\n"
                return
        
            if "features" not in request:
                resp.status = falcon.HTTP_400
                resp.body = "Invalid JSON\n"
                return                

            features = request["features"]
            
            if not isinstance(features, list):
                resp.status = falcon.HTTP_400
                resp.body = "Invalid JSON. 'features' must be a list \n"
                return  
            
            if len(features) != 4:
                resp.status = falcon.HTTP_400
                resp.body = "Invalid features list. 'features' length must be 4 \n"
                return  

            prediction = predict_knn(features, self.model)
            self.logger.info('IrisPredictor: the prediction is %s' % prediction)
            response = {"predicted_class": prediction}
            self.logger.info('IrisPredictor: Sending the results \n')
            
            resp.status = falcon.HTTP_200
            resp.body = json.dumps(response) + '\n'

        except Exception as e:
            self.logger.error(e, exc_info=True)
            resp.status = falcon.HTTP_500