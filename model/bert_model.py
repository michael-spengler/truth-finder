# +
from IPython.core.interactiveshell import InteractiveShell

InteractiveShell.ast_node_interactivity = "all"
# -

import pandas as pd
import numpy as np
from simpletransformers.classification import ClassificationModel, ClassificationArgs
import torch

df = pd.read_csv("data/processed_data.csv")

df.head()

df.label.unique()

dic = {
    'Mostly True'    : 0.75,
    'False'          : 0.15,
    'True'           : 1,
    'Mostly False'   : 0.35, 
    'Legend'         : 0,
    'Mixture'        : 0.5,
    'Out'            : None,
    'Scam'           : 0,
}

df.replace({"label": dic}, inplace=True)

df.head()

df.dropna(subset=['label'],inplace=True)

len(df)

df.label.unique()

cuda_available = torch.cuda.is_available()
cuda_available

df.drop(columns=['author', 'claim', 'title'],
             inplace=True)

cols = ['text', 'label']
df = df[cols]

train, validate, test = \
              np.split(df.sample(frac=1, random_state=42), 
                       [int(.6*len(df)), int(.8*len(df))])

len(train)
len(validate)
len(test)

model_args = ClassificationArgs()
model_args.num_train_epochs = 5
model_args.learning_rate = 1e-4
model_args.regression = True

model = ClassificationModel("bert", "bert-base-cased", use_cuda=cuda_available, args=model_args, num_labels=1)

model.train_model(train)


