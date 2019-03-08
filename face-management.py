#!/usr/bin/env python

### Put your code below this comment ###
import AzureCSLib as az
import sys 

def GetParams():
    import json
    with open('faceapi.json') as jsonFile:
        key = json.load(jsonFile)['key']
    with open('faceapi.json') as jsonFile:
        group = json.load(jsonFile)['groupId']
    with open('faceapi.json') as jsonFile:
        baseURL = json.load(jsonFile)['serviceUrl']
    return az.FaceAPIsession(key, baseURL, group)

def SimpleAdd(session, video):
    try:
        personID, facesID, count = session.CreateAnonPerson(video)
        session.UpdateGroupData("Updated")
        print('{1} frames extracted{0}PersonId: {2}{0}FaceIds{0}======={0}{3}'.format('\n', count, personID, '\n'.join([x['persistedFaceId'] for x in facesID])))
    except (az.FacesCountError, az.FramesCountError):
        print('Video does not contain any face')
    except az.PersonExistError as exc:
        print(exc.message)

def GetPersonList(session):
    try:
        session.CheckGroupExist()
        print('\n'.join(session.GetPersonList()))
    except az.PersonGroupExistError as pgee:
        print(pgee.message)
    

def DeletePerson(session, personID):
    try:
        session.DeletePerson(personID=personID)
        session.UpdateGroupData("Updated")
    except az.PersonExistError:
        print('Person with id {0} does not exist'.format(personID))

def Train(session):
    if session.CheckGroupUpdation():
        print('Training task for {0} persons started'.format(session.StartTrain()))
        session.UpdateGroupData('Don\'t updated')
    else:
        print('System does not updated')

def UnsaveAuth(session, video):
    try:
        personID = session.IdentifyPerson(video)
        print(personID)
    except az.SystemReadinessError:
        print('System does not trained')
    except az.LowDegreeOfConfidenceError:
        print('The person cannot be identified')
    except az.PersonExistError:
        print('The person cannot be identified')
    except az.FacesCountError:
        print('The person cannot be identified')
    except az.FramesCountError:
        print('The person cannot be identified')

def Main():
    session = GetParams()
    temp = sys.argv
    if temp[1] == '--simple-add':
        SimpleAdd(session, temp[2])

Main()
