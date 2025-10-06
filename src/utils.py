import os
import sys
import numpy as np
import pandas as pd
import pickle
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

from src.exception import CustomException

def save_object(file_path, obj):
    """
    Save an object to a pickle file.
    
    Args:
        file_path (str): Path where the object should be saved
        obj: Object to be saved
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
            
    except Exception as e:
        raise CustomException(e, sys)

def load_object(file_path):
    """
    Load an object from a pickle file.
    
    Args:
        file_path (str): Path to the pickle file
        
    Returns:
        Loaded object
    """
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)
            
    except Exception as e:
        raise CustomException(e, sys)

def evaluate_models(X_train, y_train, X_test, y_test, models, param):
    """
    Evaluate multiple models with hyperparameter tuning.
    
    Args:
        X_train: Training features
        y_train: Training target
        X_test: Test features  
        y_test: Test target
        models: Dictionary of models to evaluate
        param: Dictionary of hyperparameters for each model
        
    Returns:
        Dictionary with model names as keys and R2 scores as values
    """
    try:
        report = {}
        
        for i in range(len(list(models))):
            model = list(models.values())[i]
            para = param[list(models.keys())[i]]
            
            gs = GridSearchCV(model, para, cv=3)
            gs.fit(X_train, y_train)
            
            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)
            
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)
            
            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)
            
            report[list(models.keys())[i]] = test_model_score
            
        return report
        
    except Exception as e:
        raise CustomException(e, sys)