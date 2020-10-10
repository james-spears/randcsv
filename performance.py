import math
from datetime import datetime
from itertools import combinations, product
from multiprocessing import cpu_count

import matplotlib.pyplot as plt
import numpy as np

from randcsv import RandCSV


def take_measurement(test_class, iterations=20, **kwargs):
    """Measures the synchronous initialization time of the provided
    test_class.

    :param test_class: Class to test
    :param iterations: number of test iterations
    :param kwargs: kwargs that class will be instantiated with
    :return:
    """
    measurements = []
    for h in range(iterations):
        start_time = datetime.now()
        test_class(**kwargs)
        execution_time = datetime.now() - start_time
        measurements.append(
            (
                kwargs['rows'] * kwargs['cols'],
                execution_time.total_seconds()
            )
        )
    return measurements


def least_squares(x, y):
    if len(x) != len(y):
        raise ValueError("length x != length y")

    num_of_pts = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xx = sum([val * val for val in x])
    sum_xy = sum([val[0] * val[1] for val in zip(x, y)])

    m = (num_of_pts * sum_xy - sum_x * sum_y) / (num_of_pts * sum_xx - sum_x ** 2)
    b = (sum_y - m * sum_x) / num_of_pts

    return m, b


def run_experiment(row_nums, col_nums, byte_nums, proc_nums, data_types):
    """Runs the test.

    :return: experimental results
    """
    results = {}
    total_tests = len(row_nums) * len(col_nums)
    fig, ax = plt.subplots(2, 2, figsize=(20, 10))
    for data_type in data_types:
        results[str(data_type)] = {}
        for byte_num in byte_nums:
            results[str(data_type)][byte_num] = {}
            for proc_num in proc_nums:
                results[str(data_type)][byte_num][proc_num] = {}
                for row_num in row_nums:
                    for col_num in col_nums:
                        iteration_num = row_num * col_num
                        results[str(data_type)][byte_num][proc_num][iteration_num] = {}
                        measurement = take_measurement(
                            RandCSV,
                            rows=row_num,
                            cols=col_num,
                            byte_size=byte_num,
                            data_types=data_type,
                            max_procs=proc_num
                        )
                        exec_times = [round(item[1] * 10 ** 3, 3) for item in measurement]
                        avg_exec = sum(exec_times) / len(exec_times)
                        avg_exec = round(avg_exec, 3)
                        var = sum([(exec_time - avg_exec) ** 2 for exec_time in exec_times]) / (len(exec_times) - 1)
                        std_dev = math.sqrt(var)
                        std_dev = round(std_dev, 3)
                        var = round(var, 3)

                        results[str(data_type)][byte_num][proc_num][iteration_num]['exec_times'] = \
                            exec_times
                        results[str(data_type)][byte_num][proc_num][iteration_num]['avg_exec'] = \
                            avg_exec
                        results[str(data_type)][byte_num][proc_num][iteration_num]['var'] = \
                            var
                        results[str(data_type)][byte_num][proc_num][iteration_num]['std_dev'] = \
                            std_dev

                experiment = [
                    (key, val['avg_exec']) for key, val in results[str(data_type)][byte_num][proc_num].items()
                ]
                iterations, execution_time = zip(*experiment)
                m, b = least_squares(iterations, execution_time)
                m = round(m, 6)
                b = round(b, 6)
                results[str(data_type)][byte_num][proc_num]['slope'] = m
                results[str(data_type)][byte_num][proc_num]['y_int'] = b
                results[str(data_type)][byte_num][proc_num]['int'] = \
                    (0.5 * m * max(iterations) ** 2) - (0.5 * m * min(iterations) ** 2)
                ax[0][0].plot(
                    iterations[:3], execution_time[:3], label=f'-d {" ".join(data_type)} -b {byte_num} -p {proc_num}')
                ax[0][1].plot(
                    iterations[:3], execution_time[:3], label=f'-d {" ".join(data_type)} -b {byte_num} -p {proc_num}')
                x_values = np.linspace(min(iterations), max(iterations), total_tests)
                y_values = m * x_values + b
                ax[1][0].plot(
                    x_values[:3], y_values[:3], label=f'-d {" ".join(data_type)} -b {byte_num} -p {proc_num}')
                ax[1][1].plot(
                    x_values[:3], y_values[:3], label=f'-d {" ".join(data_type)} -b {byte_num} -p {proc_num}')

    lines = []
    for data_type_key, data_type_val in results.items():
        for byte_num_key, byte_num_val in data_type_val.items():
            for proc_num_key, proc_num_val in byte_num_val.items():
                lines.append((proc_num_val['slope'], proc_num_val['y_int'], proc_num_key, proc_num_val['int']))

    intersection_points = []
    line_pairs = combinations(lines, 2)
    for line_pair in list(line_pairs):
        intersection_points.append(find_intersections_point(line_pair))

    intersection_points = sorted(intersection_points, key=lambda x: x[0])

    step_function = []
    for intersection_point in intersection_points:
        x_value = intersection_point[0] - 1.0
        line_f = lines[0]
        for line in lines:
            y_n = line[0] * x_value + line[1]
            y_f = line_f[0] * x_value + line_f[1]
            if y_n < y_f:
                line_f = line
        step_function.append(line_f[2])

    ax[0][0].set(
        xlabel='No. Iterations',
        ylabel='Execution Time ($s \cdot 10^{-3}$)',
        title='Affect of thread pooling on RandCSV instantiation time'
    )
    ax[1][0].set(
        xlabel='No. Iterations',
        ylabel='Execution Time ($s \cdot 10^{-3}$)',
        title='Lease Squares Approximation.'
    )
    ax[0][0].grid()
    ax[1][0].grid()
    ax[0][0].legend(title="Arguments", bbox_to_anchor=(1, 1), loc='upper left')
    ax[1][0].legend(title="Arguments", bbox_to_anchor=(1, 1), loc='upper left')

    ax[0][1].set(
        xlabel='No. Iterations',
        ylabel='Execution Time ($s \cdot 10^{-3}$)',
        title='Affect of thread pooling on RandCSV instantiation time'
    )
    ax[1][1].set(
        xlabel='No. Iterations',
        ylabel='Execution Time ($s \cdot 10^{-3}$)',
        title='Lease Squares Approximation.'
    )
    ax[0][1].grid()
    ax[1][1].grid()
    ax[0][1].legend(title="Arguments", bbox_to_anchor=(1, 1), loc='upper left')
    ax[1][1].legend(title="Arguments", bbox_to_anchor=(1, 1), loc='upper left')
    fig.tight_layout()
    plt.savefig('results.png')
    plt.show()

    return zip(intersection_points, step_function), lines


