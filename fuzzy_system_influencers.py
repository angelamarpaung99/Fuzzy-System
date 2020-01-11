import pandas as pd
import csv
from matplotlib import pyplot as plt 

def getData():
    data = pd.read_csv("influencers.csv")
    data.head(100)
    return data

def inferenceRule(follower, engagement):
    if (follower == 'many' and engagement == 'high'):
        influencer = 'accepted'
    elif (follower == 'many' and engagement == 'average'):
        influencer = 'accepted'
    elif (follower == 'many' and engagement == 'low'):
        influencer = 'considered'
    elif (follower == 'moderate' and engagement == 'high'):
        influencer = 'accepted'
    elif (follower == 'moderate' and engagement == 'average'):
        influencer = 'considered'
    elif (follower == 'moderate' and engagement == 'low'):
        influencer = 'considered'
    elif (follower == 'little' and engagement == 'high'):
        influencer = 'rejected'
    elif (follower == 'little' and engagement == 'average'):
        influencer = 'rejected'
    elif (follower == 'little' and engagement == 'low'):
        influencer = 'rejected'
    return influencer

def fuzzifikasiFollowerCount(followerCount):
    score = [0 for x in range(3)]
    if (followerCount <= 20000):
        score[0] = 1
        score[1] = 0
        score[2] = 0
    elif (followerCount > 20000 and followerCount < 30000):
        score[0] = -((followerCount - 30000)/ 10000)
        score[1] = ((followerCount - 20000)/ 10000)
        score[2] = 0
    elif (followerCount >= 30000 and followerCount <= 50000):
        score[0] = 0
        score[1] = 1
        score[2] = 0
    elif (followerCount>50000 and followerCount < 60000):
        score[0] = 0
        score[1] = -((followerCount-70000)/10000)
        score[2] = ((followerCount -60000)/10000)
    else:
        score[0] = 0
        score[1] = 0
        score[2] = 1
    return score

def fuzzifikasiEngagementRate(engagementRate):
    score = [0 for x in range(3)]
    if (engagementRate <= 2):
        score[0] = 1
        score[1] = 0
        score[2] = 0
    elif (engagementRate > 2 and engagementRate < 3):
        score[0] = -((engagementRate - 3)/1)
        score[1] = ((engagementRate - 2)/1)
        score[2] = 0
    elif (engagementRate>= 3 and engagementRate <=5 ):
        score[0] = 0
        score[1] = 1
        score[2] = 0
    elif (engagementRate > 5 and engagementRate < 6):
        score[0] = 0
        score[1] = -((engagementRate- 7)/1)
        score[2] = ((engagementRate-6)/1)
    else:
        score[0] = 0
        score[1] = 0
        score[2] = 1
    return score

def inferensi(followerCount, engagementRate):
    follower = fuzzifikasiFollowerCount(followerCount)
    engagement = fuzzifikasiEngagementRate(engagementRate)
    
    inference = [[0 for x in range(4)] for y in range(9)]
    inference[0][0] = follower[0]
    inference[0][1] = engagement[0]
    inference[0][2] = inferenceRule('little', 'low')
    inference[0][3] = min(follower[0], engagement[0])
    
    inference[1][0] = follower[0]
    inference[1][1] = engagement[1]
    inference[1][2] = inferenceRule('little', 'average')
    inference[1][3] = min(follower[0], engagement[1])
    
    inference[2][0] = follower[0]
    inference[2][1] = engagement[2]
    inference[2][2] = inferenceRule('little', 'high')
    inference[2][3] = min(follower[0], engagement[2])
    
    inference[3][0] = follower[1]
    inference[3][1] = engagement[0]
    inference[3][2] = inferenceRule('moderate', 'low')
    inference[3][3] = min(follower[1], engagement[0])
    
    inference[4][0] = follower[1]
    inference[4][1] = engagement[1]
    inference[4][2] = inferenceRule('moderate', 'average')
    inference[4][3] = min(follower[1], engagement[1])
    
    inference[5][0] = follower[1]
    inference[5][1] = engagement[2]
    inference[5][2] = inferenceRule('moderate', 'high')
    inference[5][3] = min(follower[1], engagement[2])
    
    inference[6][0] = follower[2]
    inference[6][1] = engagement[0]
    inference[6][2] = inferenceRule('many', 'low')
    inference[6][3] = min(follower[2], engagement[0])
    
    inference[7][0] = follower[2]
    inference[7][1] = engagement[1]
    inference[7][2] = inferenceRule('many', 'average')
    inference[7][3] = min(follower[2], engagement[1])
    
    inference[8][0] = follower[2]
    inference[8][1] = engagement[2]
    inference[8][2] = inferenceRule('many', 'high')
    inference[8][3] = min(follower[2], engagement[2])
  
    return inference

def inferenceResult(followerCount, engagementRate):
    rejected = []
    considered = []
    accepted = []
    inference = inferensi(followerCount, engagementRate)
    for i in range(9):
        if (inference[i][2] == 'rejected'):
            rejected.append(inference[i][3])
        elif(inference[i][2] == 'considered'):
            considered.append(inference[i][3])
        elif(inference[i][2] == 'accepted'):
            accepted.append(inference[i][3])
    
    membership = [0 for x in range(3)]
    membership[0] = max(rejected)
    membership[1] = max(considered)
    membership[2] = max(accepted)
    
    return membership   

def deFuzzifikasi(membership):
    return ((membership[0] * 1000) + (membership[1] * 2000) + (membership[2] *3000)/(membership[0]+membership[1]+membership[2]))

def labelPredict(result):
    if (result <= 1000):
        label = 'rejected'
    elif (result <= 2000):
        label = 'considered'
    else:
        label = 'accepted'
    return label

score = [[0 for x in range(3)] for y in range(100)]

print("Influencers Score")
print("------------------")
data = getData()
for i in range(100):
    score[i][0] = data.iloc[i][0]
    score[i][1] = deFuzzifikasi(inferenceResult(data.iloc[i][1], data.iloc[i][2]))
    score[i][2] = labelPredict(score[i][1])
    print(i+1," Score= ",score[i][1])
    print("Label=", score[i][2])
    print("")
    
score_sorted = sorted(score,key=lambda l:l[1], reverse=True)
chosen = [0 for x in range(20)]
for i in range(20):
    chosen[i] = int(score_sorted[i][0])
    
with open('chosen.csv', 'w') as f:
    for item in chosen:
        f.write("%s\n" % item)