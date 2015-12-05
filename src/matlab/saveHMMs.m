prefix = '4hmm'

str = 'UD'
a1
b1
p1
C1
csvwrite(sprintf('%s%s_a.csv', prefix, str), a1)
csvwrite(sprintf('%s%s_b.csv', prefix, str), b1)
csvwrite(sprintf('%s%s_p.csv', prefix, str), p1)
csvwrite(sprintf('%s%s_obs.csv', prefix, str), C1)

str = 'LL'
a2
b2
p2
C2
csvwrite(sprintf('%s%s_a.csv', prefix, str), a2)
csvwrite(sprintf('%s%s_b.csv', prefix, str), b2)
csvwrite(sprintf('%s%s_p.csv', prefix, str), p2)
csvwrite(sprintf('%s%s_obs.csv', prefix, str), C2)

str = 'LR'
a3
b3
p3
C3
csvwrite(sprintf('%s%s_a.csv', prefix, str), a3)
csvwrite(sprintf('%s%s_b.csv', prefix, str), b3)
csvwrite(sprintf('%s%s_p.csv', prefix, str), p3)
csvwrite(sprintf('%s%s_obs.csv', prefix, str), C3)
str = 'NO'
a4
b4
p4
C
csvwrite(sprintf('%s%s_a.csv', prefix, str), a4)
csvwrite(sprintf('%s%s_b.csv', prefix, str), b4)
csvwrite(sprintf('%s%s_p.csv', prefix, str), p4)
csvwrite(sprintf('%s%s_obs.csv', prefix, str), C)
