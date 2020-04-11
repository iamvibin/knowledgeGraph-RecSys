import argparse
import numpy as np
import pdb
if __name__ == '__main__':
    np.random.seed(555)

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', type=str, default='music', help='which dataset to preprocess')
    args = parser.parse_args()
    DATASET = args.d
    targetwriter = open('../data/' + DATASET + '/ratingsNew_target.txt', 'w', encoding='utf-8')
    truthwriter = open('../data/' + DATASET + '/ratingsNew_truth.txt', 'w', encoding='utf-8')
    blockingwriter = open('../data/' + DATASET + '/ratings_block.txt', 'w', encoding='utf-8')

    file = '../data/' + DATASET + '/' + 'ratings_final.txt'


    useritem = {}
    itemuser = {}

    for line in open(file, encoding='utf-8').readlines()[1:]:
        array = line.strip().split('\t')
        user = int(array[0])
        item = int(array[1])


        if item not in itemuser:
            itemuser[item] = set()
            itemuser[item].add(user)
        else:
            itemuser[item].add(user)



    file2 = '../data/' + DATASET + '/' + 'kg_final.txt'
    item_set = set()
    count = 0
    for line in open(file2, encoding='utf-8').readlines()[1:]:
        array = line.strip().split('\t')
        item1 = int(array[0])
        item2 = int(array[2])
        user_set1 = set()
        user_set2 = set()

        #if item2 == 7854 or item1 == 7854:
         #   pdb.set_trace()

        if item1 in itemuser:
            user_set1 = itemuser[item1]
        else:
            itemuser[item1]=user_set1
        if item2 in itemuser:
            user_set2 = itemuser[item2]
        else:
            itemuser[item2]=user_set2

        user_set1.update(user_set2)

        itemuser[item1].update(user_set1)
        itemuser[item2].update(user_set1)



    obs_file = '../data/' + DATASET + '/' + 'ratings_obs.txt'
    obs_set = set()

    for line in open(obs_file, encoding='utf-8').readlines()[1:]:
        array = line.strip().split('\t')
        user = array[0]
        item = array[1]
        observation = user + '\t' + item
        obs_set.add(observation)

    for item in itemuser:
        userset = itemuser[item]
        for user in userset:
            test_string = '{}\t{}'.format(user, item)
            blockingwriter.write(test_string + '\n')
            if test_string in obs_set:
                continue
            targetwriter.write(test_string+'\n')
            truthwriter.write(test_string+'\t1.0\n')

    targetwriter.close()
    truthwriter.close()