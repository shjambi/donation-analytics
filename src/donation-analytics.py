import csv
import time
import math
import sys
import bisect
import re

# Initialize variables
all_donors = {'years':set()}  # A dictionary of year set and donor set of each year
recipient = {} # A dictionary of key/value of distinct contributions 
recipient_set = set() # A set of distinct contribution keys


def valid_name(strName):
	if (re.compile("[a-zA-Z ,.'`-]+$").match(strName)) and len(strName)<=200:
		return True
	else:
		return False


def valid_date(strDate):
	# Transaction Date (MMDDYYYY)
	correctDate = True
	try:
		time.strptime(strDate, '%m%d%Y')
	except ValueError:
		correctDate = False
	else:
		if not 1900 <= int(strDate[4:]) <= 2020: correctDate = False
	return correctDate


def get_percentile(percentile_file_name):
	# Get percentile value
	percentile_file = open(percentile_file_name, 'r') 
	return percentile_file.read()


def add_contribution(year, cmte_id, zip_code, amount, percentile, output_file):
	# Define a unique contribution key of calendar year, recipient, and zipcode   
	key = year+cmte_id+zip_code
	# Check if this unique key has been already found for a repeat donor
	# Look up for the key in the recipient set instead of recipient.keys list.
	if key in recipient_set:
		# If found, calculate
		# the running percentile of contributions from repeat donors, 
		# total amount of donations streaming in from repeat donors, and
		# total number of transactions from repeat donors, 
		# so far for that calendar year, recipient and zipcode.
		amount_list = recipient[key]
		# Add the new amount to the total amount in the last index
		amount_list[-1] += amount
		# Inser the new amount in the sorted list of amounts
		bisect.insort(amount_list, amount)
		# Get the total amount value from the last index
		total_amount = amount_list[-1]
		# Get the total number of received amounts
		count = len(amount_list)-1
		# Calculate the ordinal rank of percentile for an ordered amount list
		ordinal_rank = int(math.ceil(percentile * count))
		# Take the value from the ordered amount list that corresponds to that rank
		percentile_value = int(round(amount_list[ordinal_rank-1]))
		# Update current recipient value
		recipient[key] = amount_list

	else:
		# If not found,
		# add a key of calendar year, recipient, and zipcode,   
		# with a list value of a new amount, so that
		# this contribution is the only one that qualifies.
		percentile_value = amount
		total_amount = amount
		count = 1
		# Add a new amount, then the same amount as total amount 
		recipient[key] = [amount, total_amount]
		# Use an extra Set for unique contribution keys of calendar year, recipient, and zipcode,
		# for the purpose of searching, because lookup time is constant (O(1)) using Set.
		recipient_set.add(key)

	# Write contribution to the output file
	output_file.write("{}|{}|{}|{}|{}|{}\n".format(cmte_id, zip_code, year, percentile_value, total_amount, count))


def main(input_file_name, percentile_file_name, output_file_name):

	start_time = time.time()

	# Read percentile from file
	percentile = get_percentile(percentile_file_name)
	# Percentile should be in range (1-100) 
	if not 1 <= int(percentile) <= 100:
		raise Exception('Percentile value is out of range.')
	percentile = float(percentile)/100

	# Open an input file of campaign contributions for reading
	with open(input_file_name) as input_file:
		readCSV = csv.reader(input_file, delimiter='|', dialect=csv.excel_tab)

		# Open a new text file for writing output
		output_file = open(output_file_name, 'w') 
		valid_row = 0

		# Read each row of campaign contributions
		for index, row in enumerate(readCSV):

			if not row[15]: # OTHER_ID should be empty for individual contributions
	 			# Read current contribution data 
				cmte_id = row[0] # CMTE_ID
				name = row[7] # NAME should be invalid name (e.g., empty, malformed)
				zip_code = row[10] # ZIP_CODE should be invalid zip code (i.e., empty, fewer than five digits)
				transaction_dt = row[13] # TRANSACTION_DT should be invalid date (e.g., empty, malformed)
				transaction_amt = row[14]  # TRANSACTION_AMT (should be positive amount)

				# Validate data of required fields 
				if cmte_id and valid_name(name) and len(zip_code)>=5 and valid_date(transaction_dt) and transaction_amt.isdigit():
					# Set variables for current contribution data
					year = transaction_dt[4:]
					zip_code = zip_code[:5]
					amount = int(transaction_amt)
					# Identify a unique donor by NAME and ZIP_CODE 
					donor = name + '. ' + zip_code
					found_repeat_donor = False

					# Keep track of donor with donation year
					if year not in all_donors['years']:
						all_donors['years'].add(year)
						all_donors[year] = set()
					if donor not in all_donors[year]:
						all_donors[year].add(donor)

					# Check if donor had previously contributed to any recipient in any prior calendar year
					for y in all_donors['years']:
						if int(y)<int(year) and donor in all_donors[y]: 
							found_repeat_donor = True
							break
					if found_repeat_donor:
						add_contribution(year, cmte_id, zip_code, amount, percentile, output_file)

					valid_row += 1
						
			sys.stdout.write("Number of Input Rows = %d\r" % index)

		output_file.close()
	input_file.close()
	end_time = time.time()

	print("Number of Input Rows = %d" % (index+1))
	print("Number of Valid Rows = %d" % (valid_row))
	with open('output/repeat_donors.txt') as f: num_lines = len(list(f))
	print("Number of Output Rows = %d" % (num_lines))
	print("Execution Time = %s seconds" % (end_time - start_time))


if __name__ == '__main__':
	if len(sys.argv) < 4:
		print("Wrong number of arguments.")
		exit()
	input_file = sys.argv[1]
	percentile_file = sys.argv[2]
	output_file = sys.argv[3]
	main(input_file, percentile_file, output_file)


