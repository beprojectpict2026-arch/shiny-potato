from matplotlib import cm
import pandas as pd
from sklearn.neural_network import MLPClassifier
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score,f1_score,recall_score,confusion_matrix,classification_report,precision_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("Churn_Modelling.csv")

df.info()

print(df.isnull().sum())

df.drop(["RowNumber","CustomerId","Surname"],axis=1,inplace=True)



x = df.drop("Exited",axis=1)
y = df["Exited"]

x = pd.get_dummies(x,columns=["Geography","Gender"],drop_first=True)

X_train,X_test,Y_train,Y_test = train_test_split(
    x,y,test_size = 0.2,random_state = 42   
)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

mlp = MLPClassifier(
    max_iter = 100,
    early_stopping=True,
    hidden_layer_sizes=(16,8),
    random_state=42
)

mlp.fit(X_train,Y_train)
mlp_pred = mlp.predict(X_test)

cm  = confusion_matrix(Y_test,mlp_pred)

print("MLP classifier model Metrics\n")
print("Accuracy: ",accuracy_score(Y_test,mlp_pred))
print("Precision: ",precision_score(Y_test,mlp_pred))
print("recall: ",recall_score(Y_test,mlp_pred))
print("f1 score: ",f1_score(Y_test,mlp_pred))

sns.heatmap(
    cm,annot=True,fmt=".2f",cmap="Blues",
    xticklabels=["Stay","Not Stay"],
    yticklabels=["Stay","Not Stay"]
)
plt.title("confusion matrix for MLP classifier")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()



