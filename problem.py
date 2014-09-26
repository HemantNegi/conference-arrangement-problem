__author__ = 'hemant'

import sys
import csv

num_sessions = 3			# set no of sessions here	


# program start
def main(argv):  

	try:
		N = argv[0]   		# Recieve total conference time from command line
	except IndexError:
		print 'No arguments supplied!!'
		exit()

	try:
		N = int(N)			   	# Typecast to int
	except ValueError:
		print 'Only integers are expected!!'
		exit()
	
	print "N =",N	
	
	# loads csv data in a list 
	presenters = load_data('sample.csv')
	
	# validates the list
	presenters = validate_data(presenters,N)
	
	if presenters is None:
		print "Not enough presenters"
		exit()
	
	presenters =  sort_presenters(presenters)
	print '\n\nSorted data'
	print presenters
	
	presenters_list = subset_sum(presenters,N)
	
	
	selected_presenters = select_less_expensive(presenters_list)
	print '\n\nselected presenters list'
	print selected_presenters
	
	print "\n\nDistribute in sessions"
	sol = split_chunks(selected_presenters,num_sessions)
		
	for i,s in enumerate(sol):
		print 'session %d' %(i+1), s	
	
	
# Read data from the sample csv and returns a list
def load_data(file_name):
	with open(file_name, 'rb') as sample:
		data = csv.reader(sample, delimiter=',')
		return list(data)

# remove those presenters whose time is > N/2 and check if theya are less than num_sessions
def validate_data(presenters, N):
	presenters = [presenters[i] for i in range(len(presenters)) if int(presenters[i][1]) <= N/2]

	if len(presenters) < num_sessions:
		return None
	return presenters

# sorting presenters in asc according to time.
def sort_presenters(presenters):
	presenters.sort(key=lambda x: x[1])    
	return presenters

# calculates all the possible combinations which contains max no of presenters.
def subset_sum(press, target, partial=[]):
	lst = [] 												  # presenters set list

	s = sum(int(c[1]) for c in partial)

	if s < target:
		lst.append(partial)
	
    # check if the partial sum is equals to target
	elif s == target:
		lst.append(partial) # The perfect match and best case
		return lst
	elif s > target:
		return None # if we reach the number why bother to continue

	for i in range(len(press)):
		n = press[i]
		remaining = press[i+1:]
		ss = subset_sum(remaining, target, partial + [n])
		if ss:													# if return is not None
			if len(lst[0]) <= len(ss[0]):						# if ss no of speakers are more than current number of speakers
				if len(lst[0]) < len(ss[0]):					# if current lst is less 
					lst = []									# then empty it
				#ss[0].sort(key=lambda x: x[0])  				# just precaution to avoid duplicates
				if ss[0] not in lst:							# if this set of presenters is already not there
					lst = lst + ss								# add ss set to current list
	return lst



def select_less_expensive(presenters_list):
	print '\n\nPossible combinaitons of max no of presenters'
	minamount = sys.maxint # initialize with some max value
	selected_presenters = []
	for presenters in presenters_list:
		s = sum(int(presentor[2]) for presentor in presenters)
		print 'sum :', s, presenters
		if minamount > s:
			minamount = s
			selected_presenters = presenters
	return selected_presenters

# Splits list l into n chunks with approximately equals sum of values
def split_chunks(l, n):
    result = [[] for i in range(n)]
    sums   = {i:0 for i in range(n)}
    c = 0
    for e in l:
        for i in sums:
            if c == sums[i]:
                result[i].append(e)
                break
        sums[i] += int(e[1])
        c = min(sums.values())    
    return result





if __name__ == "__main__":
    main(sys.argv[1:])

