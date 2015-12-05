import numpy as np

class HiddenMarkovModel:

    def __init__(self, model_path):
        self.A = np.genfromtxt(model_path+'_a.csv', delimiter=",")
        self.B = np.genfromtxt(model_path+'_b.csv', delimiter=",")
        self.p = np.genfromtxt(model_path+'_p.csv', delimiter=",")
        self.O = np.genfromtxt(model_path+'_obs.csv', delimiter=",")
        self.obser = []
        self.seq_length = 25

    def log_observation(self, obs):
        o = np.sum(np.square(self.O - np.tile(np.array(obs), [self.O.shape[0], 1])),1)
        self.obser.append(np.argmin(o))
        l = len(self.obser)
        if l > self.seq_length:
            self.obser = self.obser[l-self.seq_length:]

        # print(self.obser)

    def reset_observations(self, keep=None):
        if keep is None:
            self.obser = []
        else:
            self.obser = self.obser[-keep:]

    def compute_likelihood(self):
        val = [-10000]
        for i in range(15,len(self.obser)):
            fw = self.forward(self.obser[-i-1:])
            val.append(np.log(np.sum(fw[-1,:]))/(i+1))
            srt = np.argsort(fw[-1,:])

        return val[-1]

    def forward(self, X):
        a = self.A
        b = self.B
        p = self.p
        K = a.shape[0]
        T = len(X)

        alpha = np.zeros([T,K])
        alpha[0,:] = b[:, X[0]]*p

        for i in range(1,T):
            alpha[i,:] = np.dot(alpha[i-1,:], a)*b[:,X[i]]

        return alpha
