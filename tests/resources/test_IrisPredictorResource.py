
import pytest
from resources.IrisPredictorResource import error_output, ok_output
import falcon



class Response():
    def __init__(self):
        self.status = None
        self.body = None

@pytest.fixture
def resp():
    return Response()

@pytest.mark.parametrize("falcon_400_status, error_message",[   
     (falcon.HTTP_400 ,"somthing" ),
     (falcon.HTTP_400,"other_thing" )])


def test_error_output(resp, falcon_400_status, error_message): 
    resp = error_output(resp, error_message)
    assert resp.status == falcon_400_status
    assert resp.body == error_message











# class Response():
#     def __init__(self):
#         self.status = None
#         self.body = None


# @pytest.fixture
# def resp_dict():
#     resp = Response()
#     return resp

# @pytest.mark.parametrize("falcon_400_status, error_message",[   
#     (falcon.HTTP_400 ,"somthing" ),
#     (falcon.HTTP_400,"other_thing" )])

# def test_error_output(resp_dict, falcon_400_status, error_message):
#     resp_dict = error_output(resp_dict, error_message)
#     assert resp_dict.status == falcon_400_status
#     assert resp_dict.body == error_message

# @pytest.mark.parametrize("falcon_200_status, results",[   
#     (falcon.HTTP_200 ,"somthing" ),
#     (falcon.HTTP_200,"other_thing" )])

# def test_error_output(resp_dict, falcon_200_status, results):
#     resp_dict = ok_output(resp_dict, results)
#     assert resp_dict.status == falcon_200_status