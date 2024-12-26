# advent-of-code-2024

Solutions for the [Advent of Code 2024](https://adventofcode.com/2024)

Run the solution for one day (requires Python version 3.12 or higher):
```shell
python src/day-20.py --input data/input-20.txt
```

Run all solutions:
* fish
  ```shell
  for n in (seq -w 1 25); python src/day-$n.py --input data/input-$n.txt; end
  ```
* bash, zsh
  ```shell
  for n in {01..25}; do python src/day-$n.py --input data/input-$n.txt; done
  ```
