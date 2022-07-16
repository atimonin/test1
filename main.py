import os.path
import flask
import json
import requests
import werkzeug.datastructures
import itertools
from google.cloud import datastore
from collections import OrderedDict


app = flask.Flask(__name__)

@app.route('/liveness', methods=['GET'])
def liveness():
    return 'Alive'

@app.route('/', methods=['GET'])
def root():
    return 'SizeRecommendation needs a classId and loginId as part of the path!'

@app.route('/classId/<classId>/loginId/<loginId>')
def product_model_productId(classId,loginId):
    loginId= loginId + '_loginId'
    modelType='SizeRecommendation'
    response={'recs_data':{'SizeRecommendation':reco_lookup(modelType, classId, loginId)}}
    return (json.dumps(response), 200, {"access-control-allow-origin": "*", "content-type": "application/json"})
            
def reco_lookup(modelType, classId, loginId):
    datastore_client= datastore.Client()
    try:
        id = classId + '-' + loginId
        query = datastore_client.query(kind=modelType)
        first_key = datastore_client.key(modelType, id )
        query.key_filter(first_key, '=')
        
        result= list(query.fetch(limit=1))
        
        if not result:
            query_default = datastore_client.query(kind=modelType)
            default_ds_key='0'
            second_key=datastore_client.key(modelType, default_ds_key)
            query_default.key_filter(second_key, '=')
            result= list(query_default.fetch(limit=1))
            if not result:
                result=None
                return result
            else:
                return result
        else:
            return result
    except Exception as e:
        print('hit an exception in reco_lookup')
        return print(repr(e))
    

    
# def main(request):
#     with app.app_context():
#         headers = werkzeug.datastructures.Headers()
#         for key, value in request.headers.items():
#             headers.add(key, value)
#         with app.test_request_context(method=request.method, base_url=request.base_url, path=request.path, query_string=request.query_string, headers=headers, data=request.form):
#             try:
#                 rv = app.preprocess_request()
#                 if rv is None:
#                     rv = app.dispatch_request()
#             except Exception as e:
#                 rv = app.handle_user_exception(e)
#             response = app.make_response(rv)
#             return app.process_response(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000)