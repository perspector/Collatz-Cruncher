from collatzConjecture import collatz
import datetime
import sys
from tqdm import tqdm
import traceback
import os
import fnmatch
from colorama import init, Fore
import math
import time

init(autoreset=True)

power = 1000000
cooldown = 10


def find(pattern, path):
	result = []
	for root, dirs, files in os.walk(path):
		for name in files:
			if fnmatch.fnmatch(name, pattern):
				result.append(name)
	if len(result) <= 10:
		result.sort()
	if len(result) > 10:
		result.sort(key=len)
	return result


# cwd = '/media/pythoncoder8888/ToshibaEXT/CollatzConjecture'
# data_filename = 'collatz_data_TEST.txt'
data_filename = find('collatz_*-*.txt', str(os.getcwd()+'/data/'))
log_filename = 'collatz_log.txt'

try:
	print(
		f"""
      {Fore.CYAN}_____     _ _       _          {Fore.BLUE}____                       _
     {Fore.CYAN}/ ___/___ | | | __ _| |_ ____  {Fore.BLUE}/ ___|_ __ _   _ _ __   ___| |__   ___ _ __
    {Fore.CYAN}| |   / _ \| | |/ _` | __|_  / {Fore.BLUE}| |   | '__| | | | '_ \ / __| '_ \ / _ \ '__|
    {Fore.CYAN}| |__| (_) | | | (_| | |_ / /  {Fore.BLUE}| |___| |  | |_| | | | | (__| | | |  __/ |
     {Fore.CYAN}\____\___/|_|_|\__,_|\__/___|  {Fore.BLUE}\____|_|   \__,_|_| |_|\___|_| |_|\___|_|
        """
	)
	data_file = open(os.getcwd() + '/data/' + data_filename[-1], 'r')
	file_data = data_file.readlines()
	numlines = len(file_data)
	file_data = file_data[-1]  # choose last line from file
	file_data = file_data.strip('][').split(', ')
	file_data = file_data[0]
	data_file.close()
	print(Fore.LIGHTGREEN_EX + 'Continuing where last left off, at ' + file_data)
	n = int(file_data) + 1
	print(f"""{Fore.LIGHTGREEN_EX}
File limit: {str(power)} numbers per file.
If your number exceeds the file limit, multiple files will be created.
This will limit memory usage and file size.
""")
	print(f"""
{Fore.LIGHTGREEN_EX}{numlines} inputs have been calculated and are in file {str(os.getcwd())}/data/{data_filename[-1]}
""")
	amount = int(input(Fore.YELLOW + 'How many numbers do you want to calculate? '))
	print('This will give you a total of ' + str(amount + n - 1) + '\n')
	start = time.time()
	# while True:
	data_list = []
	
	
	def write_and_compute(amount, last_num, data_filename):
		data_list = []
		try:
			for i in tqdm(
					range(amount),
					colour='green',
					unit=' numbers',
					ncols=200):
				tqdm.color = 'green'
				data = collatz(last_num)
				data_list.append(data)
				last_num += 1
			print(f"{Fore.LIGHTGREEN_EX}Finished Calculating!")
			data_file = open(data_filename, 'a')
			for i in tqdm(
					range(len(data_list)),
					colour='blue',
					unit=' numbers',
					ncols=200):
				tqdm.color = 'green'
				data_file.write(str(data_list[i]) + '\n')
			data_file.close()
			print(f'{Fore.LIGHTGREEN_EX}Finished writing to file {data_filename}')
			del data_file
			del data_list
		except OverflowError:
			print(Fore.YELLOW + "tqdm progress bar is not working,\nnumber to large,\nrunning without progress bar")
			date_time = datetime.datetime.now()
			date_time = date_time.strftime("%Y-%b-%d %H:%M:%S")
			log = open(log_filename, 'a')
			log.write(date_time + ' | too many iterations for tqdm progress bar, continuing without progress bar\n')
			log.close()
			for i in range(0, amount):
				data = collatz(last_num)
				data_list.append(data)
				last_num += 1
			print(f'{Fore.LIGHTGREEN_EX}Finished calculating!')
			data_file = open(data_filename, 'a')
			for i in range(amount):
				data_file.write(str(data_list[i]) + '\n')
			data_file.close()
			print(f'{Fore.LIGHTGREEN_EX}Finished writing to file {data_filename}')
			del data_file
			del data_list
	
	lastfilename = find('collatz_*-*.txt', str(os.getcwd()+'/data/'))
	print("lastfilename: " + str(lastfilename))
	print("lastfilename[-1]: " + str(lastfilename[-1]))
	prev = numlines
	maximum = power
	num_lines_left_prev_file = maximum - prev
	amount_left = amount - num_lines_left_prev_file
	if amount_left > 0:
		# more than the last file is needed
		num_files_needed = math.ceil(amount_left / maximum)
		data_to_files = [num_lines_left_prev_file]
		for i in range(num_files_needed):
			amount_left_2 = amount_left - maximum
			if amount_left_2 > 0:
				data_to_files.append(maximum)
				amount_left = amount_left - maximum
			else:
				data_to_files.append(amount_left)
	else:
		# data can be written to only the last file
		data_to_files = [amount]
	if data_to_files[0] != 0:
		write_and_compute(
			amount=data_to_files[0],
			last_num=int(file_data)+1,
			data_filename=str(os.getcwd()) + '/data/' + lastfilename[-1]
		)
		print(Fore.YELLOW + f'Letting ram "cool down", pausing for {cooldown} seconds')
		time.sleep(cooldown)
		file_data = int(file_data) + data_to_files[0]
	
	formatted_last_file = lastfilename[-1]
	formatted_last_file = formatted_last_file.replace('collatz_', '')
	formatted_last_file = formatted_last_file.replace('.txt', '')
	formatted_dash_index = formatted_last_file.index('-')
	file_part_first = formatted_last_file[:formatted_dash_index]
	file_part_last = formatted_last_file[formatted_dash_index+1:]
	
	print(data_to_files)
	
	for value_index in range(len(data_to_files)):
		if value_index != 0:
			value = data_to_files[value_index]
			# compute and write required amount to fill file
			if len(data_to_files) != 1:
				dash_index = lastfilename[-1].index('-')
				newfilename = f'{os.getcwd()}/data/collatz_{str(int(file_part_first) + (power*value_index))}-{str(int(file_part_last) + (power*value_index))}.txt'
				newfile = open(newfilename, 'x')
				newfile.close()
				write_and_compute(
					amount=value,
					last_num=int(file_data)+1,  # int(file_data)+1+value-power
					data_filename=newfilename
				)
				print(Fore.YELLOW + f'Letting ram "cool down", pausing for {cooldown} seconds')
				time.sleep(cooldown)
				file_data = int(file_data) + value
	end = time.time()
	elapsed = str(datetime.timedelta(seconds=round(end-start, 0)))
	print(
		f"""
\n\n\n\n{Fore.LIGHTGREEN_EX}Calculations completed!
{amount} numbers have been calculated and written to data files.
It took {elapsed} to compute and write this data.
This gives you a total of {str(amount+n-1)}
The data files can be found in:
{str(os.getcwd())}/data/
		"""
	)
except KeyboardInterrupt:
	print(Fore.RED + "\nInterrupted by user, exiting")
	sys.exit()
except Exception as e:
	ex = traceback.format_exc()
	print('\n' + str(ex) + '\n\n')
	date_time = datetime.datetime.now()
	date_time = date_time.strftime("%Y-%b-%d %H:%M:%S")
	log = open(log_filename, 'a')
	log.write(date_time + ' | ' + str(ex) + '\n')
	log.close()
	print(Fore.RED + "\n[!!!] Got an error, see collatz_log.txt for more information")
	sys.exit()
