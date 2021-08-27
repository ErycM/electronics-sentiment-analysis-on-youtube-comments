def model_parallel(l, i):
    l.acquire()
    try:
        param_grid = [
            {'C': [1, 10, 100, 1000]}
        ] 
        svc = LinearSVC()

        X_train_w2v, X_test_w2v, y_train_w2v, y_test_w2v = train_test_split(X_w2v, df['final_type'], test_size = .2)
        X_train_w2v, y_train_w2v = overSamplDef(X_train_w2v, y_train_w2v, ADASYN, sampling_strategy='minority') #SMOTE | SMOTE
        clf = GridSearchCV(svc, param_grid).fit(X_train_w2v, y_train_w2v)
        y_pred_w2v = clf.predict(X_test_w2v)

        param_grid = [
            {'C': [1, 10, 100, 1000]}
        ] 
        svc = LinearSVC()

        X_train_lsa, X_test_lsa, y_train_lsa, y_test_lsa = train_test_split(X_lsa, df['final_type'], test_size = .2)
        X_train_lsa, y_train_lsa = overSamplDef(X_train_lsa, y_train_lsa, ADASYN, sampling_strategy='minority') #SMOTE | SMOTE
        clf = GridSearchCV(svc, param_grid).fit(X_train_lsa, y_train_lsa)
        y_pred_lsa = clf.predict(X_test_lsa)

        svc_w2v = classification_report(y_test_w2v, y_pred_w2v, output_dict=True)
        predict_w2v_traning.append(svc_w2v)

        svc_lsa = classification_report(y_test_lsa, y_pred_lsa, output_dict=True)
        predict_lsa_traning.append(svc_lsa)
    finally:
        l.release()





if __name__ == '__main__':
    lock = Lock()

    from multiprocessing import Process, Lock

    model_report = pd.DataFrame()
    predict_w2v_traning = []
    predict_lsa_traning = []

    for num in range(600):
        Process(target=model_parallel, args=(lock, num)).start()

    model_w2v_report = pd.json_normalize(predict_w2v_traning)
    model_lsa_report = pd.json_normalize(predict_lsa_traning)

    model_w2v_report.to_csv('w2v_report2.csv', index=False)
    model_lsa_report.to_csv('lsa_report2.csv', index=False)


# from multiprocessing import Process, Lock

# def f(l, i):
#     l.acquire()
#     try:
#         print('hello world')
#     finally:
#         l.release()

# if __name__ == '__main__':
#     lock = Lock()

#     for num in range(10):
#         Process(target=f, args=(lock, num)).start()