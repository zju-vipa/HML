from app import dataturksUserService
import config
import requests
import json

def test_register():
    firstName = secondName = 'test002'
    email = 'test002@qq.com'
    password = 'test002'
    auth = dataturksUserService.register(email, password)
    print(auth)

def test_login():
    from utils.EncryptUtil import encryptPassword
    email = 'test002@qq.com'
    password = 'test002'
    auth = dataturksUserService.login(email, encryptPassword(password))
    print(auth)

def test_getUserHome():

    headers = {
        'Content-Type': 'application/json',
        'uid': 'CHo0tFRkKJBtGyAjtlmGpcH8r3eD',
        'token': 'NaF1A6RLEc71V2Te4ovPSQK75eQIGBPtIjNCfy0Zmh4NV0iKhwRVGaXAsqaK54AY'
    }

    url = config.DATATURKS_BASE + "/getUserHome"

    rep = requests.post(url=url, data=None, headers=headers)  # post the backend of dataturks to get the login auth
    # rep.raise_for_status()  # will raise error if http error, can't process in this way
    result = json.loads(rep.text)

    print(result)

def test_createProject():

    headers = {
        'Content-Type': 'application/json',
        'uid': 'CHo0tFRkKJBtGyAjtlmGpcH8r3eD',
        'token': 'NaF1A6RLEc71V2Te4ovPSQK75eQIGBPtIjNCfy0Zmh4NV0iKhwRVGaXAsqaK54AY'
    }

    data = {
        "name": "cigar",
        "taskType": "IMAGE_CLASSIFICATION",
        "rules": "{\"tags\":\"a,b,c,d,e,f,g\",\"instructions\":\"test description\"}"
    }

    url = config.DATATURKS_BASE + "/createProject"

    rep = requests.post(url=url, data=json.dumps(data), headers=headers)  # post the backend of dataturks to get the login auth
    # rep.raise_for_status()  # will raise error if http error, can't process in this way
    result = json.loads(rep.text)
    print(result)

def test_getProjectStatus():
    headers = {
        'Content-Type': 'application/json',
        'uid': 'CHo0tFRkKJBtGyAjtlmGpcH8r3eD',
        'token': 'NaF1A6RLEc71V2Te4ovPSQK75eQIGBPtIjNCfy0Zmh4NV0iKhwRVGaXAsqaK54AY'
    }
    url = config.DATATURKS_BASE + "/2c9180827013b8f80170572f75a8000c/getProjectStats"

    rep = requests.post(url=url, data=None,
                        headers=headers)  # post the backend of dataturks to get the login auth
    # rep.raise_for_status()  # will raise error if http error, can't process in this way
    result = json.loads(rep.text)
    # {'id': '2c9180827013b8f80170572f75a8000c', 'details': {'id': '2c9180827013b8f80170572f75a8000c', 'name': 'cigar', 'subtitle': None, 'orgId': '2c9180827013b8f8017050e5cc820004', 'orgName': 'test002', 'hasSubscriptionExpired': False, 'access_type': 'RESTRICTED', 'visibility_type': 'PRIVATE', 'task_type': 'IMAGE_CLASSIFICATION', 'taskRules': '{"tags":"a,b,c,d,e,f,g","instructions":"test description"}', 'totalHits': 0, 'totalHitsDone': 0, 'totalHitsSkipped': 0, 'totalHitsDeleted': 0, 'totalEvaluationCorrect': 0, 'totalEvaluationInCorrect': 0, 'description': None, 'shortDescription': None, 'created_timestamp': 1582010693000, 'contributorDetails': None, 'permissions': None}, 'posTaggingStats': None, 'textSummarizationStats': None, 'textClassificationStats': None, 'imageClassificationStats': {'laeblStats': []}, 'imageBoundingBoxStats': None, 'videoBoundingBoxStats': None, 'videoClassificationStats': None, 'documentTaggingStats': None}
    print(result)

def test_getProjectDetails():
    headers = {
        'Content-Type': 'application/json',
        'uid': 'CHo0tFRkKJBtGyAjtlmGpcH8r3eD',
        'token': 'NaF1A6RLEc71V2Te4ovPSQK75eQIGBPtIjNCfy0Zmh4NV0iKhwRVGaXAsqaK54AY'
    }
    url = config.DATATURKS_BASE + "/2c9180827013b8f80170572f75a8000c/getProjectDetails"

    rep = requests.post(url=url, data=None,
                        headers=headers)  # post the backend of dataturks to get the login auth
    # rep.raise_for_status()  # will raise error if http error, can't process in this way
    result = json.loads(rep.text)
    # {'id': '2c9180827013b8f80170572f75a8000c', 'name': 'cigar', 'subtitle': None, 'orgId': '2c9180827013b8f8017050e5cc820004', 'orgName': 'test002', 'hasSubscriptionExpired': False, 'access_type': 'RESTRICTED', 'visibility_type': 'PRIVATE', 'task_type': 'IMAGE_CLASSIFICATION', 'taskRules': '{"tags":"a,b,c,d,e,f,g","instructions":"test description"}', 'totalHits': 0, 'totalHitsDone': 0, 'totalHitsSkipped': 0, 'totalHitsDeleted': 0, 'totalEvaluationCorrect': 0, 'totalEvaluationInCorrect': 0, 'description': None, 'shortDescription': None, 'created_timestamp': 1582010693000, 'contributorDetails': [{'userDetails': {'uid': 'CHo0tFRkKJBtGyAjtlmGpcH8r3eD', 'firstName': 'test002@qq.com', 'secondName': 'test002@qq.com', 'profilePic': None, 'email': 'test002@qq.com'}, 'hitsDone': 0, 'avrTimeTakenInSec': 0, 'role': 'OWNER'}], 'permissions': {'canSeeInsights': True, 'canSeeLeaderboard': True, 'canSeeCompletedHITs': True, 'canCompleteHITs': True, 'canInviteCollaborators': True, 'canDownloadData': True, 'canUploadData': True, 'canEditProject': True, 'canDeleteProject': True}}
    print(result)