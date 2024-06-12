from helpers.git_interact import git_add, git_interact

with open('testing.txt', 'w', encoding = 'utf-8') as file:
  file.write('hello world')
git_add('testing.txt')
git_interact(['commit', '-m', '"testing git"'])
git_interact(['push', 'origin', 'main'])