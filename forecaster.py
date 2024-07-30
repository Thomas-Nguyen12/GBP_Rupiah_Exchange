#!/usr/bin/env python
from scalecast.Forecaster import Forecaster
import prophet
import joblib 
import pickle
import matplotlib.pyplot as plt
# Importing the dataset 
from currency_data_extraction import *


df['date'] = df.index

f = Forecaster(
   y=df['rupiahs_in_a_pound'],
   current_dates=df.index,
   # defaults below
   require_future_dates=True,
   future_dates=None,
   test_length = 0,
   cis = False,
   metrics = ['rmse','mape','mae','r2'],
)
f.set_test_length(12)




f.generate_future_dates(365)

f.add_ar_terms(4) # 4 AR terms
f.add_AR_terms((2,12)) # 2 seasonal AR terms
f.add_seasonal_regressors('month',raw=False,sincos=True)
f.add_seasonal_regressors('year')
f.add_covid19_regressor() # called 'COVID19' by default
f.add_time_trend() # called 't' by default
f.add_combo_regressors('t','COVID19') # 't_COVID19'
f.add_poly_terms('t',pwr=3) # 't^2' and 't^3'

f.set_validation_length(6)
# automatically tune and forecast with a series of models
models = ('mlr','knn','svr','xgboost','gbt','elasticnet','mlp','prophet')
for m in models:
 f.set_estimator(m)
 f.tune() # by default, will pull grids from Grids.py
 f.auto_forecast()
 f.set_estimator('combo')
f.manual_forecast(how='simple',models='top_3',determine_best_by='ValidationMetricValue',call_me='avg')
f.manual_forecast(how='weighted',models=models,determine_best_by='ValidationMetricValue',call_me='weighted')
f.set_estimator('lstm')
f.manual_forecast(
    call_me='lstm_model',
    epochs=100,
    loss='mse',
    learning_rate=0.01,
    optimizer='Adam',
    lstm_layer_sizes=[32],
)

# Saving the forecaster 

    
f.export(['model_summaries', 'lvl_test_set_predictions', 'lvl_fcsts'])


# Saving the figure 
f.plot(models='top_3', order_by="TestSetRMSE")
plt.axvline(x=max(df.index), c='black')
plt.ylabel("Rupiahs in a Pound")
plt.savefig('forecast.png')

plt.show()
date_for_line = max(df.index) 

joblib.dump(date_for_line, 'date_line_boundary.joblib')
