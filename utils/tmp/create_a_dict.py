
def create_upd_dict():
  upd_dict = {
    "command": "UPDATE_STATUS",
    "documentId": "",
    "status": "TASK_STARTED",
    "task": "optimize",
    "managedStudyId": "NV_JOB_29e9f079-8f05-4715-98d1-8d247e308a4f",
    "jobId": "NV_JOB_29e9f079-8f05-4715-98d1-8d247e308a4f_1",
    "updateTime": "2020-03-23 09:20:14.314139",
    "body": "",
    "user": "airflow1234",
    "modelId": "model0001",
    "modelName": "test_model.prt",
    "studyId": "NV_STUDY_a4125ddf-a84c-4cf6-9af2-9763fb679393",
    "totalJobs": 1,
    "jobStartId": 1,
    "appliedParams": [],
    "taskId": "none",
    "files": {
      "model_zip": {
        "location": "/user_airflow1234/study_NV_STUDY_a4125ddf-a84c-4cf6-9af2-9763fb679393/inputs/model.zip",
        "foreignId": "5e7831d1c9fd514aa93bd3a9"
      },
    }
  }
  return upd_dict
