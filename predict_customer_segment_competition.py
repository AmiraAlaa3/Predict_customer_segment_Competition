# -*- coding: utf-8 -*-
"""Predict customer segment Competition.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nu-KgrqeIHEpAlcYxi2sT2IbOp0v3XL7
"""

import pandas as pd
import numpy as np 
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt 
import seaborn as sns
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

missingValues = [""," "]
data = pd.read_csv("/content/train.csv", encoding= 'unicode_escape',na_values=missingValues)
test = pd.read_csv("/content/test.csv", encoding= 'unicode_escape',na_values=missingValues)

data

test

data.describe()

missing={"missing":data.isnull().sum()," % of missing":round(((data.isnull().sum()/data.shape[0])*100),2)}
pd.DataFrame(missing)

missing={"missing":test.isnull().sum()," % of missing":round(((test.isnull().sum()/test.shape[0])*100),2)}
pd.DataFrame(missing)

data.duplicated().sum()

data.info()

sns.countplot(data['Work_Experience'])

sns.countplot(data['Work_Experience'])

sns.countplot(data['Gender'],hue=data['Segmentation'])
sns.countplot(data['Ever_Married'],hue=data['Segmentation'])
sns.distplot(data['Age'])

plt.rcParams['figure.figsize'] = (10, 6)
sns.countplot(data['Profession'],hue=data['Segmentation'])

sns.countplot(data['Work_Experience'])

sns.countplot(test['Graduated'])

data['Ever_Married']=data['Ever_Married'].fillna('Yes')
test['Ever_Married']=test['Ever_Married'].fillna('Yes')

meann= test["Work_Experience"].mean()
test["Work_Experience"].fillna(meann,inplace=True)
#cat1   then 4
data['Var_1'].fillna('Cat_1',inplace=True)
test['Var_1'].fillna('Cat_1',inplace=True)

meann= data["Family_Size"].mean()
data["Family_Size"].fillna(meann,inplace=True)
meann= test["Family_Size"].mean()
test["Family_Size"].fillna(meann,inplace=True)

data['Gender'] =  data['Gender'].map({'Female': 1,'Male':0})
test['Gender'] =  test['Gender'].map({'Female': 1,'Male':0})

data['Ever_Married'] =  data['Ever_Married'].map({'Yes': 1,'No':0})
test['Ever_Married'] =  test['Ever_Married'].map({'Yes': 1,'No':0})

data['Graduated'] =  data['Graduated'].map({'Yes': 1,'No':0})
test['Graduated'] =  test['Graduated'].map({'Yes': 1,'No':0})

data['Spending_Score'] =  data['Spending_Score'].map({'Average': 1,'Low':0 ,'High':2})
test['Spending_Score'] =  test['Spending_Score'].map({'Average': 1,'Low':0 ,'High':2})

data['Segmentation'] = data['Segmentation'].map({'A': 1,'B':0 ,'C':2 ,'D':3})
data.duplicated().value_counts()

# i tried to wite all features here but the same score
from sklearn.preprocessing import LabelEncoder
cat_cols = ['Profession','Var_1']
enc = LabelEncoder()

for col in cat_cols:
    data[col] = data[col].astype('str')
    test[col] = test[col].astype('str')
    data[col] = enc.fit_transform(data[col])
    test[col] = enc.transform(test[col])

meann= data["Graduated"].median()
data["Graduated"].fillna(meann,inplace=True)
meann= test["Graduated"].median()
test["Graduated"].fillna(meann,inplace=True)

meann= data["Profession"].mean()
data["Profession"].fillna(meann,inplace=True)
meann= test["Profession"].mean()
test["Profession"].fillna(meann,inplace=True)

Work_Experience_nan_1 = data.query('Segmentation == 1')['Work_Experience'][data['Work_Experience'].isna()].index
data.loc[Work_Experience_nan_1,'Work_Experience'] =data.query('Segmentation == 1')['Work_Experience'][data['Work_Experience'].notna()].mean()

Work_Experience_nan_0 = data.query('Segmentation == 0')['Work_Experience'][data['Work_Experience'].isna()].index
data.loc[Work_Experience_nan_0,'Work_Experience'] = data.query('Segmentation == 0')['Work_Experience'][data['Work_Experience'].notna()].mean()

Work_Experience_nan_1 = data.query('Segmentation == 2')['Work_Experience'][data['Work_Experience'].isna()].index
data.loc[Work_Experience_nan_1,'Work_Experience'] =data.query('Segmentation == 2')['Work_Experience'][data['Work_Experience'].notna()].mean()

