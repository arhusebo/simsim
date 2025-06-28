import time
import simsim


@simsim.experiment(path="./experiments/")
def long_duration(status: simsim.ExperimentStatus):
    n_iter = 10
    t_iter = 1.0
    status.max_progress = n_iter
    for i in range(n_iter):
        time.sleep(t_iter)
        status.progress = i+1
