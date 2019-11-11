import numpy as np
import timeit
import copy
import pandas as pd
import matplotlib.pyplot as plt
import math


def merge(a, first_index, middle_index, last_index):
    """Merge function for use in merge sort."""
    n1 = middle_index - first_index + 1
    n2 = last_index - middle_index

    left = [0] * n1
    right = [0] * n2

    for i in range(n1):
        left[i] = a[first_index + i - 1]

    for j in range(n2):
        right[j] = a[middle_index + j]

    left.append(float('inf'))
    right.append(float('inf'))

    i = 0
    j = 0

    for k in range(first_index - 1, last_index):
        if left[i] <= right[j]:
            a[k] = left[i]
            i += 1
        else:
            a[k] = right[j]
            j += 1

    return a


def merge_sort(a, first_index=0, last_index=None):
    """Sorts a list using the 'merge-sort' algorithm."""
    if last_index is None:
        last_index = len(a) - 1
    if first_index < last_index:
        middle_index = (first_index + last_index) // 2
        merge_sort(a, first_index, middle_index)
        merge_sort(a, middle_index + 1, last_index)
        return merge(a, first_index, middle_index, last_index)


def parent(i):
    """Returns the parent to a node in a heap."""
    return math.floor((i-1) / 2)


def left_child(i):
    """Returns the left child of a node in a heap."""
    return 2 * i + 1


def right_child(i):
    """Returns the right child of a node in a heap."""
    return 2 * i + 2


def max_heapify(a, i, heap_size):
    """Max-heapifies subtree of 'a' rooted at 'i'."""
    l = left_child(i)
    r = right_child(i)
    if l <= heap_size - 1 and a[l] > a[i]:
        largest = l
    else:
        largest = i
    if r <= heap_size - 1 and a[r] > a[largest]:
        largest = r
    if largest != i:
        a[i], a[largest] = a[largest], a[i]
        max_heapify(a, largest, heap_size)


def build_max_heap(a):
    """Builds a max heap"""
    heap_size = len(a)
    for i in range(math.floor(heap_size / 2), -1, -1):
        max_heapify(a, i, heap_size)


def heap_sort(a):
    """Sorts a list using the 'heap-sort' algorithm."""

    build_max_heap(a)
    heap_size = len(a)
    for i in range(len(a) - 1, 0, -1):
        a[0], a[i] = a[i], a[0]
        heap_size -= 1
        max_heapify(a, 0, heap_size)


def partition(array, low, high):
    """DEFINE PARTITION FOR QUICKSORT"""
    i = (low - 1)
    pivot = array[high]

    for j in range(low, high):
        if array[j] <= pivot:
            i = i + 1
            array[i], array[j] = array[j], array[i]
    array[i + 1], array[high] = array[high], array[i + 1]
    return i + 1


def quick_sort(array, low=0, high=None):
    """Sorts a list using the 'quick-sort' algorithm."""
    if high is None:
        high = len(array) - 1
    if low < high:
        part = partition(array, low, high)
        quick_sort(array, low, part - 1)
        quick_sort(array, part + 1, high)


np.random.seed(12235)
results = pd.DataFrame(
    columns=['Input ordering', 'Input size', 'Run number', 'Sorting algorithm',
             'Time'])

for input_ordering in ['sorted', 'reverse', 'random']:
    for input_size in range(1, 7):
        test_data = np.random.random((10 ** input_size,))
        if input_ordering == 'sorted':
            test_data = sorted(test_data)
        elif input_ordering == 'reverse':
            test_data = list(reversed(sorted(test_data)))

        clock = timeit.Timer(stmt='sort_func(copy(data))',
                             globals={'sort_func': merge_sort,
                                      'data': test_data,
                                      'copy': copy.copy})

        n_ar, t_ar = clock.autorange()
        t = clock.repeat(repeat=7, number=n_ar)
        print(
            f"Merge sort minimum time on {input_ordering} data of size 10^{input_size}:",
            min(t))

        for run_number in range(7):
            results = results.append({'Input ordering': input_ordering,
                                      'Input size': 10 ** input_size,
                                      'Run number': run_number + 1,
                                      'Sorting algorithm': 'merge_sort',
                                      'Time': t[run_number]},
                                     ignore_index=True)

        clock = timeit.Timer(stmt='sort_func(copy(data))',
                             globals={'sort_func': heap_sort,
                                      'data': test_data,
                                      'copy': copy.copy})

        n_ar, t_ar = clock.autorange()
        t = clock.repeat(repeat=7, number=n_ar)
        print(
            f"Heap sort minimum time on {input_ordering} data of size 10^{input_size}:",
            min(t))

        for run_number in range(7):
            results = results.append({'Input ordering': input_ordering,
                                      'Input size': 10 ** input_size,
                                      'Run number': run_number + 1,
                                      'Sorting algorithm': 'heap_sort',
                                      'Time': t[run_number]},
                                     ignore_index=True)

        if not ((
                        input_ordering == 'sorted' or input_ordering == 'reverse') and input_size > 2):
            clock = timeit.Timer(stmt='sort_func(copy(data))',
                                 globals={'sort_func': quick_sort,
                                          'data': test_data,
                                          'copy': copy.copy})

            n_ar, t_ar = clock.autorange()
            t = clock.repeat(repeat=7, number=n_ar)
            print(
                f"Quick sort minimum time on {input_ordering} data of size 10^{input_size}:",
                min(t))
        print("--------------------")

        for run_number in range(7):
            results = results.append({'Input ordering': input_ordering,
                                      'Input size': 10 ** input_size,
                                      'Run number': run_number + 1,
                                      'Sorting algorithm': 'quick_sort',
                                      'Time': t[run_number]},
                                     ignore_index=True)

print(results)

## Plotting results
for input_ord in ['sorted', 'reverse', 'random']:
    plt.figure()
    plt.title(input_ord)

    is_input_ord = results['Input ordering'] == input_ord
    results_input_ord = results[is_input_ord]

    is_merge_sort = results_input_ord['Sorting algorithm'] == 'merge_sort'
    results_merge_sort = results_input_ord[is_merge_sort]
    merge_sort_means = []
    for input_size in [1, 2, 3, 4, 5, 6]:
        is_input_size = results_merge_sort['Input size'] == 10 ** input_size
        results_input_size = results_merge_sort[is_input_size]
        merge_sort_means.append(np.mean(results_input_size['Time']))
    plt.plot([1, 2, 3, 4, 5, 6], merge_sort_means)

    is_heap_sort = results_input_ord['Sorting algorithm'] == 'heap_sort'
    results_heap_sort = results_input_ord[is_heap_sort]
    heap_sort_means = []
    for input_size in [1, 2, 3, 4, 5, 6]:
        is_input_size = results_heap_sort['Input size'] == 10 ** input_size
        results_input_size = results_heap_sort[is_input_size]
        heap_sort_means.append(np.mean(results_input_size['Time']))
    plt.plot([1, 2, 3, 4, 5, 6], heap_sort_means)

    is_quick_sort = results_input_ord['Sorting algorithm'] == 'quick_sort'
    results_quick_sort = results_input_ord[is_quick_sort]
    quick_sort_means = []
    for input_size in [1, 2, 3, 4, 5, 6]:
        is_input_size = results_quick_sort['Input size'] == 10 ** input_size
        results_input_size = results_quick_sort[is_input_size]
        quick_sort_means.append(np.mean(results_input_size['Time']))
    plt.plot([1, 2, 3, 4, 5, 6], quick_sort_means)
    plt.legend(['Merge sort', 'Heap sort', 'Quicksort'])


