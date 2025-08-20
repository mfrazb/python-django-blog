name = 'Meredith'
name3Times = 'Meredith' * 3
print(name)
print(name3Times)

# list
names = ['Sara', 'Meredith', 'Shavone', 'Deanna', 'Peyton']

# practice with if else 
if 2 > 3:
  print('You got it girl')
else: 
  print('not so much')

# practice with else if 
if 'Dog' in names: 
  print('Dog is in the list')
elif 'Meredit' in names:
  print ('Meredith is in the list')
else:
  print ('No names in list')

# functions and parameters
def hi(name):
  print(f'Hello {name}!')

# function execution
hi('Sandy')

# loops 
# for name in names:
#   hi(name)
#   print('Next name')

# loops with numbers 
for i in range(1, 6):
  print(i)

# loop based on list index
for i in range(len(names) - 2):
  print(names[i])

# while loops
i = 0
while i < 10:
  print(i)
  i += 1
