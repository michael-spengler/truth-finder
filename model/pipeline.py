# +
from IPython.core.interactiveshell import InteractiveShell

InteractiveShell.ast_node_interactivity = "all"

# +
import numpy as np # linear algebra
import pandas as pd # read data

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV

import seaborn as sns

from lightgbm import LGBMRegressor as LGBM

from warnings import simplefilter
simplefilter(action='ignore', category=FutureWarning)

# +
df = pd.read_csv("ames.csv").iloc[0:2000]
df_test = pd.read_csv("ames.csv").iloc[2001:]

#get target
salePrice = df.Sale_Price
df.drop(columns=['Sale_Price'], inplace=True)

salePrice_test = df_test.Sale_Price
df_test.drop(columns=['Sale_Price'], inplace=True)

df.describe().T
# -

df.head().T

categorical_cols = [col for col in df.columns if df[col].dtype == 'object']
#categorical_cols
numerical_cols = [col for col in df.columns if (df[col].dtype == 'int64' or df[col].dtype == 'float64')]
#numerical_cols

# +
numerical_transformer = SimpleImputer()
categorical_transformer = Pipeline(steps=
                                   [('imputer', SimpleImputer(strategy='most_frequent')),
                                    ('onehot', OneHotEncoder(handle_unknown='ignore'))])

preprocessor = ColumnTransformer(transformers=
                                 [('num', numerical_transformer, numerical_cols), 
                                  ('cat', categorical_transformer, categorical_cols)])

# +
model = LGBM(random_state=0)

pipeline = Pipeline(steps=
                   [('preprocess', preprocessor),
                   ('model', model)])
# -
grid = GridSearchCV(pipeline,  
                    param_grid={'model__n_estimators': [2000],
                                'model__learning_rate' : [0.01, 0.05],                                
                                'model__min_child_weight' : [0, 1]
                               },
                    #cv = 10,
                    scoring = 'neg_mean_absolute_error')
grid.fit(df, salePrice)
print(f"Best model parameters: {grid.best_params_}")
print(f"Best score: {-1 * grid.best_score_}")

# save test predictions to file
predictions = grid.predict(df_test)
output = pd.DataFrame({'Id': df_test.index, 'SalePrice': predictions, 'Label': salePrice_test})

output.to_csv('result_20.csv', index=False)

avg = (output['SalePrice'] - output['Label']).abs()
avg = avg.to_numpy()

np.average(avg)

np.std(avg)


