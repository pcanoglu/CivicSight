import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

data = pd.read_csv('data/donations.csv')

X = data[['donation_amount', 'last_donation_days', 'donation_frequency']]
y = data['will_donate_again']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = LogisticRegression()
model.fit(X_train, y_train)

print("Model trained successfully")
