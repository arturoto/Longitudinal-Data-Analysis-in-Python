import sys

file_path = sys.argv[1]
'''../Datasets/RIESBY.DAT.txt'''

with open(file_path) as file:
	vocab_list = file.readlines()

#print(vocab_list)
return_list = []

word = []
for index, i in enumerate(vocab_list):
	word = i.split(' ')
	#print(word)

	finalStr = []
	comma = False

	#print(word)
	for string in word:

		if string == '':
			continue
		elif string == '\n':
			# print(string)
			#comma = True
			finalStr.append(string)

		elif string != '':
			# print(string)
			#comma = True
			finalStr.append(string)
			finalStr.append(',')
		else:
			continue

	vocab_list[index] = finalStr


final_list = []
for x in vocab_list:
	final_list.append(''.join(x))

final_string = ''.join(final_list)



save_as = file_path = sys.argv[2]
file_object = open(save_as, 'w')
file_object.write(final_string)
file_object.close()



