import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report


def algorithm_RFC_train(x, y, n_estimators):
    model_enc = LabelEncoder()
    model_enc.fit(y)
    y = model_enc.transform(y)

    model_rfc = RandomForestClassifier(n_estimators=n_estimators)
    model_rfc.fit(x, y)

    y_prediction = model_rfc.predict(x)
    report = classification_report(y, y_prediction)

    y_prediction = model_enc.inverse_transform(y_prediction)

    y_prediction = pd.Series(y_prediction, name='label')

    return model_enc, model_rfc, y_prediction, report


def algorithm_RFC_validation(x, y, model_enc, model_rfc):
    y = model_enc.transform(y)

    y_prediction = model_rfc.predict(x)
    report = classification_report(y, y_prediction)

    y_prediction = model_enc.inverse_transform(y_prediction)

    y_prediction = pd.Series(y_prediction, name='label')

    return y_prediction, report


def algorithm_RFC_test(x, model_enc, model_rfc):
    y_prediction = model_rfc.predict(x)

    y_prediction = model_enc.inverse_transform(y_prediction)

    y_prediction = pd.Series(y_prediction, name='label')

    return y_prediction


from sklearn.svm import SVC

def algorithm_SVM_train(x, y, n_estimators):
    model_enc = LabelEncoder()
    model_enc.fit(y)
    y = model_enc.transform(y)

    model_svm = SVC()
    model_svm.fit(x, y)

    y_prediction = model_svm.predict(x)
    report = classification_report(y, y_prediction)

    y_prediction = model_enc.inverse_transform(y_prediction)

    y_prediction = pd.Series(y_prediction, name='label')

    return model_enc, model_svm, y_prediction, report

from sklearn.linear_model import LogisticRegression

def algorithm_LR_train(x, y, n_estimators):
    model_enc = LabelEncoder()
    model_enc.fit(y)
    y = model_enc.transform(y)

    model_lr = LogisticRegression()
    model_lr.fit(x, y)

    y_prediction = model_lr.predict(x)
    report = classification_report(y, y_prediction)

    y_prediction = model_enc.inverse_transform(y_prediction)

    y_prediction = pd.Series(y_prediction, name='label')

    return model_enc, model_lr, y_prediction, report

