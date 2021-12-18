# -*- coding: utf-8 -*-
"""Predicting price of used car.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12h0CKr6yhnbm9taE4S14nHB9mZ8uHdlF
"""

import pandas as pd
import numpy as np 
from matplotlib import pyplot as plt
df=pd.read_csv('car data.csv')
print(df.shape)
print(df['Seller_Type'].unique())
print(df['Fuel_Type'].unique())
print(df['Transmission'].unique())
print(df['Owner'].unique())
##check missing values
print(df.isnull().sum())
print(df.describe())
final_dataset=df[['Year','Selling_Price','Present_Price','Kms_Driven','Fuel_Type','Seller_Type','Transmission','Owner']]
final_dataset.head()
final_dataset['Current Year']=2020
final_dataset.head()

final_dataset['no_year']=final_dataset['Current Year']- final_dataset['Year']
final_dataset.head()

final_dataset.drop(['Year'],axis=1,inplace=True)
final_dataset.head()

"""**ONE HOT ENCODING**"""

final_dataset=pd.get_dummies(final_dataset,drop_first=True)
final_dataset.head()

final_dataset=final_dataset.drop(['Current Year'],axis=1)
final_dataset.head()

final_dataset.corr()

import seaborn as sns
sns.pairplot(final_dataset)

"""**HEATMAP**"""

import seaborn as sns
#get correlations of each features in dataset
corrmat = df.corr()
top_corr_features = corrmat.index
plt.figure(figsize=(20,20))
#plot heat map
g=sns.heatmap(df[top_corr_features].corr(),annot=True,cmap="RdYlGn")

#independent and dependent features
X=final_dataset.iloc[:,2:]
y=final_dataset.iloc[:,1]
X['Owner'].unique()

X.head()

y.head()

"""# **Feature Importance**"""

### Feature Importance

from sklearn.ensemble import ExtraTreesRegressor
import matplotlib.pyplot as plt
model = ExtraTreesRegressor()
model.fit(X,y)

print(model.feature_importances_)

#plot graph of feature importances for better visualization
feat_importances = pd.Series(model.feature_importances_, index=X.columns)
feat_importances.nlargest(5).plot(kind='barh')
plt.show()

"""**train_test_split**"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
from sklearn.ensemble import RandomForestRegressor
regressor=RandomForestRegressor()
n_estimators = [int(x) for x in np.linspace(start = 100, stop = 1200, num = 12)]
print(n_estimators)

"""**selecting out of all decision tree values**"""

from sklearn.model_selection import RandomizedSearchCV
 #Randomized Search CV

# Number of trees in random forest
n_estimators = [int(x) for x in np.linspace(start = 100, stop = 1200, num = 12)]
# Number of features to consider at every split
max_features = ['auto', 'sqrt']
# Maximum number of levels in tree
max_depth = [int(x) for x in np.linspace(5, 30, num = 6)]
# max_depth.append(None)
# Minimum number of samples required to split a node
min_samples_split = [2, 5, 10, 15, 100]
# Minimum number of samples required at each leaf node
min_samples_leaf = [1, 2, 5, 10]
# Create the random grid
random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf}

print(random_grid)

"""# **Hyper Parameter Tuning**

1. Finding best parameters

2.Randomized search cv is fast than decision tree,grid search cv

**RandomForestRegressor**
"""

# Use the random grid to search for best hyperparameters
# First create the base model to tune
#verbose displays result values
rf = RandomForestRegressor()
# Random search of parameters, using 3 fold cross validation, 
# search across 100 different combinations
rf_random = RandomizedSearchCV(estimator = rf, param_distributions = random_grid,scoring='neg_mean_squared_error', n_iter = 10, cv = 5, verbose=2, random_state=42, n_jobs = 1)
rf_random.fit(X_train,y_train)
#all the parameters are being defined in the previous step.n_jobs is number of cores of system to be used

rf_random.best_params_

rf_random.best_score_

predictions=rf_random.predict(X_test)

"""# **DISTPLOT**
To compare predicted and actual value.If the graph(the difference) compressed normal disrtribution it is good model.
"""

sns.distplot(y_test-predictions)

plt.scatter(y_test,predictions)
#plotting should be linearly available in order to make prediction good

from sklearn import metrics
print('MAE:', metrics.mean_absolute_error(y_test, predictions))
print('MSE:', metrics.mean_squared_error(y_test, predictions))
print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, predictions)))

"""# **PICKLE**

Pickling is a way to convert a python object (list, dict, etc.) into a character stream. The idea is that this character stream contains all the information necessary to reconstruct the object in another python script.
"""

import pickle
# open a file, where you ant to store the data
file = open('random_forest_regression_model.pkl', 'wb')
#wb: open for writing and open in binary mode.
# 'write binary' and is used for the file handle: open('save. p', 'wb' ) which writes the pickeled data into a file.
#it's just a way to convert from one representation (in RAM) to another (in "text").

# dump information to that file
pickle.dump(rf_random, file)