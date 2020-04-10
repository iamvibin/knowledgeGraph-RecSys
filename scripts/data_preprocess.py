import argparse
import numpy as np

RATING_FILE_NAME = dict({'movie': 'ratings.dat',
                         'book': 'BX-Book-Ratings.csv',
                         'music': 'user_artists.dat',
                         'news': 'ratings.txt'})
SEP = dict({'movie': '::', 'book': ';', 'music': '\t', 'news': '\t'})
THRESHOLD = dict({'movie': 4, 'book': 0, 'music': 0, 'news': 0})

def read_item_index_to_entity_id_file():
    file = '../data/' + DATASET + '/item_index2entity_id.txt'
    print('reading item index to entity id file: ' + file + ' ...')
    i = 0
    for line in open(file, encoding='utf-8').readlines():
        item_index = line.strip().split('\t')[0]
        satori_id = line.strip().split('\t')[1]
        item_index_old2new[item_index] = i
        entity_id2index[satori_id] = i
        i += 1

def convert_rating_new():
    file = '../data/' + DATASET + '/' + RATING_FILE_NAME[DATASET]

    print('reading rating file ...')
    item_set = set(item_index_old2new.values())
    user_pos_ratings = dict()
    user_neg_ratings = dict()
    item_ratings = dict()


    for line in open(file, encoding='utf-8').readlines()[1:]:
        array = line.strip().split(SEP[DATASET])

        # remove prefix and suffix quotation marks for BX dataset
        if DATASET == 'book':
            array = list(map(lambda x: x[1:-1], array))

        item_index_old = array[1]
        if item_index_old not in item_index_old2new:  # the item is not in the final item set
            continue
        item_index = item_index_old2new[item_index_old]

        user_index_old = int(array[0])

        rating = float(array[2])

        if rating >= THRESHOLD[DATASET]:
            if user_index_old not in user_pos_ratings:
                user_pos_ratings[user_index_old] = set()
            user_pos_ratings[user_index_old].add(item_index)
            rating = float(rating / 5)

            item_ratings[item_index] = rating
        else:
            if user_index_old not in user_neg_ratings:
                user_neg_ratings[user_index_old] = set()
            user_neg_ratings[user_index_old].add(item_index)
            rating = float(rating / 5)

            item_ratings[item_index] = rating


    print('converting rating file ...')
    writer = open('../data/' + DATASET + '/ratings_final.txt', 'w', encoding='utf-8')
    user_cnt = 0
    user_index_old2new = dict()
    count = 1
    for user_index_old, pos_item_set in user_pos_ratings.items():
        if user_index_old not in user_index_old2new:
            user_index_old2new[user_index_old] = user_cnt
            user_cnt += 1
        user_index = user_index_old2new[user_index_old]

        for item in pos_item_set:
            rating = float(item_ratings[item])
            writer.write('%d\t%d\t%f\t\n' % (user_index, item, rating))
            count = count+1
        unwatched_set = item_set - pos_item_set
        if user_index_old in user_neg_ratings:
            unwatched_set -= user_neg_ratings[user_index_old]
        for item in np.random.choice(list(unwatched_set), size=len(pos_item_set), replace=False):
            rating = float(item_ratings[item])
            writer.write('%d\t%d\t%f\t\n' % (user_index, item, rating))
            count = count+1
    writer.close()
    print('number of lines in dataset: %d' % count)
    return count
    print('number of users: %d' % user_cnt)
    print('number of items: %d' % len(item_set))

