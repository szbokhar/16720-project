import numpy as np
from numpy.linalg import inv, det
import math

class GaussianModel:

    def __init__(self, mu, sigma):
        self.mu = mu
        self.sigma = sigma

    def eval(self, x):
        mx = x - self.mu
        ex = -1/2*np.dot(np.dot(mx.transpose(), inv(self.sigma)), mx)
        coef = 1/math.sqrt((2*math.pi)**self.mu.size*det(self.sigma))
        return coef*math.exp(ex)

    def set_mu(self, mu):
        self.mu = mu

    def set_sigma(self, sigma):
        self.sigma = sigma

class GaussianMixtureModel:

    def __init__(self, k, mus, sigmas):
        self.models = []
        self.k = k
        for i in range(k):
            self.models.append(GaussianModel(mus[i], sigmas[i]))

    def eval(self, x):
        val = []
        for i in range(self.k):
            val.append(self.models[i].eval(x))

        val = np.array(val)/np.sum(np.array(val))
        return val

