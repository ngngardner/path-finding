
from path.environment import Environment
from path.ground_truth import get_ground_truth


def main():
    env = Environment((8, 8))
    env.reset()
    env.render()
    ground_truth = get_ground_truth(env)
    print(ground_truth)


if __name__ == "__main__":
    main()