def find_intersections_point(lp):
    line_0 = lp[0]
    line_1 = lp[1]

    m_0 = line_0[0]
    m_1 = line_1[0]

    b_0 = line_0[1]
    b_1 = line_1[1]

    try:
        x = (b_1 - b_0) / (m_0 - m_1)
    except ZeroDivisionError:
        x = 0

    y = m_0 * x + b_0

    return x, y


def step_function_generator(thread_break_points):
    def step_function(num_of_iterations):
        thread_count = 1
        for thread_break_point in thread_break_points:
            if num_of_iterations > thread_break_point[0][0]:
                thread_count = thread_break_point[1]

        return thread_count

    return step_function


if __name__ == '__main__':
    ROW_NUMS = [10, 100]
    COL_NUMS = [10, 20]
    BYTE_NUMS = [8]
    PROC_NUMS = [i + 1 for i in range(cpu_count())]
    print(PROC_NUMS)
    DATA_TYPES = [['integer']]
    sf, exp_lines = run_experiment(
        row_nums=ROW_NUMS,
        col_nums=COL_NUMS,
        byte_nums=BYTE_NUMS,
        proc_nums=PROC_NUMS,
        data_types=DATA_TYPES,
    )

    sf_list = list(sf)
    print(sf_list)
    print(exp_lines)
    stepper = step_function_generator(sf_list)

    print(stepper(100))
    print(stepper(1000))
    print(stepper(10000))
    print(stepper(100000))

    fig, ax = plt.subplots(figsize=(20, 10))
    num_of_iterations = [item[0] * item[1] for item in product(ROW_NUMS, COL_NUMS)]
    iteration_range = np.arange(0, max(num_of_iterations), 100)
    optimal_thread = [stepper(item) for item in iteration_range]
    ax.set_yticks(PROC_NUMS)
    ax.set_ylabel("Optimal no. threads in pool")
    ax.set_xlabel("No. iterations")
    plt.step(iteration_range, optimal_thread, label='optimal threads')
    ax.set_title("Optimal Threads for Given Iteration.")
    plt.savefig('stepper.png')
    plt.show()

    max_iterations = max(ROW_NUMS) * max(COL_NUMS)
    avg_execution_time = [item[3] / max_iterations for item in exp_lines]
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.bar(PROC_NUMS, avg_execution_time)
    ax.set_xticks(PROC_NUMS)
    ax.set_xlabel("No. Threads in pool")
    ax.set_ylabel("Avg. execution time (ms.)")
    ax.set_title("Avg. Execution Time (ms.) by No. Threads in Pool.")
    plt.savefig('comparison.png')
    plt.show()
