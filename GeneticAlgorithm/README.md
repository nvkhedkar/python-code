# Genetic Algorithm

- Simple implementation of a GA to run on distributed systems
- Run by setting parameters and defining objective function in genetic_runner.py
- All run info stored in Json files, which can be pushed to cache/db/blob storage to enable distributed task runs
- Each task is independent to be able to run on different machines
- User can define input and output functions in genetic_data.py for each task 
- These functions can be used to push data to cache/db/blob storage

## Links
[sobol squuence](https://stackoverflow.com/questions/55788739/monte-carlo-simulations-in-python-using-quasi-random-standard-normal-numbers-usi)
