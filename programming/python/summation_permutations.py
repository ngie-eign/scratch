#!/usr/bin/env python

flags = [pow(2, i) for i in range(5)]
print('=' * 16)
print('Flags')
print('=' * 16)
for flag in flags:
    print('0x%02x' % (flag, ))

flags_post = []
end = len(flags)
while 0 <= end:
    start = 0
    while start < end:
        flag = sum(flags[start:end])
        if flag not in flags_post:
            flags_post.append(flag)
        start += 1
    end -= 1
flags_post.sort()

print('=' * 16)
print('Flags (After)')
for flag in flags_post:
    print('0x%02x' % (flag, ))
print('=' * 16)
