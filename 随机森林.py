import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from scipy.sparse import hstack

def var():
    global my_price
    global my_comment
    global my_name
    global name_data
    global data
    global message3
    my_price = []
    my_comment = []
    my_name = []
    name_data = []
    data = []
    message3 = []

def file_read():
    with open("./得分2.txt", 'r', encoding="utf-8") as fp:
        for line in fp:
            my_price.append(line.strip().split()[1])
            my_comment.append(line.strip().split()[2])
            my_name.append(line.strip().split()[3])

    for i in my_name:
        name_data.append(str(list(jieba.cut(i))))

    for i in range(len(my_price)):
        data.append({'price': my_price[i], 'name': name_data[i]})


def model_build():
    df = pd.DataFrame(data)
    text_data = df['name'].tolist()
    numeric_data = df['price'].values.reshape(-1, 1)

    global tfidf_vectorizer
    tfidf_vectorizer = TfidfVectorizer()
    X_text_features = tfidf_vectorizer.fit_transform(text_data)

    global scaler
    scaler = StandardScaler()
    X_numeric_features = scaler.fit_transform(numeric_data)

    global X_features
    X_features = hstack([X_text_features, X_numeric_features])

def forest():
    print(X_features.shape,len(my_comment))
    x_train, x_test, y_train, y_test = train_test_split(X_features, my_comment, random_state=22,test_size=0.2)
    global estimator
    estimator = RandomForestClassifier()
    param_grid = {"n_estimators": [10, 20, 50, 100], "max_depth": [3, 5, 8, 10]}
    estimator = GridSearchCV(estimator, param_grid=param_grid, cv=3)
    estimator.fit(x_train, y_train)


def input_data(a,b):
    a = float(a)
    input_data = pd.DataFrame({'price': [a], "name": [b]}, index=[0])
    name_data2 = input_data['name'].tolist()
    price_data2 = input_data['price'].values.reshape(-1, 1)
    X_text_features2 = tfidf_vectorizer.transform(name_data2)
    X_numeric_features2 = scaler.transform(price_data2)
    X_features2 = hstack([X_text_features2, X_numeric_features2])
    predicted_value = estimator.predict(X_features2)
    print("预测结果:", predicted_value)
    message3.append(predicted_value)

def run(a,b):
    var()
    file_read()
    model_build()
    forest()
    input_data(a,b)
    return message3

if __name__ == '__main__':
    var()
    file_read()
    model_build()
    forest()
    input_data(50,"苹果")
