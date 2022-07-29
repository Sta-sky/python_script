def search(num_list, num):
  n = len(num_list)
  fisrt = 0
  last = n - 1
  while fisrt <= last:
    mid = (fisrt + last) // 2
    if num_list[mid] == num:
      return True
    elif num < num_list[mid]:
      last = mid - 1
    else:
      fisrt = mid + 1
  return False

li = [12, 21, 26, 30, 56, 54, 55, 97, 43]
print(search(li, 55))



