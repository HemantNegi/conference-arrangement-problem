__author__ = 'hemant'

import sys
import csv

# set no of sessions here
num_sessions = 3


def main(argv):
    """
    program start
    receives command line arguments as array
    :param argv:  Command line arguments
    """
    try:
        # Receive total conference time from command line
        N = argv[0]
    except IndexError:
        print 'No arguments supplied!!'
        exit()

    try:
        # Typecast to int
        N = int(N)
    except ValueError:
        print 'Only integers are expected!!'
        exit()

    print "N =", N

    # loads csv data from a sample.csv file in the format of a list
    # eg: [['hemant', '1', '200'], ['amit', '1', '300']]
    presenters = load_data('sample.csv')

    # validates the list (to improve performance)
    # remove those presenters whose time is > N/2 and check if they are less than num_sessions
    presenters = validate_data(presenters, N)

    print '\n\npresenters\n', presenters

    # if presenters are < num_sessions exit
    if presenters is None:
        print "Not enough presenters"
        exit()

    # Finding the most valuable subsets of presenters whose sum of duration is not more than N/2
    presenters_list = subset_sum(presenters, N)

    # select the least costly group of presenters
    selected_presenters = select_less_expensive(presenters_list)
    print '\n\nselected presenters list'
    print selected_presenters

    print "\n\nDistribute in sessions"
    # Divide the presenters in sessions
    sol = split_chunks(selected_presenters, num_sessions)

    for i, s in enumerate(sol):
        print 'session %d' % (i + 1), s


def load_data(file_name):
    """
     Read data from the sample csv and returns a list
    :param file_name: (string) the csv file path
    :return: the csv in form of list
    >> load_data('sample.csv')
    [['rohit', '2', '100'], ['rajeev', '3', '50'], ['sanjeev', '4', '200'], ['saksham', '5', '300']]
    """
    with open(file_name, 'rb') as sample:
        data = csv.reader(sample, delimiter=',')
        return list(data)


def validate_data(presenters, N):
    """
    remove those presenters whose time is > N/2 and check if they are less than num_sessions
    :param presenters: list of presenters
    :param N: The maximum weight
    :return: List / None
    """
    presenters = [presenters[i] for i in range(len(presenters)) if int(presenters[i][1]) <= N / 2]

    if len(presenters) < num_sessions:
        return None
    return presenters


def subset_sum(press, target, partial=[]):
    """
    This method is slightly modified version of subset sum problem
    calculates the all possible subset of press which has maximum no of items
    and which should not exceed the given target weight
    >> press = [['rohit', '2', '100'], ['rajeev', '3', '50'], ['sanjeev', '4', '200'], ['saksham', '5', '300']]
    >> target = 6
    >> subset_sum(press, target)
    [[['rohit', '2', '100'], ['rajeev', '3', '50']],
     [['rohit', '2', '100'], ['sanjeev', '4', '200']],
     [['rohit', '2', '100'], ['saksham', '5', '300']],
     [['rajeev', '3', '50'], ['sanjeev', '4', '200']],
     [['rajeev', '3', '50'], ['saksham', '5', '300']]]

    :param press: The list of presenters on which the addition is pending
    :param target: Target weight which the sum should not exceed
    :param partial: The subset of presenters which are already added
    :return: The list of most valuable presenters
    """

    # list to hold the presenters subset
    lst = []

    # calculate the sum of duration from partial
    # can be accessed like ['rohit', '2', '100'][1]
    s = sum(int(c[1]) for c in partial)

    # if the sum is less than target then add partial to lst
    if s < target:
        lst.append(partial)

    # check if the partial sum is equals to target
    # The perfect match and return from here
    elif s == target:
        lst.append(partial)
        return lst

    # if sum exceeds the target then return None
    elif s > target:
        return None

    # iterate over each item in press and calculate the subset sum of each subset
    for i in range(len(press)):
        n = press[i]
        remaining = press[i + 1:]
        ss = subset_sum(remaining, target, partial + [n])

        # if subset_sum is None return the prepared list `lst`.
        # else check if subset ss contains more no of items then lst.
        # this means there is subset `ss` available which can have more
        # items(presenters) than the current subset.
        # in this case empty the current subset list `lst` and update it
        # with new subset list
        if ss:
            if len(lst[0]) <= len(ss[0]):       # if ss no of speakers are more than current number of speakers
                if len(lst[0]) < len(ss[0]):    # if current lst is less
                    lst = []                    # then empty it
                if ss[0] not in lst:            # if this set of presenters is already not there
                    lst = lst + ss              # add ss set to current list
    return lst


def select_less_expensive(presenters_list):
    """
    Selects the first subset in given list which has minimum cost as sum
    >> presenters_list = [[['hemant', '1', '200'], ['amit', '1', '300'], ['abc', '2', '50'], ['xyz', '1', '100']]
                          [['hemant', '1', '200'], ['amit', '1', '300'], ['xyz', '1', '100'], ['Neha', '2', '30']]]
    >> select_less_expensive(presenters_list)
       [['hemant', '1', '200'], ['amit', '1', '300'], ['xyz', '1', '100'], ['Neha', '2', '30']]

    :param presenters_list: the list of selected subsets (presenters)
    :return: a single subset having minimum cost
    """
    print '\n\nPossible combinaitons of max no of presenters'

    # initialize with some max value
    minamount = sys.maxint
    selected_presenters = []

    # iterate over presenters_list and find the subset having least subset
    for presenters in presenters_list:
        s = sum(int(presentor[2]) for presentor in presenters)
        print 'sum :', s, presenters
        if minamount > s:
            minamount = s
            selected_presenters = presenters
    return selected_presenters


def split_chunks(l, n):
    """
    Splits list l into n chunks with approximately equals sum of values
    using partition problem algorithm
    :param l: The list of
    :param n: no of chunks to prepare
    :return: list of prepared chunks
    """

    # init an empty array of length n
    result = [[] for i in range(n)]

    # init a dictionary having n keys
    # >> sums = {i: 0 for i in range(3)}
    # >>> sums
    # {0: 0, 1: 0, 2: 0}

    sums = {i: 0 for i in range(n)}
    c = 0

    # iterate over each item in list l
    # then calculate the suitable position `i` for the number
    # and keep adding to the sums dictionary
    for e in l:
        for i in sums:
            if c == sums[i]:
                result[i].append(e)
                break
        sums[i] += int(e[1])

        # update c with the minimum value in sums dictionary
        c = min(sums.values())

    return result


# program init
if __name__ == "__main__":
    main(sys.argv[1:])

