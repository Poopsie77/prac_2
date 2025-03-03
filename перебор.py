import math
for a11 in range(1,10):
    for a12 in range(1, 10):
        for a21 in range(1, 10):
            for a22 in range(1, 10):
                if ((a11*a22) - (a21*a12) !=0) and (math.gcd((a11*a22) - (a21*a12),33)==1):
                    if ((a11*14+a12*9)%33 == 4) and ((a21*14 + a22*9)%33 == 13):
                        print('ключ k1: ',a11,'',a12,'',a21,'',a22)


for a_11 in range(1,10):
    for a_12 in range(1, 10):
        for a_21 in range(1, 10):
            for a_22 in range(1, 10):
                if ((a_11*a_22) - (a_21*a_12) !=0) and (math.gcd((a_11*a_22) - (a_21*a_12),33)==1):
                    if ((a_11*19+a_12*15)%33 == 6) and ((a_21*19 + a_22*15)%33 == 2):
                        print('ключ k2: ',a_11,'',a_12,'',a_21,'',a_22)