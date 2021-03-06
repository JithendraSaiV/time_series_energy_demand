from sklearn.metrics import mean_absolute_error, make_scorer
import numpy as np
import pandas as pd


def relative_mean_absolute_error(y_true, y_pred):
    """Calculate the relative mean absolute error
    Parameters
    ----------
    y_true : array-like object
        The reference values
    y_pred : array-like object
        The predicted values
    """
    diff = np.abs(y_true-y_pred)
    return np.mean(diff/y_true)

def relative_mean_squared_error(y_true, y_pred):
    """Calculate the relative mean squared error
    Parameters
    ----------
    y_true : array-like object
        The reference values
    y_pred : array-like object
        The predicted values
    """
    diff_squared = np.abs(y_true-y_pred)**2
    return np.mean(diff_squared/(y_true**2))

def calculate_score(y_true, y_pred, metric=mean_absolute_error):
    """Function to calculate a score with a given metric for the output of the GAR model
    
    Parameters
    ----------
    y_true : pandas DataFrame
        The dataframe with the reference data (has NaNs in the lower right half)
    y_pred : pandas DataFrame
        The dataframe with the predicted values, i.e. the output of the GAR model
    metric : object, optional, default: mean_absolute_error (from scikit-learn)
        A function that calculates a score and takes as input y_true and y_pred (e.g.
        from scikit-learn)
    """
    df_results = pd.DataFrame(y_true.values, 
                                index=y_true.index, 
                                columns=['left']).join(pd.DataFrame(y_pred.values, 
                                                                    index=y_pred.index)).dropna()
    df_results.columns = ['y_true', 'y_pred']
    df_results.dropna(axis='rows', inplace=True)
    score = metric(df_results['y_true'], df_results['y_pred'])
    return score

def highlight_top(data, color='yellow', greater_is_better=False):
    """Highlight the top value of the score table
    Parameters
    ----------
    data : pandas Series
        The series (columns of the dataframe) return by df.apply()
    color : str, default: 'yellow'
        Color to use to mark the top value for each column
    greater_is_better : boolean, default: False
        For the correlation test, greater is better (and don't highlight the diagonal)
    """
    attr = 'background-color: {}'.format(color)
    
    if data.name == 'coeff. of determination':
        is_max = data == data.max() # because top value is 1.0 (larger is better)
    else:
        if greater_is_better==False:
            is_max = data == data.min() # others are error functions (smaller is better)
        else:
            is_max = data == data.max()
    return [attr if v else '' for v in is_max]