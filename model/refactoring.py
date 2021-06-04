# +
# #!pip install transformers

import torch
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
import torch.nn.functional as F

from transformers import BertTokenizer, BertConfig,AdamW, BertForSequenceClassification,get_linear_schedule_with_warmup
from tqdm import tqdm, trange
import pandas as pd
import io
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
import sklearn.metrics as metrics

import random
import os
from pathlib import Path
% matplotlib inline


# -

def relabel_df(path):
    """
    reads in dataframe from given path,
    relabels it for Regression purpose and drops
    filtered columns for simplicity
    
    parameters:
        path: preferribly a pathlib object,
              string also acceptable (for using colab)
              
    return:
        processed dataframe
    """
    
    df = pd.read_csv(path)
    
    # scale from 0 (flat out scam)
    # to 1 objectivly true and well written
    # originally label are provided by pilitico and similar websites
    # translation to scale is tuneable and selfmade
    dic = {'Mostly True'    : 0.85,
           'False'          : 0.10,
           'True'           : 1.0,
           'Mostly False'   : 0.30, 
           'Legend'         : 0.0,
           'Mixture'        : 0.5,
           'Out'            : None,
           'Scam'           : 0.0,
           }
    
    # replace original labels and drop uniformative ones
    df.replace({"label": dic}, inplace=True)
    df.dropna(subset=['label'],inplace=True)
    df.drop(columns=['author', 'claim', 'title'],
             inplace=True)
    
    # reorders the columns for the bert model
    cols = ['text', 'label']
    df = df[cols]
    
    return df


def visulize_label_distribution(df):
    
    names = sorted([str(x) for x in df.label.unique()])
    values = df.label.value_counts()

    plt.figure(figsize=(9, 5))

    plt.subplot(131)
    plt.bar(names, values, align='center', width=0.5)
    plt.suptitle('Class Distribution')
    plt.show()


path = Path.cwd().joinpath('data','processed_data.csv')
df = relabel_df(path)

visulize_label_distribution(df)
# dataset overfits towards false news because articles checked on
# fact checking sites tend to be false. "True" news makes people
# less suspicious so it does not get checked

def bert_preprocessing(df):
    """
    tokenizes articles and creates the corresponding attention mask for it
    
    return:
        input_ids: tokenized articles
        attention_mask: filles the attention mask used on articles shorter then specified
    """
    
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased',
                                              do_lower_case=True)
    sentences = df.text.values
    
    
    # for this version we only use the first 512 characters of a article
    # this is to lower computing performance needs
    # a why to tokenize hole articles needs to be used for better performance
    input_ids = [tokenizer.encode(sent[:512],
                                  add_special_tokens=True,
                                  max_length=512,
                                  pad_to_max_length=True)
                 if len(sent)>512
                 else tokenizer.encode(sent,
                                       add_special_tokens=True,
                                       max_length=512,
                                       pad_to_max_length=True) 
                 for sent in sentences]
    
    attention_masks = []
    ## Create a mask of 1 for all input tokens and 0 for all padding tokens
    attention_masks = [[float(i>0) for i in seq] for seq in input_ids]
    
    return input_ids, attention_masks


def split_dataset(input_ids, masks, batch_size=5):
    """
    splits dataset into train, validation and test set
    return:
     data loader pipelines for all three subsets
    """

    train_inputs, val_inputs_help, train_labels, val_labels = train_test_split(input_ids, labels, random_state=42, test_size=0.4)
    train_masks, val_masks, _, _ = train_test_split(attention_masks, input_ids, random_state=42, test_size=0.4)

    val_inputs, test_inputs, val_labels, test_labels = train_test_split(val_inputs_help, val_labels, random_state=42, test_size=0.5)
    val_masks, test_masks, _, _ = train_test_split(val_masks, val_inputs_help, random_state=42, test_size=0.5)

    # convert all our data into torch tensors, required data type for our model
    train_inputs = torch.tensor(train_inputs)
    val_inputs = torch.tensor(val_inputs)
    test_inputs = torch.tensor(test_inputs)

    train_labels = torch.tensor(train_labels)
    val_labels = torch.tensor(val_labels)
    test_labels = torch.tensor(test_labels)

    train_masks = torch.tensor(train_masks)
    val_masks = torch.tensor(val_masks)
    test_masks = torch.tensor(test_masks)

    # Create an iterator of our data with torch DataLoader. This helps save on memory during training because, unlike a for loop, 
    # with an iterator the entire dataset does not need to be loaded into memory
    train_data = TensorDataset(train_inputs,train_masks,train_labels.float())
    train_sampler = RandomSampler(train_data)
    train_dataloader = DataLoader(train_data,sampler=train_sampler,batch_size=batch_size)

    val_data = TensorDataset(val_inputs,val_masks,val_labels.float())
    val_sampler = RandomSampler(val_data)
    val_dataloader = DataLoader(val_data, sampler=val_sampler, batch_size=batch_size)

    test_data = TensorDataset(test_inputs, test_masks, test_labels.float())
    test_sampler = RandomSampler(test_data)
    test_dataloader = DataLoader(test_data, sampler=test_sampler, batch_size=batch_size)
    
    return train_dataloader, val_dataloader, test_dataloader


