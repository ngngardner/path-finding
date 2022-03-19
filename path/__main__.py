"""Main module."""

from path.environment import Environment, get_ground_truth


def main():
    env = Environment((8, 8))
    env.reset()
    env.render()
    get_ground_truth(env)


if __name__ == "__main__":
    main()
