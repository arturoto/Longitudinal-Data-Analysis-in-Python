with open('VocabGrowth.txt') as file:
	vocab_list = file.readlines()


for index, i in enumerate(vocab_list):
	word = i.split(' ')

	finalStr = []
	comma = False

	#print(word)
	for string in word:
		if string != '':
			comma = False
			finalStr.append(string)
		elif string =='' and comma == False:
			comma = True
			finalStr.append(',')
		else:
			continue
		#print(finalStr)
	vocab_list[index] = finalStr
	#print('\n')


final_list = []
for x in vocab_list:
	final_list.append(''.join(x))

final_string = ''.join(final_list)

print(final_string)

file_object = open('VocabGrowth.csv', 'w')
file_object.write(final_string)
file_object.close()





	#print(word)
	#print(i.replace(' ', ',', 1))