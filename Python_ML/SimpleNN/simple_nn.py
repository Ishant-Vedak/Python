import torch
import torch.nn as nn
import torch.nn.functional as F

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split

class Model(nn.Module):
    def __init__(self, in_features=4, h1=8, h2=9, out_features=3):
        super().__init__()
        self.fc1 = nn.Linear(in_features, h1)
        self.fc2 = nn.Linear(h1, h2)
        self.out = nn.Linear(h2, out_features)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.out(x)

        return x
    
torch.manual_seed(41)
model = Model()

url = 'https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/raw/0e7a9b0a5d22642a06d3d5b9bcbad9890c8ee534/iris.csv'
my_df = pd.read_csv(url)

my_df['species'] = my_df['species'].replace('setosa', 0.0)
my_df['species'] = my_df['species'].replace('versicolor', 1.0)
my_df['species'] = my_df['species'].replace('virginica', 2.0)

X = my_df.drop('species', axis=1)
y = my_df['species']

X = X.values
y = y.values


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=41)

X_train = torch.FloatTensor(X_train)
X_test = torch.FloatTensor(X_test)

y_train = torch.LongTensor(y_train)
y_test = torch.LongTensor(y_test)


criterion = nn.CrossEntropyLoss()

optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

epochs = 100
losses = []

for i in range(epochs):
    y_predict = model(X_train)

    loss = criterion(y_predict, y_train)

    losses.append(loss.detach().numpy())
    '''
    if i % 10 == 0:
        print(f'Epoch is {i} and loss is {loss}')
    '''
    
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()


with torch.no_grad():
    y_eval = model.forward(X_test)
    loss = criterion(y_eval, y_test)

correct = 0 

with torch.no_grad():
    for i, data in enumerate(X_test):
        y_val = model.forward(data)

        '''
        print(f'{i + 1}) {str(y_val)}')
        '''
        if y_val.argmax().item() == y_test[i]:
            correct += 1



print(f'Correct: {correct}')


'''
new_iris = torch.tensor([4.7, 3.2, 1.3, 0.2])

with torch.no_grad():
    print(model(new_iris))
'''
'''Saving the model:
torch.save(model.state_dict(), 'iris_dataet_nn.pt')

    Loading the model:

    new_model = Model()
    new_model.load_state_dict(torch.load('iris_dataset_nn.pt))

'''
