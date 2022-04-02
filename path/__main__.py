"""Main module."""

from tensorforce import Environment as Env
from tensorforce import Agent, Runner

import path.const as const
from path.environment import Environment, get_ground_truth


def main():
    environment = Env.create(
        environment=Environment, max_episode_timesteps=100,
    )

    # Instantiate a Tensorforce agent
    agent = Agent.create(
        agent='configs/dqn.json',
        # alternatively: states, actions, (max_episode_timesteps)
        environment=environment,
    )

    # bootstrap agent
    # get ground truth experiences
    for boot_ep in range(100):
        print('Bootstrapping episode {}'.format(boot_ep))
        env = Environment()
        env.reset()
        episode_states = list()
        episode_actions = list()
        episode_terminal = list()
        episode_reward = list()

        # transform experiences to lists of attributes
        experiences = env.ground_truth
        for experience in experiences:
            episode_states.append(experience['state'])
            episode_actions.append(experience['action'])
            episode_terminal.append(experience['done'])
            episode_reward.append(experience['reward'])

        # apply experience
        agent.experience(
            states=episode_states,
            actions=episode_actions,
            terminal=episode_terminal,
            reward=episode_reward,
        )

        # perform update
        agent.update()

    # run agent
    runner = Runner(
        agent=agent,
        environment=environment,
    )
    runner.run(num_episodes=10)

    # evaluation
    print(runner.run(num_episodes=10, evaluation=True))

    # Close agent and environment
    agent.close()
    environment.close()
    runner.close()


if __name__ == "__main__":
    main()
