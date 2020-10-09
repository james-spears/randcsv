import math
from datetime import datetime

import matplotlib.pyplot as plt

from randcsv import RandCSV


def measure_performance(test_class, iterations=20, **kwargs):
    """

    :param test_class:
    :param iterations:
    :param kwargs:
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


def main():
    row_nums = [1, 10, 100, 1000]
    col_nums = [10, 20, 30, 40]
    byte_nums = [32]
    proc_nums = [1, 4, 8, 12, 16]
    data_types = [['integer']]

    fig, ax = plt.subplots()
    measurements = {}
    for data_type in data_types:
        measurements[str(data_type)] = {}
        for byte_num in byte_nums:
            measurements[str(data_type)][byte_num] = {}
            for proc_num in proc_nums:
                measurements[str(data_type)][byte_num][proc_num] = {}
                for row_num in row_nums:
                    for col_num in col_nums:
                        iteration_num = row_num * col_num
                        measurements[str(data_type)][byte_num][proc_num][iteration_num] = {}
                        performance = measure_performance(
                            RandCSV,
                            rows=row_num,
                            cols=col_num,
                            byte_size=byte_num,
                            data_types=data_type,
                            max_procs=proc_num
                        )
                        exec_times = [round(item[1] * 10 ** 3, 3) for item in performance]
                        avg_exec = sum(exec_times) / len(exec_times)
                        avg_exec = round(avg_exec, 3)
                        var = sum([(exec_time - avg_exec) ** 2 for exec_time in exec_times]) / (len(exec_times) - 1)
                        std_dev = math.sqrt(var)
                        std_dev = round(std_dev, 3)
                        var = round(var, 3)

                        measurements[str(data_type)][byte_num][proc_num][iteration_num]['exec_times'] = \
                            exec_times
                        measurements[str(data_type)][byte_num][proc_num][iteration_num]['avg_exec'] = \
                            avg_exec
                        measurements[str(data_type)][byte_num][proc_num][iteration_num]['var'] = \
                            var
                        measurements[str(data_type)][byte_num][proc_num][iteration_num]['std_dev'] = \
                            std_dev

                experiment = [
                    (key, val['avg_exec']) for key, val in measurements[str(data_type)][byte_num][proc_num].items()
                ]
                iterations, execution_time = zip(*experiment)
                ax.plot(iterations, execution_time, label=f'-d {" ".join(data_type)} -b {byte_num} -p {proc_num}')

    ax.set(
        xlabel='No. Iterations',
        ylabel='Execution Time ($s \cdot 10^{-3}$)',
        title='Affect of thread pooling on execution time'
    )
    ax.grid()
    ax.legend(title="Arguments")
    fig.tight_layout()
    fig.savefig("_thread_pooling.png")
    plt.show()


if __name__ == '__main__':
    main()