Work_Experience_nan_0 = data.query('Segmentation == 3')['Work_Experience'][data['Work_Experience'].isna()].index
data.loc[Work_Experience_nan_0,'Work_Experience'] = data.query('Segmentation == 3')['Work_Experience'][data['Work_Experience'].notna()].mean()

data=data.set_index("ID")
test=test.set_index("ID")
index=test.index

data.isnull().sum()

test.isnull().sum()

print(np.intersect1d(data.index, test.index).shape[0]/data.index.nunique())
common_ids = len(set(test.index.unique()).intersection(set(data.index.unique())))
print("Common IDs : ",common_ids)

from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
X=data.drop(["Segmentation"],axis=1)
y=data["Segmentation"]
X_train, X_test, y_train, y_test = train_test_split(X, y,random_state = 0, train_size = 0.7)

clf = RandomForestClassifier( max_depth = 20, n_estimators = 500,min_samples_leaf=4,min_samples_split=30,random_state=40)

clf.fit(X_train,y_train)
y_pred = clf.predict(test)
    
print('Accuracy on training set: {:.6f}'.format(clf.score(X_train, y_train)))  

#Accuracy on training set: 0.590030   scored 0.49518


#Accuracy on training set: 0.622532     scored 0.49688

import xgboost as xgb
X=data.drop(["Segmentation"],axis=1)
y=data["Segmentation"]
X_train, X_test, y_train, y_test = train_test_split(X, y,random_state = 0, train_size = 0.7)

xg_reg = xgb.XGBClassifier(objective ='multi:softmax',num_class=4,  learning_rate = 0.1,
                max_depth = 3,alpha = 2, n_estimators = 200,min_samples_leaf=4,min_samples_split=2,random_state=0)
xg_reg.fit(X_train,y_train)
y_pred = xg_reg.predict(test)
print("Testing score: ",xg_reg.score(X_test, y_test))      
print('Accuracy on training set: {:.6f}'
     .format(xg_reg.score(X_train, y_train)))  

#Testing score:  0.4790697674418605           
#Accuracy on training set: 0.514457

from sklearn.ensemble import ExtraTreesClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X=data.drop(["Segmentation"],axis=1)
y=data["Segmentation"]

Xtrain, Xtest, y_train, y_test = train_test_split(X, y,random_state = 0, train_size = 0.7)

#X, y = make_classification(n_features=9, random_state=0)
clf = ExtraTreesClassifier(n_estimators=100, max_depth=20,min_samples_leaf=5,min_samples_split=18,random_state=0)
clf.fit(Xtrain, y_train)

y_pred = clf.predict(test)
print("Testing score: ",clf.score(Xtest, y_test))      
print('Accuracy on training set: {:.6f}'
     .format(clf.score(Xtrain, y_train)))  
#Testing score:  0.46837209302325583
#Accuracy on training set: 0.668195      
   
#Testing score:  0.47069767441860466
#Accuracy on training set: 0.647059

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
X=data.drop(["Segmentation"],axis=1)
y=data["Segmentation"]
X_train, X_test,y_train,y_test = train_test_split(X,y,train_size = 0.8 ,random_state=42)

clf = GradientBoostingClassifier(n_estimators=60, learning_rate=1.0,
   max_depth=2, random_state=0)
clf.fit(X_train, y_train)
y_pred = clf.predict(test)   
print("Testing score: ",clf.score(X_test, y_test))     
print('Accuracy on training set: {:.6f}'
     .format(clf.score(X_train, y_train)))             
  
#Testing score:  0.4640614096301465
#Accuracy on training set: 0.541172

X=data.drop(["Segmentation"],axis=1)
y=data["Segmentation"]

X_train, X_test, y_train, y_test = train_test_split(X, y,random_state = 42, train_size = 0.8)

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)#
X_test = sc.transform(X_test)

logi = LogisticRegression()
logi.fit(X_train, y_train)
y_pred = logi.predict(X_test)
print("Testing score: ",logi.score(X_test, y_test))        #testing was 0.452896 then 0.4577808792742498
print('Accuracy on training set: {:.6f}'
     .format(logi.score(X_train, y_train))) 
#knn.score(Xtest, y_pred)

#Do not run again not a good accuracy$$$ logistic:0.43  knn:0.40
X=data.drop(["Segmentation"],axis=1)
y=data["Segmentation"]

Xtrain, Xtest, y_train, y_test = train_test_split(X, y,random_state = 42, train_size = 0.7)

knn = KNeighborsClassifier()
knn.fit(Xtrain, y_train)
y_pred = knn.predict(test)
#knn.score(Xtest, y_pred)

#do not run 0.43569 score when logistic gave 0.44
from lightgbm  import LGBMClassifier
X=data.drop(["Segmentation"],axis=1)
y=data["Segmentation"]

