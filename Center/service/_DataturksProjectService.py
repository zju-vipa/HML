import config
import requests
import json

class DataturksProjectService:

    # 创建dataturks的project
    def createProject(self, uid, token, name, taskType, rules):
        headers = {
            'Content-Type': 'application/json',
            'uid': uid,
            'token': token
        }

        data = {
            "name": name,
            "taskType": taskType,
            "rules": rules
        }

        url = config.DATATURKS_BASE + "/createProject"
        try:
            rep = requests.post(url=url, data=json.dumps(data),
                                headers=headers)  # post the backend of dataturks to get the login auth
            rep.raise_for_status()  # will raise error if http error, can't process in this way
            result = json.loads(rep.text)['response']
        except:
            result = None
        return result

    # 根据projectId获取project的标注状态
    def getProjectStatus(self, uid, token, projectId):
        headers = {
            'Content-Type': 'application/json',
            'uid': uid,
            'token': token
        }
        url = config.DATATURKS_BASE + "/{}}/getProjectStats".format(projectId)
        try:
            rep = requests.post(url=url, data=None,
                                headers=headers)  # post the backend of dataturks to get the login auth
            rep.raise_for_status()  # will raise error if http error, can't process in this way
            result = json.loads(rep.text)
        except:
            result = None
        # {'id': '2c9180827013b8f80170572f75a8000c', 'details': {'id': '2c9180827013b8f80170572f75a8000c', 'name': 'cigar', 'subtitle': None, 'orgId': '2c9180827013b8f8017050e5cc820004', 'orgName': 'test002', 'hasSubscriptionExpired': False, 'access_type': 'RESTRICTED', 'visibility_type': 'PRIVATE', 'task_type': 'IMAGE_CLASSIFICATION', 'taskRules': '{"tags":"a,b,c,d,e,f,g","instructions":"test description"}', 'totalHits': 0, 'totalHitsDone': 0, 'totalHitsSkipped': 0, 'totalHitsDeleted': 0, 'totalEvaluationCorrect': 0, 'totalEvaluationInCorrect': 0, 'description': None, 'shortDescription': None, 'created_timestamp': 1582010693000, 'contributorDetails': None, 'permissions': None}, 'posTaggingStats': None, 'textSummarizationStats': None, 'textClassificationStats': None, 'imageClassificationStats': {'laeblStats': []}, 'imageBoundingBoxStats': None, 'videoBoundingBoxStats': None, 'videoClassificationStats': None, 'documentTaggingStats': None}
        return result

    # 根据projectId获取project的详细信息
    def getProjectDetails(self, uid, token, projectId):
        headers = {
            'Content-Type': 'application/json',
            'uid': uid,
            'token': token
        }
        url = config.DATATURKS_BASE + "/{}/getProjectDetails".format(projectId)
        try:
            rep = requests.post(url=url, data=None,
                                headers=headers)  # post the backend of dataturks to get the login auth
            rep.raise_for_status()  # will raise error if http error, can't process in this way
            result = json.loads(rep.text)
        except:
            result = None
        # {'id': '2c9180827013b8f80170572f75a8000c', 'name': 'cigar', 'subtitle': None, 'orgId': '2c9180827013b8f8017050e5cc820004', 'orgName': 'test002', 'hasSubscriptionExpired': False, 'access_type': 'RESTRICTED', 'visibility_type': 'PRIVATE', 'task_type': 'IMAGE_CLASSIFICATION', 'taskRules': '{"tags":"a,b,c,d,e,f,g","instructions":"test description"}', 'totalHits': 0, 'totalHitsDone': 0, 'totalHitsSkipped': 0, 'totalHitsDeleted': 0, 'totalEvaluationCorrect': 0, 'totalEvaluationInCorrect': 0, 'description': None, 'shortDescription': None, 'created_timestamp': 1582010693000, 'contributorDetails': [{'userDetails': {'uid': 'CHo0tFRkKJBtGyAjtlmGpcH8r3eD', 'firstName': 'test002@qq.com', 'secondName': 'test002@qq.com', 'profilePic': None, 'email': 'test002@qq.com'}, 'hitsDone': 0, 'avrTimeTakenInSec': 0, 'role': 'OWNER'}], 'permissions': {'canSeeInsights': True, 'canSeeLeaderboard': True, 'canSeeCompletedHITs': True, 'canCompleteHITs': True, 'canInviteCollaborators': True, 'canDownloadData': True, 'canUploadData': True, 'canEditProject': True, 'canDeleteProject': True}}
        return result
