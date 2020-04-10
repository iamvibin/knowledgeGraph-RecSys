import argparse
import numpy as np
if __name__ == '__main__':
    np.random.seed(555)

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', type=str, default='music', help='which dataset to preprocess')
    args = parser.parse_args()
    DATASET = args.d
    writer = open('../data/' + DATASET + '/blocking_obs.txt', 'w', encoding='utf-8')

    file = '../data/' + DATASET + '/' + 'ratings_final.txt'
    useritem = {}
    itemuser = {}
    m = 0
    for line in open(file, encoding='utf-8').readlines()[1:]:
        array = line.strip().split('\t')
        user = int(array[0])
        item = int(array[1])
        if m <= user:
            m = user
        if user not in useritem:
            useritem[user] = set()
            useritem[user].add(item)
        else:
            item_set = useritem[user]
            if item not in item_set:
                useritem[user].add(item)

        if item not in itemuser:
            itemuser[item] = set()
            itemuser[item].add(user)
        else:
            user_set = itemuser[item]
            if user not in user_set:
                itemuser[item].add(user)

        writer.write('%d\t%d\n' % (user, item))

    file2 = '../data/' + DATASET + '/' + 'kg_final.txt'
    item_set = set()
    for line in open(file, encoding='utf-8').readlines()[1:]:
        array = line.strip().split('\t')
        item1 = int(array[0])
        item2 = int(array[2])
        user_set1 = set()
        user_set2 = set()

        if item1 not in itemuser:
            item_set.add(item1)
            if item2 not in itemuser:
                item_set.add(item2)
                continue
        
        if item1 in itemuser:
            user_set1 = itemuser[item1]
        if item2 in itemuser:
            user_set2 = itemuser[item2]

        item2newUsers = user_set1 - user_set2
        item1newUsers = user_set2 - user_set1

        for user in item2newUsers:
            writer.write('%d\t%d\n' % (user, item2))
            if item2 in itemuser:
                itemuser[item2].add(user)
            else:
                itemuser[item2]=set()
                itemuser[item2].add(user)


        for user in item1newUsers:
            writer.write('%d\t%d\n' % (user, item1))
            if item1 in itemuser:
                itemuser[item1].add(user)
            else:
                itemuser[item1]=set()
                itemuser[item1].add(user)


    writer.close()
    print(len(item_set))


