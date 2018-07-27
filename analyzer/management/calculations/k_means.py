import os
import random

import numpy as np
from django.core.management.base import BaseCommand
from chatanalyzer import settings

TOLERANCE = 1
MAX_ITERATION = 100


class Command(BaseCommand):
    help = 'partitions the data in database into specified number of bins'

    def add_arguments(self, parser):
        parser.add_argument('partition_number', nargs='+', type=int)
        parser.add_argument('get_file_name', nargs='+', type=str)
        parser.add_argument('save_file_name', nargs='+', type=str)

    def handle(self, *args, **options):
        p_no = options['partition_number'][0]
        get_file_name = options['get_file_name'][0]
        save_file_name = options['save_file_name'][0]
        train_set = k_means(p_no,get_file_name,save_file_name)
        for e in train_set.items():
            print('Key:', e[0], "Total:", len(e[1]))


def k_means(p_no,get_file_name, save_file_name):
    message_list = get_from_file(get_file_name)
    random.shuffle(message_list)
    for i in range(len(message_list)):
        message_list[i] = float(message_list[i])
    message_list = message_list[:40000]
    # # dataset = []
    # # for message in message_list[:10000]:
    # #     dataset.append((message, len(message)))
    partitioned_dict = k_cluster(p_no, message_list, MAX_ITERATION)
    np.save('time_train_data.npy', partitioned_dict)
    read_dictionary = np.load('analyzer/trained_data/{}.npy'.format(save_file_name)).item()
    sorted_dict_keys =  sorted(read_dictionary.iterkeys())
    train_dict = {
        'Very Short' : read_dictionary[sorted_dict_keys[0]],
        'Short' : read_dictionary[sorted_dict_keys[1]],
        'Medium': read_dictionary[sorted_dict_keys[2]],
        'Long':read_dictionary[sorted_dict_keys[3]],
        'Very Long': read_dictionary[sorted_dict_keys[4]]
    }

    np.save('time_train_data.npy', train_dict)
    return train_dict


def get_from_file(filename):
    filename = filename
    file_path = os.path.join(settings.BASE_DIR, filename)

    with open(file_path) as f:
        lines = f.readlines()
    return lines


def getPartition(partition_keys, dataset):
    partitioned_dict = {}

    for key in partition_keys:
        partitioned_dict[key] = []
    # print(partition_keys)
    for data in dataset:
        closest_key = min(partition_keys, key=lambda x: abs(x - data))
        # finds the key that has the least distance to given data
        partitioned_dict[closest_key] = partitioned_dict[closest_key] + [data]

    return partitioned_dict


def get_avg(data_list):
    sum = 0
    for data in data_list:
        sum = sum + data
    return sum / len(data_list)


def check_if_done(old_keys, new_keys):
    for i in range(0, len(old_keys)):
        if abs(old_keys[i] - new_keys[i]) > 0:
            return 0
    return 1


def k_cluster(partition_number, dataset, iter_no):
    partition_keys = list()
    for i in range(0, partition_number):
        partition_keys.append(dataset[i])

    for i in range(0, iter_no):

        partitioned_dict = getPartition(partition_keys, dataset)

        new_partition_key_list = []
        for key in partition_keys:
            average = get_avg(partitioned_dict[key])
            new_partition_key_list.append(average)

        if check_if_done(partition_keys, new_partition_key_list):
            print("New partition", new_partition_key_list)
            print("Number of iterations: ", i)
            return partitioned_dict
        else:
            partition_keys = new_partition_key_list
    return "Iteration limit reached"
