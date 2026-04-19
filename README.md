# Hash Brute-Force: Parallel vs Sequential

## Overview
This repository contains a Python-based benchmarking tool designed to compare the performance of **Sequential**, **Multithreading**, and **Multiprocessing** approaches for MD5 hash brute-forcing. It evaluates execution times, speedup, and scalability across different operating systems and hardware configurations.

## Features
- **MD5 Hash Brute-Forcing:** Attempts to find the original numeric value of a given MD5 hash.
- **Execution Modes:** Supports Sequential, Parallel via Threads, and Parallel via Processes.
- **Automated Benchmarking:** Runs multiple test iterations, logs system hardware/OS information, and outputs the results to a CSV file.
- **Data Visualization:** Includes a dedicated script (`PlotarDados.py`) to generate comprehensive charts (Scalability Curves, Speedup, Execution Time, and Thread vs. Process Efficiency) using `pandas`, `matplotlib`, and `seaborn`.

## Project Structure
- `main.py`: The entry point for the benchmarking script. Manages execution scenarios and logging.
- `hash_finder.py`: Contains the core logic for the brute-force search (sequential and parallel implementations).
- `os_info.py`: Collects system hardware and OS details (CPU, RAM, OS version) for the benchmark logs.
- `write_results.py`: Utility module to export benchmark results to a CSV format.
- `PlotarDados.py`: Data analysis and visualization script to process `datasetFinal.csv` and generate plots.
- `requirements.txt`: List of Python dependencies required to run the project.

## Installation

1. Clone the repository.

2. Install the required dependencies:

```Bash
pip install -r requirements.txt
```
Note: To run the data visualization script, you will also need to install pandas, matplotlib, and seaborn, which can be installed via pip install pandas matplotlib seaborn.

## Usage

**Running the Benchmark**

You can run the benchmark using the `main.py` script.

```Bash
python main.py -n <target_base_number> -m <max_search_limit> -t <number_of_workers>
```

**Arguments**:

- `-n`, `--number`: The base number to generate the target MD5 hash (Required).
- `-m`, `--max_entries`: The maximum search limit for the brute-force algorithm (Required).
- `-t`, `--threads`: Number of threads/processes to use (Default: 1).
- `--num_tests`: Number of iterations for each scenario (Default: 30).
- `-f`, `--filename`: Name of the output CSV file (Default: resultados_benchmark.csv).
- `--sleep`: Cooldown time (in seconds) between different execution scenarios (Default: 300).

**Example**:

```Bash
python main.py -n 123456 -m 1000000 -t 4 --num_tests 10 --sleep 60
```

**Generating Plots**

After generating the dataset (saving as datasetFinal.csv), run the plotting script to visualize the results:

```Bash
python PlotarDados.py
```