Xtrain, Xtest, y_train, y_test = train_test_split(X, y,random_state = 42, train_size = 0.8)

lgb_model = LGBMClassifier(
                                   boosting_type='gbdt', 
                                   max_depth=15, 
                                   learning_rate=0.15, 
                                   objective='multiclass', # Multi Class Classification
                                   random_state=42,  
                                   n_estimators=1000 ,
                                   reg_alpha=0, 
                                   reg_lambda=1, 
                                   n_jobs=-1
                                 )
lgb_model.fit(Xtrain,y_train)
y_pred = lgb_model.predict(test)

from sklearn.ensemble import GradientBoostingClassifier
clf = GradientBoostingClassifier(n_estimators=60,random_state=0)

X=data.drop(["Segmentation"],axis=1)
y=data["Segmentation"]

Xtrain, Xtest, y_train, y_test = train_test_split(X, y,random_state = 0, train_size = 0.7)

#X, y = make_classification(n_features=9, random_state=0)
#clf = ExtraTreesClassifier(n_estimators=100, max_depth=20,min_samples_leaf=5,min_samples_split=18,random_state=0)
clf.fit(Xtrain, y_train)

y_pred = clf.predict(test)
print("Testing score: ",clf.score(Xtest, y_test))      
print('Accuracy on training set: {:.6f}'
     .format(clf.score(Xtrain, y_train)))

from lightgbm import LGBMClassifier
neigh = LGBMClassifier(boosting_type='gbdt', num_leaves=30,
                                learning_rate=0.1, max_depth=15,n_estimators=60,
                                feature_fraction=0.9, reg_lambda=0.4,random_state=1)
neigh.fit(X_train, y_train)
y_pred = neigh.predict(test)
print('Accuracy of K-NN classifier on training set: {:.6f}'
     .format(neigh.score(X_train, y_train)))
print('Accuracy of K-NN classifier on test set: {:.6f}'
     .format(neigh.score(X_test, y_test)))

#Accuracy  classifier on training set: 0.600598       scored:0.49631
#Accuracy classifier on test set: 0.480465

#y_pred = y_pred.map({'A': 1,'B':0 ,'C':2 ,'D':3})
new_arr=['']*(len(y_pred))
for i in range(len(y_pred)):
  if(y_pred[i]==1):
    new_arr[i]='A'
  elif(y_pred[i]==0):
    new_arr[i]='B'
  elif(y_pred[i]==2):
    new_arr[i]='C'
  else:
    new_arr[i]='D'

result=pd.DataFrame({"ID":index,"Segmentation":new_arr})
result=result.set_index("ID")
result.to_csv('Result1.csv')

x=data.drop(["Segmentation"],axis=1)
y=data["Segmentation"]

X_train, X_test,y_train,y_test = train_test_split(x,y,train_size = 0.7 ,random_state=42)

knn = KNeighborsClassifier(algorithm= 'brute',n_neighbors=4,leaf_size=70)
knn.fit(X_train, y_train)
print('Accuracy of K-NN classifier on training set: {:.2f}'
     .format(knn.score(X_train, y_train)))
print('Accuracy of K-NN classifier on test set: {:.2f}'
     .format(knn.score(X_test, y_test)))

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, classification_report
neigh = KNeighborsClassifier(n_neighbors=7, weights='distance', algorithm='auto', leaf_size=30, p=4, metric='euclidean', metric_params=None, n_jobs=None)
neigh.fit(X_train, y_train)
y_pred = neigh.predict(test)
print('Accuracy of K-NN classifier on training set: {:.2f}'
     .format(neigh.score(X_train, y_train)))
print('Accuracy of K-NN classifier on test set: {:.2f}'
     .format(neigh.score(X_test, y_test)))
#print(classification_report(y_test,pred))
#print(confusion_matrix(y_test,pred))

from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from lightgbm import LGBMClassifier
from sklearn.ensemble import GradientBoostingClassifier

seed = 3
#MODELS
models = []
models.append(('DecisionTreeClassifier', DecisionTreeClassifier()))
models.append(('LR', LogisticRegression()))
models.append(('NB', GaussianNB()))
models.append(('LGBMClassifier',LGBMClassifier(n_estimators=60)))
models.append(('GradientBoostingClassifier',GradientBoostingClassifier(n_estimators=60)))

results = []
names = []
scoring = 'accuracy'
for name, model in models:
    kfold = model_selection.KFold(n_splits=10)
    cv_results = model_selection.cross_val_score(model, X_train, y_train, cv=kfold, scoring=scoring)
    results.append(cv_results)
    names.append(name)
    msg = "%s: %f" % (name, cv_results.mean())
    print(msg)