def convert_rating():
    file = '../data/' + DATASET + '/' + RATING_FILE_NAME[DATASET]

    print('reading rating file ...')
    item_set = set(item_index_old2new.values())
    user_pos_ratings = dict()
    user_neg_ratings = dict()

    for line in open(file, encoding='utf-8').readlines()[1:]:
        array = line.strip().split(SEP[DATASET])

        # remove prefix and suffix quotation marks for BX dataset
        if DATASET == 'book':
            array = list(map(lambda x: x[1:-1], array))

        item_index_old = array[1]
        if item_index_old not in item_index_old2new:  # the item is not in the final item set
            continue
        item_index = item_index_old2new[item_index_old]

        user_index_old = int(array[0])

        rating = float(array[2])
        if rating >= THRESHOLD[DATASET]:
            if user_index_old not in user_pos_ratings:
                user_pos_ratings[user_index_old] = set()
            user_pos_ratings[user_index_old].add(item_index)
        else:
            if user_index_old not in user_neg_ratings:
                user_neg_ratings[user_index_old] = set()
            user_neg_ratings[user_index_old].add(item_index)

    print('converting rating file ...')
    writer = open('../data/' + DATASET + '/ratings_final.txt', 'w', encoding='utf-8')
    user_cnt = 0
    user_index_old2new = dict()
    line_count = 1
    for user_index_old, pos_item_set in user_pos_ratings.items():
        if user_index_old not in user_index_old2new:
            user_index_old2new[user_index_old] = user_cnt
            user_cnt += 1
        user_index = user_index_old2new[user_index_old]

        for item in pos_item_set:
            writer.write('%d\t%d\t1\n' % (user_index, item))
            line_count = line_count + 1
        unwatched_set = item_set - pos_item_set
        if user_index_old in user_neg_ratings:
            unwatched_set -= user_neg_ratings[user_index_old]
        for item in np.random.choice(list(unwatched_set), size=len(pos_item_set), replace=False):
            writer.write('%d\t%d\t0\n' % (user_index, item))
            line_count = line_count + 1
    writer.close()

    print('number of users: %d' % user_cnt)
    print('number of items: %d' % len(item_set))
    return line_count

def data_split(count):
    file = '../data/' + DATASET + '/' + 'ratings_final.txt'

    writer1 = open('../data/' + DATASET + '/ratings_obs.txt', 'w', encoding='utf-8')
    writer2 = open('../data/' + DATASET + '/ratings_target.txt', 'w', encoding='utf-8')
    writer3 = open('../data/' + DATASET + '/ratings_truth.txt', 'w', encoding='utf-8')
    useritem = dict()



    lines = []
    for line in open(file, encoding='utf-8').readlines()[1:]:
        lines.append(line)

    limit = int(0.8 * len(lines))
    c = 1
    c1 = 1
    randnums = np.random.randint(1, len(lines), len(lines))
    print(randnums)
    print(limit)
    print(range(len(lines)))
    for i in range(len(lines)):
        line = lines[randnums[i]]

        array = line.strip().split('\t')

        #item_index_old = array[1]
        #if item_index_old not in item_index_old2new:  # the item is not in the final item set
         #   c1 = c1+1
          #  continue
        #item_index = item_index_old2new[item_index_old]
        item_index = int(array[1])

        user_index_old = int(array[0])

        rating = float(array[2])

        if i < limit:
            if user_index_old not in useritem:
                useritem[user_index_old] = set()
                useritem[user_index_old].add(item_index)
                writer1.write('%d\t%d\t%f\n' % (user_index_old, item_index, rating))
            else:
                item_set = useritem[user_index_old]
                if item_index not in item_set:
                    useritem[user_index_old].add(item_index)
                    writer1.write('%d\t%d\t%f\n' % (user_index_old, item_index, rating))
        else:
            if user_index_old not in useritem:
                useritem[user_index_old] = set()
                useritem[user_index_old].add(item_index)
                writer2.write('%d\t%d\n' % (user_index_old, item_index))
                writer3.write('%d\t%d\t%f\n' % (user_index_old, item_index, rating))
            else:
                item_set = useritem[user_index_old]
                if item_index not in item_set:
                    useritem[user_index_old].add(item_index)
                    writer2.write('%d\t%d\n' % (user_index_old, item_index))
                    writer3.write('%d\t%d\t%f\n' % (user_index_old, item_index, rating))


        c = c + 1

    print("stats")
    print(c)
    print(c1)
    writer1.close()
    writer2.close()
    writer3.close()


if __name__ == '__main__':
    np.random.seed(555)

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', type=str, default='movie', help='which dataset to preprocess')
    args = parser.parse_args()
    DATASET = args.d

    entity_id2index = dict()
    relation_id2index = dict()
    item_index_old2new = dict()

    read_item_index_to_entity_id_file()
    count = convert_rating()
    data_split(count)

    print('done')
