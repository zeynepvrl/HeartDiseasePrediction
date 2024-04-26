# -*- coding: utf-8 -*-
"""HeartDiseasePredictionSwitzerland.ipynb adlı not defterinin kopyası001ödevigöndermedenönceki

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/10lJcrQ74ns8j5i0yeqffTVNuGoX6JvbJ
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from google.colab import drive
drive.mount('/content/drive')

column_names = ['age', 'sex','cp','trestbps','chol','fbs','resteccg','thalach','exange','oldpeak','slope','ca','thall', 'num']
df = pd.read_csv('/content/drive/MyDrive/deneme1.data',header=None ,names=column_names ,na_values='?')

x=df.drop(['num' ,'ca','thall','slope'],axis=1).values         #Dataframe değil de numpy array formatında olması için sonuna .values ekledim
y=df['num']

df

print(df.isnull().sum())

x

"""Taking care of missing data"""

y

from sklearn.impute import SimpleImputer
imputer = SimpleImputer(missing_values=np.nan , strategy='mean')
imputer.fit(x[: ,3:10])                                              #bu adımda sadece ortalama değer hesaplanır
x[: ,3:10]=imputer.transform(x[: ,3:10])                             #Eksik değerleri doldurulan dataset, dönüştürülmüş dataset olarak döndürülür.  SimpleImputer kullanırken np.array işlemi gerekli değildir.  doğrudan dönüştürülmüş veriyi döndürdüğü için, bu dönüştürülmüş veriyi doğrudan kullanabilirsiniz.
x

from plotly.express import scatter
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)

# PCA modeli oluşturma
pca = PCA(n_components=2)
x_pca = pca.fit_transform(x_scaled)
pca_df = pd.DataFrame(x_pca, columns=["x", "y"])

y_df=pd.DataFrame(y, columns=["num"])

plot_df = pd.concat(objs=[y_df, pca_df], axis=1)

scatter(data_frame=plot_df, x='x', y='y', color='num', height=500)

class_counts = df['num'].value_counts()
print(class_counts)

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)                               #split den sonda yapsan daha iyi olabilir, y ye de uygulaman gerekeilir

# Veri setini bölme
x_train, x_test, y_train, y_test = train_test_split(x_scaled, y, test_size=0.2, random_state=100)
# Random Forest Classifier modelini oluşturma ve eğitme
class_weights = {0:1, 1:1, 2:2, 3:2, 4:8}
rf_classifier =RandomForestClassifier(class_weight=class_weights, random_state=100)
rf_classifier.fit(x_train, y_train)

# Test verisi üzerinde modelin performansını değerlendirme
y_pred = rf_classifier.predict(x_test)

# Sınıflandırma raporunu oluşturma
report = classification_report(y_test, y_pred)
print("RandomForestClassifier Sınıflandırma Raporu:")
print(report)

"""WUHUUUUUU ACC YÜKSELDİ, SMOTE SAYESİNDE:"""

from imblearn.over_sampling import SMOTE

smote = SMOTE(random_state=42)
x_resampled, y_resampled = smote.fit_resample(x_train, y_train)

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures

scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)

# Polinom özelliklerini oluşturma
poly = PolynomialFeatures(degree=6)
X_train_poly = poly.fit_transform(x_resampled)

# Veri setini bölme
x_train, x_test, y_train, y_test = train_test_split(X_train_poly, y_resampled, test_size=0.2, random_state=100)
# Random Forest Classifier modelini oluşturma ve eğitme
class_weights = {0:1, 1:1, 2:2, 3:2, 4:8}
rf_classifier =RandomForestClassifier(class_weight=class_weights, random_state=100)
rf_classifier.fit(x_train, y_train)

# Test verisi üzerinde modelin performansını değerlendirme
y_pred = rf_classifier.predict(x_test)

# Sınıflandırma raporunu oluşturma
report = classification_report(y_test, y_pred)
print("RandomForestClassifier Sınıflandırma Raporu:")
print(report)

from sklearn.model_selection import GridSearchCV

# GridSearchCV için parametrelerin olası değerlerini belirleyin
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_features': ['auto', 'sqrt', 'log2']
}

# GridSearchCV nesnesini oluşturun
grid_search = GridSearchCV(RandomForestClassifier(class_weight=class_weights, random_state=100), param_grid, cv=5, scoring='accuracy')

# Eğitim veri seti üzerinde GridSearchCV'yi uygulayın
grid_search.fit(x_train, y_train)

# En iyi parametreleri ve en iyi skoru görüntüleyin
print("En iyi parametreler:", grid_search.best_params_)
print("En iyi skor:", grid_search.best_score_)

# En iyi modeli alın
best_rf_classifier = grid_search.best_estimator_

# En iyi modeli kullanarak tahmin yapın
y_pred_best = best_rf_classifier.predict(x_test)

# Sınıflandırma raporunu oluşturma
report_best = classification_report(y_test, y_pred_best)
print("En iyi Random Forest Classifier Sınıflandırma Raporu:")
print(report_best)

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report

scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)

# Veri setini bölmek
x_train, x_test, y_train, y_test = train_test_split(x_scaled, y, test_size=0.2, random_state=100)
# Karar ağacı modelini oluşturma
decision_tree_model = DecisionTreeClassifier(class_weight='balanced')

# Karar ağacı modelini eğitme
decision_tree_model.fit(x_train, y_train)

# Test verisi üzerinde modelin performansını değerlendirme
y_pred = decision_tree_model.predict(x_test)

# Sınıflandırma raporunu oluşturma
report = classification_report(y_test, y_pred)
print("DecisionTreeClassifier Sınıflandırma Raporu:")
print(report)

from sklearn.ensemble import GradientBoostingClassifier

# Gradient Boosting Classifier modelini oluşturma ve eğitme
gb_classifier = GradientBoostingClassifier()
gb_classifier.fit(x_train, y_train)

# Test verisi üzerinde modelin performansını değerlendirme
y_pred = gb_classifier.predict(x_test)

# Sınıflandırma raporunu oluşturma
report = classification_report(y_test, y_pred)
print("GradientBoostingClassifier Sınıflandırma Raporu:")
print(report)

from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import precision_score, recall_score
from sklearn.metrics import classification_report

# Destek Vektör Makineleri modelini oluşturun ve eğitin

scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)

x_train, x_test, y_train, y_test = train_test_split(x_scaled, y, test_size=0.2, random_state=100)

svm_model = SVC()  # Lineer çekirdek kullanıyoruz
svm_model.fit(x_train, y_train)   # eğitiyotuz verilerimizle

# Test seti üzerinde tahmin
y_pred = svm_model.predict(x_test)

# Sınıflandırma raporunu oluşturma
report = classification_report(y_test, y_pred)
print("SVC Sınıflandırma Raporu:")
print(report)

"""svc deki bu uyarıların sebebi , datasetimizde class dağılımları dengesiz , bazı class lar için çok az sayıda instance var, ve svc buna dayanıklı bir yapıya sahip değil, bazı class lar için değerlendirmede yetersiz kalıp bu uyarıları veriyor

