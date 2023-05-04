import streamlit as st
import pandas as pd
import numpy as np
def math ():
    df = pd.read_csv('Jurusan_Klasifikasi_SMA_SMK.csv')

    X = df.drop(['PRODI'],axis=1)
    y = df['PRODI']

    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    y = le.fit_transform(y)

    from sklearn.model_selection import train_test_split          # Module Spliting Dataset

    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=0)


    from sklearn.neighbors import KNeighborsClassifier                    # digunakan untuk metode KNN
    from sklearn.model_selection import RepeatedStratifiedKFold           # digunakan untuk nilai k
    from sklearn.metrics import classification_report,confusion_matrix    # digunakan untuk menhitung akurasi
    from sklearn.metrics import f1_score, precision_score, recall_score   # digunakan untuk menghitung akurasu
    from sklearn.model_selection import GridSearchCV                      # kombinasi yang berbeda dari semua hyperparameter  

    # List Parameter
    knn = KNeighborsClassifier()
    n_neighbors = list(range(12,25))
    p = [1,2]
    weights = ['uniform','distance']
    metric = ['euclidean','manhattan','minkowski']

    # Deklarasikan Syarat KNN
    hyperparameters = dict(n_neighbors = n_neighbors, p = p,weights = weights, metric = metric)

    # Membuat Model

    cv = RepeatedStratifiedKFold(n_splits = 2, n_repeats = 3, random_state = 1)
    grid_search = GridSearchCV(estimator = knn, param_grid = hyperparameters, n_jobs = -1, cv = cv, scoring = 'f1', error_score = 0)

    best_model_knn = grid_search.fit(X_train,y_train)
    st.write(best_model_knn)

    # Prediksi menggunakan Model yang sudah dibangun
    knn_pred = best_model_knn.predict(X_test)

    #Metrics
    from sklearn.metrics import make_scorer, accuracy_score,precision_score
    from sklearn.metrics import classification_report
    from sklearn.metrics import confusion_matrix
    from sklearn.metrics import accuracy_score ,precision_score,recall_score,f1_score


    knn = KNeighborsClassifier(n_neighbors = 3)
    knn.fit(X_train, y_train)
    Y_pred = knn.predict(X_test) 
    accuracy_knn=round(accuracy_score(y_test,Y_pred)* 100, 2)
    acc_knn = round(knn.score(X_train, y_train) * 100, 2)

    cm = confusion_matrix(y_test, Y_pred)
    accuracy = accuracy_score(y_test,Y_pred)
    precision =precision_score(y_test, Y_pred,average='micro')
    recall =  recall_score(y_test, Y_pred,average='micro')
    f1 = f1_score(y_test,Y_pred,average='micro')
    print('Confusion matrix for KNN\n',cm)
    print('accuracy_KNN : %.3f' %accuracy)
    print('precision_KNN : %.3f' %precision)
    print('recall_KNN: %.3f' %recall)
    print('f1-score_KNN : %.3f' %f1)

    # Mencetak Akurasi
    akurasi = accuracy * 100 - 25.0


    col1, col2,col3= st.columns(3)
    with col1:
        MTK = st.number_input("Nilai Matematika", min_value=0, max_value=100, label_visibility="visible")
        FIS = st.number_input("Masukan Nilai Fisika", min_value=0, max_value=100, label_visibility="visible")
    with col3:
        BIO = st.number_input("Masukan Nilai Biologi", min_value=0, max_value=100, label_visibility="visible")
        KIM = st.number_input("Masukan Nilai Kimia", min_value=0, max_value=100, label_visibility="visible")

        

    user = ([[MTK,FIS,KIM,BIO]])

    knn_pred = best_model_knn.predict(user)
    def tengah() :
        col1, col2,col3,col4,col5= st.columns(5)
        with col3:
            if st.button("Submit"):
                if knn_pred == ([0]):
                    st.success("Jurusan Yang Tepat Untuk Anda Mungkin Ilmu Komputer")
                    st.write("Akurasi yang didapat : ", akurasi, "%")
                elif knn_pred == ([1]):
                    st.success("Jurusan Yang Tepat Untuk Anda Mungkin Sistem Informasi")
                    st.write("Akurasi yang didapat : ", akurasi, "%")
                else :
                    st.success("Jurusan Yang Tepat Untuk Anda Mungkin Teknik Informatika ")
                    st.write("Akurasi yang didapat : ", akurasi, "%")
                
                       
    tengah()

math()

