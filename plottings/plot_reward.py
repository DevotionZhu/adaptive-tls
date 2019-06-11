import json
import matplotlib.pyplot as plt

from datetime import datetime


def parse_date(_date):
    return datetime.strptime(_date, '%Y-%m-%d_%H-%M-%S')


def extract_results(_filepath):
    _epoch = None
    _prev_reward = 0
    _rewards = []
    _timestamps = []

    with open(_filepath) as f:
        for line in f:
            results = json.loads(line)

            if _epoch is None:
                _epoch = parse_date(results['date'])

            _new_reward = results['episode_reward_mean']
            if _prev_reward != _new_reward \
                    and _new_reward == _new_reward:  # NaN check
                _rewards.append(_new_reward)

                _time_passed = parse_date(results['date']) - _epoch
                _timestamps.append(round(_time_passed.seconds/3600, 2))

                _prev_reward = _new_reward
    return _timestamps, _rewards


if __name__ == '__main__':
    filepaths = [
        '/home/gosha/ray_results/NO-TUNING-QUEUES2/result.json',  # DQN Agent
    ]

    agents = ['DQN', '', '']
    color = ['purple', '', '']
    marker = ['o', '', '']

    plt.figure(figsize=(7, 4))
    # plt.ylim([4000, 6600])
    plt.ylim([-3200, -200])
    plt.xlim([0, 8])
    plt.locator_params(axis='y', nbins=10)
    plt.locator_params(axis='x', nbins=12)

    for idx, filepath in enumerate(filepaths):
        timestamps, rewards = extract_results(filepath)
        plt.plot(timestamps, rewards, color=color[idx], lw=1, label=agents[idx],
                 marker=marker[idx], markevery=0.1, ms=5)

    plt.ylabel('Episode mean reward (Queue Length)', fontsize=11)
    plt.xlabel('Time elapsed (Hours)', fontsize=11)
    plt.legend(loc="lower right", prop={'size': 11})
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('Reward_Queues')
