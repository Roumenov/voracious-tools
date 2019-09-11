import pymel.core as pm


def fib(n):
    index = 0
    sequence = range(n)
    print 'start sequence' + str(sequence)
    while index < n:
        print 'index: ' + str(index)
        if index == 0:
            sequence[index] = 1
        elif index == 1:
            sequence[index] = 1
        else:
            sequence[index] = sequence[index-1] + sequence[index-2]
        print 'index value ' + str(sequence[index])
        index += 1
    return sequence


#iterate backwards over fib sequence

joints = pm.ls(sl=1)
n = len(joints)
fib_seq = fib(n)
print fib_seq
check_sum = sum(fib_seq)

distance = 8.5
for num in range(len(joints)):
    print num
    print fib_seq[num]
    joints[num].tx.set(distance/(fib_seq[num]+1))



value = num*(1.0/float(sum(fib_seq)))
joints[num].tx.set(value)