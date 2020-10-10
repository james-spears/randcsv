import math
from datetime import datetime
from itertools import combinations

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
                ax[0][0].plot(
                    iterations, execution_time, label=f'-d {" ".join(data_type)} -b {byte_num} -p {proc_num}')
                ax[0][1].plot(
                    iterations[:9], execution_time[:9], label=f'-d {" ".join(data_type)} -b {byte_num} -p {proc_num}')
                x_values = np.linspace(min(iterations), max(iterations), 100)
                y_values = m * x_values + b
                ax[1][0].plot(
                    x_values, y_values, label=f'-d {" ".join(data_type)} -b {byte_num} -p {proc_num}')
                ax[1][1].plot(
                    x_values[:10], y_values[:10], label=f'-d {" ".join(data_type)} -b {byte_num} -p {proc_num}')

    lines = []
    for data_type_key, data_type_val in results.items():
        for byte_num_key, byte_num_val in data_type_val.items():
            for proc_num_key, proc_num_val in byte_num_val.items():
                lines.append((proc_num_val['slope'], proc_num_val['y_int'], proc_num_key))

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
    ax[0][0].grid()
    ax[1][0].grid()
    ax[0][0].legend(title="Arguments")
    ax[1][0].legend(title="Arguments")
    ax[0][1].grid()
    ax[1][1].grid()
    ax[0][1].legend(title="Arguments")
    ax[1][1].legend(title="Arguments")
    fig.tight_layout()
    plt.savefig('results.png')
    plt.show()

    return zip(intersection_points, step_function)


def find_intersections_point(lp):
    line_0 = lp[0]
    line_1 = lp[1]

    m_0 = line_0[0]
    m_1 = line_1[0]

    b_0 = line_0[1]
    b_1 = line_1[1]

    x = (b_1 - b_0) / (m_0 - m_1)
    y = m_0 * x + b_0

    return x, y


if __name__ == '__main__':
    sf = run_experiment(
        row_nums=[1, 10, 100],
        col_nums=[10, 20, 30],
        byte_nums=[8],
        proc_nums=[1, 2, 4, 8, 16],
        data_types=[['integer']],
    )

    print(list(sf))
