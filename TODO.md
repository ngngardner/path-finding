# Research Project - Custom Path-Finding Agent

## Goals

1. Create custom environment
2. Define agent behavior
3. Wrap in Gym.env API
4. Train model
5. Evaluate results
6. Write final report/presentation

## Custom Research Environment

### Done

- [x] Environment size (>16x16)
- [x] Orthogonal movement
- [x] Fixed and Random (compare)
      a. Starting location
      b. Goal location
- [x] Way to ensure that a path exists
- [x] Random generation
      a. Obstacles
      b. Traps (slows down agent)

### Todo

1. Agent no longer takes lowest cost path with traps.
2. How to bootstrap agent
   1. Give rewards along the path
   2. Add experiences to memory replay
3. Give reward/punishment for moving into trap
4. Test with random agent initialization

### Stretch

1. Obstacles of random sizes (blobs)

### Notes

1. Output state will be either centered around agent, or entire environment.
2. Can experiment and compare fixed and random starting and goal locations

### Challenges

1. Agent no longer takes lowest cost path with traps.
2. We tried to implement djikstra's.
