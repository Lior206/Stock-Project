import datetime as dt
import numpy as np
from data import import_df as imdf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Ridge, Lasso, BayesianRidge, LinearRegression, RidgeCV
from sklearn.pipeline import make_pipeline
from sklearn.metrics import r2_score, mean_squared_error


# Function to choose the best prediction between the models
def best_indx_in_arr(arr, using):
    best = arr[0][2]
    best_inx = 0
    for i in range(len(arr)):
        if arr[i][2] < best:
            best = arr[i][2]
            best_inx = i
    using[best_inx] += 1
    return best_inx


# Function to decide how many days to go back
def get_num_days(day):
    if day == 'Sunday':
        return 2
    elif day == 'Monday':
        return 3
    else:
        return 1


# Function to to split the data set and call the algorithms
def choose_algo(df, days, price, using):
    df['Prediction'] = df[['Adj Close']].shift(-(days + 1))

    X = np.array(df.drop(['Prediction'], 1))[:-(days + 1)]
    y = np.array(df['Prediction'])[:-(days + 1)]

    # Splitting the data set into the Training and Test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    data = [reg_model_algo(X_train, X_test, y_train, y_test, price, "linear_reg"),
            reg_model_algo(X_train, X_test, y_train, y_test, price, "poly1"),
            reg_model_algo(X_train, X_test, y_train, y_test, price, "poly2"),
            reg_model_algo(X_train, X_test, y_train, y_test, price, "lasso"),
            reg_model_algo(X_train, X_test, y_train, y_test, price, "bayesian"),
            reg_model_algo(X_train, X_test, y_train, y_test, price, "ridgeCV")]
    return data[best_indx_in_arr(data, using)]


# Function to active algorithm for each amount of days
def stock_predictions(stock_name, predictions, prices, num_days, r2_scores, scores, using, score_avgs, r2_avgs):

    days = get_num_days(dt.datetime.today().strftime("%A"))
    start = str(dt.datetime.today().date() - dt.timedelta(days=days))
    df = imdf(stock_name)

    df1 = df[['Adj Close']]
    curr_price = float(df1.loc[start, :].to_string().split(" ")[5])
    curr_x = np.array(df.loc[start, :])
    avg = 0
    r2_avg = 0
    prices.append(curr_price)

    for days in num_days:
        prediction, r2_model_score, score = choose_algo(df, days, curr_x, using)
        avg += score
        r2_avg += r2_model_score
        if days == 14:
            predictions[8].append(prediction)
            r2_scores[8].append(r2_model_score)
            scores[8].append(score)
        elif days == 30:
            predictions[9].append(prediction)
            r2_scores[9].append(r2_model_score)
            scores[9].append(score)
        else:
            predictions[days].append(prediction)
            r2_scores[days].append(r2_model_score)
            scores[days].append(score)
    score_avgs.append(avg / len(num_days))
    r2_avgs.append(r2_avg / len(num_days))


# Algorithm
def reg_model_algo(X_train, X_test, y_train, y_test, price, alg_type):
    # Create model for prediction
    if alg_type == "linear_reg":
        reg_model = LinearRegression()
    elif alg_type == "poly1":
        reg_model = make_pipeline(PolynomialFeatures(2), Ridge())
    elif alg_type == "poly2":
        reg_model = make_pipeline(PolynomialFeatures(3), Ridge())
    elif alg_type == "lasso":
        reg_model = Lasso(alpha=0.1)
    elif alg_type == "bayesian":
        reg_model = BayesianRidge()
    elif alg_type == "ridgeCV":
        reg_model = RidgeCV(alphas=np.logspace(-6, 6, 13))

    reg_model.fit(X_train, y_train)
    y_pred = reg_model.predict(X_test)
    r2_model_score = r2_score(y_test, y_pred)
    score = mean_squared_error(y_test, y_pred)
    print("Accuracy checked successfully")
    prediction = reg_model.predict([price])
    return prediction[0], r2_model_score, score







