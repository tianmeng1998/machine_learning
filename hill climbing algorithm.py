import gym
import numpy as np
import matplotlib.pyplot as plt


def run_episode(env, parameters):
    observation = env.reset()
    totalreward = 0
    counter = 1
    for _ in range(200):
        # env.render()
        action = 0 if np.matmul(parameters, observation) < 0 else 1
        observation, reward, done, info = env.step(action)
        totalreward += reward
        counter += 1
        if done:
            break
    return totalreward


def train(submit):
    env = gym.make('CartPole-v0')
    if submit:
        env.monitor.start('cartpole-hill/', force=True)

    episodes_per_update = 5
    noise_scaling = 0.2
    parameters = np.random.rand(4) * 2 - 1
    bestreward = 0
    counter = 0

    for _ in range(200):
        counter += 1
        newparams = parameters + (np.random.rand(4) * 2 - 1) * noise_scaling
        # print newparams
        # reward = 0
        # for _ in xrange(episodes_per_update):
        #     run = run_episode(env,newparams)
        #     reward += run
        reward = run_episode(env, newparams)
        # print "%d: reward %d best %d" % (counter, reward, bestreward)
        if reward > bestreward:
            # print "update"
            bestreward = reward
            parameters = newparams
            if reward == 200:
                break

    if submit:
        for _ in range(100):
            run_episode(env, parameters)
        env.monitor.close()
    return counter


# r = train(submit=False)
# print r

results = []
for _ in range(1000):
    results.append(train(submit=False))
weights = np.ones_like(results)/float(len(results))
plt.hist(results, 10, weights=weights)
# plt.hist(results, 50, normed=1, facecolor='g', alpha=0.75)
plt.xlabel('Episodes required to reach 200')
plt.ylabel('Frequency')
plt.title('Histogram of Hill Climbing Search')
plt.show()