import numpy as np
import python_speech_features as sf
from sklearn.base import BaseEstimator, ClassifierMixin


class MFCC(BaseEstimator, ClassifierMixin):
    def fit(self, X, y):
        return self

    @staticmethod
    def transform(X):
        return np.array([sf.mfcc(sample, 44100, 0.01, 0.0025, 32, 32, preemph=0, highfreq=12000, ceplifter=0,
                                 appendEnergy=False).flatten() for sample in X])
