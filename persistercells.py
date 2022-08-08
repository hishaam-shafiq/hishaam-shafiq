import numpy as np
import matplotlib.pyplot as plt

class BetHedging:
    """
    simulate bet-hedging strategy in changing environments.
    """
    
    def __init__(self, phe_dist, fit_mat, N0=1., record=True):
        """
        initialize population.
        inputs:
        phe_dist: 1-d array-like, phenotype distribution q[i] (should sum to 1).
        fit_mat: 2-d array-like, fitness matrix f[i,j] = number of offspring for phenotype i in environment j.
        N0: real, initial population size (use real instead of integer).
        record: bool, whether to record history of environment and population size.
        """
        self.phe_dist = np.asarray(phe_dist)    # phenotype distribution q_i
        self.fit_mat = np.asarray(fit_mat)    # fitness matrix f_{ij}
        self.pop_size = float(N0)    # current population size
        self.time = 0    # current number of generations since the beginning of simulation
        self.record = record
        if record:
            self.env_hist = []
            self.pop_hist = []
    
    def grow(self, env_seq):
        """
        simulation population growth in changing environments.
        inputs:
        env_seq: 1-d array-like, environment sequence, list of environment indices.
        """
        T = len(env_seq)
        for t in range(T):
            env = env_seq[t]    # environmental condition at each time step
            factor = np.dot(phe_dist, fit_mat[:,env])    # growth factor according to formula
            new_pop = self.pop_size * factor    # new population size at next time step
            if self.record:    # record history
                self.env_hist.append(env)
                self.pop_hist.append(self.pop_size)
            self.pop_size = new_pop    # update population size
            
env_dist = np.array([0.5, 0.5])    # environmental distribution
phe_dist = np.array([0.3, 0.7])    # phenotype distribution
fit_mat = np.array([[3., 0.],
                    [1., 1.]])    # fitness matrix

T = 1000    # number of time steps
env_seq = np.random.choice(2, size=T, p=env_dist)    # choose random environment sequence according to distribution

N0 = 1.    # initial population size
bh1 = BetHedging(phe_dist, fit_mat, N0=N0, record=True)    # create bet-hedging population
bh1.grow(env_seq)    # grow population under given environmental sequence

plt.figure()
plt.plot(bh1.pop_hist)
plt.yscale('log')
plt.xlabel('generations')
plt.ylabel('population size')
plt.show()

lam_avg = np.log(bh1.pop_size / N0) / T    # average growth rate 
pop_avg = N0 * np.exp(lam_avg * np.arange(T))    # trend line

lam_theory = np.dot(np.log(np.dot(phe_dist, fit_mat)), env_dist)    # asymptotic growth rate
pop_theory = N0 * np.exp(lam_theory * np.arange(T))    # theoretical trend line

plt.figure()
plt.plot(bh1.pop_hist)
plt.plot(pop_avg, label='average growth rate')
plt.plot(pop_theory, 'k', lw=1, label='theoretical growth rate')
plt.yscale('log')
plt.xlabel('generations')
plt.ylabel('population size')
plt.legend()
plt.show()

q1_list = np.arange(0.01, 1, 0.01)    # list of values for q_1
lam_avg_list = []    # list to collect average growth rates
lam_theory_list = []    # list to collect theoretical growth rates

for q1 in q1_list:
    phe_dist = [1-q1, q1]
    bh1 = BetHedging(phe_dist, fit_mat, N0=N0, record=True)
    env_seq = np.random.choice(2, size=T, p=env_dist)
    bh1.grow(env_seq)
    lam_avg = np.log(bh1.pop_size / N0) / T    # simulation result
    lam_theory = np.dot(np.log(np.dot(phe_dist, fit_mat)), env_dist)    # theoretical result
    lam_avg_list.append(lam_avg)
    lam_theory_list.append(lam_theory)
    
plt.figure()
plt.plot(q1_list, lam_avg_list, label='simulation')
plt.plot(q1_list, lam_theory_list, label='theory')
plt.xlabel(r'$q_1$')
plt.ylabel(r'$\Lambda$')
plt.legend()
plt.show()

imax = np.argmax(lam_theory_list)
print(f'optimal proportion of persisters = {q1_list[imax]}')
print(f'maximum growth rate = {lam_theory_list[imax]:.6f}')