def get_model(device, model_name="bert-base-uncased", num_labels=1):
    
    model = BertForSequenceClassification.from_pretrained(model_name, num_labels)
    model.to(device)
    
    return model


def set_parameters(dataloader):
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    
    # Parameters:
    lr = 2e-3
    adam_epsilon = 1e-8
    
    epochs = 3
    
    num_warmup_steps = 0
    num_training_steps = len(dataloader)*epochs
    
    # In Transformers, optimizer and schedules are splitted and instantiated like this:
    optimizer = AdamW(model.parameters(), lr=lr,eps=adam_epsilon,correct_bias=False)  # To reproduce BertAdam specific behavior set correct_bias=False
    scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=num_warmup_steps, num_training_steps=num_training_steps)  # PyTorch scheduler


def train_model(train, val):
    """
    train: train_dataloader
    val: val_dataloader
    """
    
    ## Store our loss and accuracy for plotting
    train_loss_set = []
    learning_rate = []

    # Gradients gets accumulated by default
    model.zero_grad()
    
    # tnrange is a tqdm wrapper around the normal python range
    for _ in trange(1,epochs+1,desc='Epoch'):
        print("<" + "="*22 + F" Epoch {_} "+ "="*22 + ">")
        # Calculate total loss for this epoch
        batch_loss = 0

        for step, batch in enumerate(train):
            # Set our model to training mode (as opposed to evaluation mode)
            model.train()

            # Add batch to GPU
            batch = tuple(t.to(device) for t in batch)
            # Unpack the inputs from our dataloader
            b_input_ids, b_input_mask, b_labels = batch
            # print(b_input_ids[0].dtype ,"\n", b_input_mask[0].dtype, "\n", b_labels[0].dtype)

            # Forward pass
            outputs = model(b_input_ids, token_type_ids=None, attention_mask=b_input_mask, labels=b_labels)
            loss = outputs[0]
            loss = loss.float()

            # Backward pass
            loss.backward()

            # Clip the norm of the gradients to 1.0
            # Gradient clipping is not in AdamW anymore
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)

            # Update parameters and take a step using the computed gradient
            optimizer.step()

            # Update learning rate schedule
            scheduler.step()

            # Clear the previous accumulated gradients
            optimizer.zero_grad()

            # Update tracking variables
            batch_loss += loss.item()

            # Calculate the average loss over the training data.
            avg_train_loss = batch_loss / len(train_dataloader)

            #store the current learning rate
            for param_group in optimizer.param_groups:
                print("\n\tCurrent Learning rate: ",param_group['lr'])
                learning_rate.append(param_group['lr'])

            train_loss_set.append(avg_train_loss)
            print(F'\n\tAverage Training loss: {avg_train_loss}')
            
            validate(model, val)


def validate(model, dataloader):
    """
    gets metrics for the current model
    """
    model.eval()
    
     # Evaluate data for one epoch
    for batch in val_dataloader:
        # Add batch to GPU
        batch = tuple(t.to(device) for t in batch)
        # Unpack the inputs from our dataloader
        b_input_ids, b_input_mask, b_labels = batch
        # Telling the model not to compute or store gradients, saving memory and speeding up validation
        with torch.no_grad():
            # Forward pass, calculate logit predictions
            logits = model(b_input_ids, token_type_ids=None, attention_mask=b_input_mask)

        # Move logits and labels to CPU
        logits = logits[0].to('cpu').numpy()
        label_ids = b_labels.to('cpu').numpy()
        
        pred_flat = logits.flatten()
        labels_flat = label_ids.flatten()
        
        # placeholder for other metrics. standard deviation would be cool I think
        tmp_eval_mse, tmp_eval_variance, tmp_eval_r2_score  = model_score(labels_flat,pred_flat)
        
        eval_mse += tmp_eval_accuracy
        eval_variance += tmp_eval_variance
        eval_r2_score += tmp_eval_r2_score
        nb_eval_steps += 1
        
        
    print(F'\n\tValidation MSE: {eval_mse/nb_eval_steps}')
    print(F'\n\tValidation Var: {eval_variance/nb_eval_steps}')
    print(F'\n\tValidation R2: {eval_r2_score/nb_eval_steps}')


def model_score(labels, prediction):
    
    mse      = metrics.mean_squared_error(labels, prediction)
    variance = metrics.explained_variance_score(labels, prediction)
    r2_score = metrics.r2_score(labels, prediction)
    
    return mse, variance, r2_score


# +
# tokenizer
input_ids, attention_masks = bert_preprocessing(df)

# data pipelines
train_dataloader, val_dataloader, test_dataloader = split_dataset(input_ids, masks, batch_size=5)

# load model
model = get_model(device, model_name="bert-base-uncased", num_labels=1)

set_parameters(train_dataloader)
# -

train_model(train_dataloader, val_dataloader)
