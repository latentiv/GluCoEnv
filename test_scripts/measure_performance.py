import time
from glucoenv import T1DEnv
import gc
import argparse
from csv import writer

import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('--device', type=str, default='cpu')
parser.add_argument('--n_env', type=int, default=3)
args = parser.parse_args()

if __name__ == '__main__':
    device = args.device
    n_env = args.n_env
    steps = 100

    names = ['adolescent#001']#, 'adolescent#002']
    n_envs = [1, 2, 3] #, 4, 5, 10] #[1, 5, 10, 20, 100, 1000]
    name = 'adolescent#001'
    exec_times = []
    trials = 5
    for n_env in n_envs:
        trial_exec = []
        for i in range(0, trials):
            env = T1DEnv.make(env=name, n_env=n_env, scenario='moderate', device=device)
            SBB = T1DEnv.benchmark_controller(env=name, n_env=n_env, sample_time=env.sample_time,
                                              mode='perfect', device=device)
            action = SBB.init_action()
            print('\nn_env:{} '.format(n_env))
            tstart = time.perf_counter()
            for i in range(0, steps):
                obs, rew, done, info = env.step(action)
                action = SBB.get_action(glucose=obs, done=done, meal=info['SBB_MA'], t=info['time'])
            tstop = time.perf_counter()
            print((tstop- tstart)/60)
            trial_exec.append((tstop- tstart)/60)
            del env
            del SBB
            gc.collect()
        exec_times.append(trial_exec)

    print(n_envs)
    print(exec_times)

        # print('\nnenv: ', n_env)
        # print('steps: ', steps)
        # print('execution time:', execution_time)
        # exec_times.append(execution_time)

    # plt.plot(n_envs, exec_times)
    # plt.show()


    # names = ['adolescent#001', 'adolescent#002', 'adolescent#003', 'adolescent#004', 'adolescent#005',
    #          'adolescent#006', 'adolescent#007', 'adolescent#008', 'adolescent#009', 'adolescent#010']

    # for name in names:
    #     env = T1DEnv.make(env=name, n_env=n_env, scenario='moderate', device=device)
    #     SBB = T1DEnv.benchmark_controller(env=name, n_env=n_env, sample_time=env.sample_time,
    #                                       mode='perfect', device=device)
    #     action = SBB.init_action()
    #     start = time.time()
    #     for i in range(0, steps):
    #         obs, rew, done, info = env.step(action)
    #         action = SBB.get_action(glucose=obs, done=done, meal=info['SBB_MA'], t=info['time'])
    #     end = time.time()
    #     execution_time = (end-start)
    #     del env
    #     del SBB
    #     gc.collect()
    #
    #     print('\nnenv: ', n_env)
    #     print('steps: ', steps)
    #     print('execution time:', execution_time)
    #
    #     # FILE_NAME = 'data/'+str(n_env) + '_' + device + '_' + str(steps) +'.csv'
    #     # with open(FILE_NAME, 'a', newline='') as f_object:
    #     #     writer_object = writer(f_object)
    #     #     writer_object.writerow([execution_time])
    #     #     f_object.close()
