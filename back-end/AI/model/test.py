from intent_svm import IntentSVM
svm = IntentSVM("/home/matheusg/Documents/UNASP/BusSense/back-end/AI/model/intent_svm.pkl", threshold=0.55)
pred, conf = svm.predict("Quero ")
print(pred, conf)