"""

from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split

# Hiperparametre aralıklarını belirleme
param_grid = {
    'C': [0.1, 1, 10, 100],  # C parametresi için değerler
    'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],  # Kernel tipi için seçenekler
    'degree': [2, 3, 4],  # Polinom çekirdeği için dereceler
    'gamma': ['scale', 'auto', 0.1, 1]  # Gamma parametresi için değerler
}

# SVC modeli oluşturma
svm_model = SVC(kernel='cuda')

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=100)

# GridSearchCV veya RandomizedSearchCV modeli oluşturma ve eğitme
grid_search = GridSearchCV(svm_model, param_grid, cv=5, scoring='accuracy')
grid_search.fit(x_train, y_train)

# En iyi parametreleri ve en iyi doğruluk skorunu bulma
print("En iyi parametreler:", grid_search.best_params_)
print("En iyi doğruluk skoru:", grid_search.best_score_)

from sklearn.neighbors import KNeighborsClassifier

# KNN modelini oluşturma ve eğitme
knn_model = KNeighborsClassifier(n_neighbors=5)
knn_model.fit(x_train, y_train)

# Modelin performansını test veri setiyle değerlendirme
y_pred = knn_model.predict(x_test)

# Sınıflandırma raporunu oluşturma
report = classification_report(y_test, y_pred)
print("KNeighborsClassifier Sınıflandırma Raporu:")
print(report)

import pandas as pd
from sklearn.model_selection import train_test_split
from pycaret.classification import setup, compare_models

column_names = ['age', 'sex','cp','trestbps','chol','fbs','resteccg','thalach','exange','oldpeak','slope','ca','thall', 'num']
df = pd.read_csv('/content/drive/MyDrive/updated.data',header=None ,names=column_names ,na_values='?')

x=df.drop(['num' ,'ca','fbs','slope'],axis=1).values         #Dataframe değil de numpy array formatında olması için sonuna .values ekledim
y=df['num']

# NumPy dizisini DataFrame'e dönüştürme
x_df = pd.DataFrame(data=x, columns=['age', 'sex','cp','trestbps','chol','resteccg','thalach','exange','oldpeak','thall'])  # Sütun isimleri, veri setinizdeki sütunların gerçek isimleriyle değiştirilmelidir

# SimpleImputer'ı kullanarak eksik değerleri ortalama ile doldurma
imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
x_df.iloc[:, 3:10] = imputer.fit_transform(x_df.iloc[:, 3:10])


# Veri setini bölmek
x_train, x_test, y_train, y_test = train_test_split(x_df, y, test_size=0.2, random_state=0)


# Sütun adlarını el ile belirleme (örneğin, x' in sütunları 'feature1', 'feature2', ... şeklinde)
column_names = ['age', 'sex','cp','trestbps','chol','resteccg','thalach','exange','oldpeak','thall']

# NumPy dizilerini DataFrame'lere dönüştürme
x_train_cls_df = pd.DataFrame(x_train, columns=column_names)
y_train_cls_df = pd.DataFrame(y_train, columns=['num'])

# Veri çerçevelerini birleştirme
train_df_cls = pd.concat([x_train_cls_df, y_train_cls_df], axis=1)

# Pycaret'in setup fonksiyonunu kullanarak veri setini hazırlama
setup_cls = setup(data=train_df_cls, target='num')

# En iyi modeli seçme
best_cls_model = compare_models()

from h2o.automl import H2OAutoML
from sklearn.model_selection import train_test_split
import h2o
import pandas as pd
import numpy as np

# H2O'yu başlatma
h2o.init()


column_names = ['age', 'sex','cp','trestbps','chol','fbs','resteccg','thalach','exange','oldpeak','slope','ca','thall', 'num']
df = pd.read_csv('/content/drive/MyDrive/processed.switzerlandUpdated.data',header=None ,names=column_names ,na_values='?')

x=df.drop(['num' ,'ca','fbs','slope'],axis=1).values         #Dataframe değil de numpy array formatında olması için sonuna .values ekledim
y=df['num']

# NumPy dizisini DataFrame'e dönüştürme
x_df = pd.DataFrame(data=x, columns=['age', 'sex','cp','trestbps','chol','resteccg','thalach','exange','oldpeak','thall'])  # Sütun isimleri, veri setinizdeki sütunların gerçek isimleriyle değiştirilmelidir

# SimpleImputer'ı kullanarak eksik değerleri ortalama ile doldurma
imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
x_df.iloc[:, 3:10] = imputer.fit_transform(x_df.iloc[:, 3:10])


# Veri setini bölmek
x_train, x_test, y_train, y_test = train_test_split(x_df, y, test_size=0.2, random_state=0)

# Dizileri DataFrame'lere dönüştürme
train_df = pd.DataFrame(data=x_train, columns=x_df.columns)  # x.columns, x'in sütun adlarını temsil eder
train_df['num'] = y_train  # Etiket sütununu ekleyin

test_df = pd.DataFrame(data=x_test, columns=x_df.columns)
test_df['num'] = y_test

# H2O çerçevelerine dönüştürme
train_h2o = h2o.H2OFrame(train_df)
test_h2o = h2o.H2OFrame(test_df)

# H2O AutoML modelini oluşturma
aml = H2OAutoML(max_models=10, seed=1)
aml.train(y='num', training_frame=train_h2o)  # target_column_name, y sütununun adını temsil ediyor

# En iyi modeli seçme
best_h2o_model = aml.leader

# Test veri setinden bir örnekleme çerçevesi oluşturma
test_sample = test_h2o[0:12]  # İlk 12 örnek için örnekleme çerçevesi oluşturma

# En iyi modelin açıklamasını alma
explanation = best_h2o_model.explain(test_sample)

best_model_name = aml.leader.model_id
print("En iyi modelin ismi:", best_model_name)

import pandas as pd
from sklearn.model_selection import train_test_split
import h2o
from h2o.automl import H2OAutoML

# H2O'yu başlatma
h2o.init()

df.fillna(df.mean(), inplace=True)

# H2O çerçevesine dönüştürme
h2o_df = h2o.H2OFrame(df)

# Hedef sütunun belirlenmesi
x = h2o_df.columns
y = "num"
x.remove(y)

# Eğitim ve test setlerine ayırma
train, test = h2o_df.split_frame(ratios=[0.8], seed=42)

# H2O AutoML modelini oluşturma
aml = H2OAutoML(max_models=10, seed=1)
aml.train(x=x, y=y, training_frame=train)

# En iyi modelin ismini alınması
best_model = aml.leader
print("En iyi modelin ismi:", best_model.model_id)

# Test seti üzerinde modelin performansının değerlendirilmesi
perf = best_model.model_performance(test_data=test)
print("Test seti üzerinde modelin performansı:", perf)