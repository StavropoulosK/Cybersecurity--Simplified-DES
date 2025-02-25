import time



def P8(LS):
    # permutation P8
    return [ LS[5], LS[2], LS[6], LS[3], LS[7], LS[4], LS[9], LS[8] ]

def P10(K):
    # permutation P10

    return [K[2],K[4], K[1],K[6],K[3], K[9], K[0], K[8],K[7], K[5] ]

def getSubkeys(K):
    # Dimiourgi ta ipoklidia K1,K2

    # permutation p10
    Permutation10= P10(K)

    # aristera 5 bit
    Left= Permutation10[0:5]

    # deksia  5 bit
    Right=Permutation10[5:10]

    # left shift kathe pentada apo bits

    LS_Left= Left[1:]+[ Left[0] ]
    LS_Right= Right[1:]+[ Right[0] ] 

    LS = LS_Left + LS_Right


    # permutation P8 gia ipologismo ipoklidiou K1

    K1= P8(LS)


    # left shift dio bits sto LS_Left kai LS_Right

    LS_Left_2=  LS_Left[2:]+ [LS_Left[0]] + [LS_Left[1]]
    LS_Right_2= LS_Right[2:]+ [LS_Right[0]] + [LS_Right[1]]

    LS_2= LS_Left_2+LS_Right_2

    K2= P8(LS_2)

    return (K1,K2)


def IP(P):
    # permutation IP
    return [P[1],P[5], P[2],P[0],P[3], P[7], P[4], P[6] ]

def IPinv(IPinv):
    # inverse IP permutation
    return [IPinv[3],IPinv[0], IPinv[2],IPinv[4],IPinv[6], IPinv[1], IPinv[7], IPinv[5] ]

def Expand_and_Permute(n):
    # praksi E/P
    return [ n[3], n[0], n[1], n[2], n[1], n[2], n[3], n[0] ] 

def addKey(T,K):
    # xor subkey me to apotelesma tou E/P
    return [ T[0]^K[0], T[1]^K[1], T[2]^K[2], T[3]^K[3], T[4]^K[4], T[5]^K[5], T[6]^K[6], T[7]^K[7] ]


def S0(Left):
    # Substitution box S0

    # To proto kai to tetarto bit kathorizoun ti grami. 
    # To deutero kai to trito bit kathorizoun ti stili.
    # Ta metatrepoume stin dekadiki anaparastasi tous.

    S0_table=[ [1,0,3,2], [3,2,1,0], [0,2,1,3], [3,1,3,2] ]

    row= Left[0]*2+Left[3]
    column= Left[1]*2+Left[2]

    substitution= S0_table[row][column]

    return convertDecimalToBinary(substitution)

def S1(Right):
    # Substitution box S1

    # To proto kai to tetarto bit kathorizoun ti grami. 
    # To deutero kai to trito bit kathorizoun ti stili.
    # Ta metatrepoume stin dekadiki anaparastasi tous.

    S1_table=[ [0,1,2,3], [2,0,1,3], [3,0,1,0], [2,1,0,3] ]

    row= Right[0]*2+Right[3]
    column= Right[1]*2+Right[2]

    substitution= S1_table[row][column]

    return convertDecimalToBinary(substitution)


def convertDecimalToBinary(decimal_number):
    # Convert Decimal to binary

    binary_representation = (bin(decimal_number))[2:]

    result = [int(char) for char in binary_representation]

    if(len(result)==1):
        # to apotelesma einai panta 2 bit
        result = [0] + result

    return result


def F(R,SK):
    # H sinartisi F

    # praksi E/P
    B= Expand_and_Permute(R)

    # xor subkey me to apotelesma tou E/P
    C= addKey(B,SK)

    # diaxorismos se aristero kai deksio komati ton 4 bit to kathena
    L_C= C[0:4]
    R_C= C[4:]


    # substitution boxes
    res_left=S0(L_C)
    res_right=S1(R_C)

    # sinenosi
    value= res_left + res_right

    # Permutation P4
    result= P4(value) 

    return result



def P4(result):
    # Permutation P4
    return [ result[1], result[3], result[2], result[0] ]


def fK(L,R,SK):
    # H sinartisi fK


    D= F(R,SK)

    # xor ton 4 left bit me to apotelesma tis F
    result= [ L[0]^D[0], L[1]^D[1], L[2]^D[2], L[3]^D[3] ]


    return result


def Switch(Left, Right):
    # kanei switch ta 4 aristera bits me ta 4 deksia 
    return Right+Left

def encrypt(P,key):
    # Kriptografisi tou plaintext

    # ypoklidia K1,K2
    a=getSubkeys(key)
    K1= a[0]
    K2= a[1]

    # Arxiko permutation
    A= IP(P)

    # xorismos se left kai right.
    L= A[0:4]
    R= A[4:]

    # apotelesma tis fK
    C= fK(L,R,K1)

    # switch
    value= Switch (C, R)


    # diaxorismos se left kai right
    L2= value[0:4]
    R2= value[4:]

    # deutero apotelesma tis fK
    C2= fK(L2,R2,K2)


    # inverse permutation tou C2 kai R2 gia na prokipsi to ciphertext
    ciphertext= IPinv ( C2+ R2 )

    return ciphertext


def decrypt(ciphertext,key):
    # apokriptografisi ciphertext

    # ypoklidia K1,K2
    a=getSubkeys(key)
    K1= a[0]
    K2= a[1]

    # Arxiko permutation
    A= IP(ciphertext)


    # xorismos se left kai right.
    L= A[0:4]
    R= A[4:]

    # apotelesma tis fK
    C= fK(L,R,K2)

    # switch
    value= Switch (C, R)


    # diaxorismos se left kai right
    L2= value[0:4]
    R2= value[4:]

    # deutero apotelesma tis fK
    C2= fK(L2,R2,K1)


    # inverse permutation tou C2 kai R2 gia na prokipsi to plaintext
    plaintext= IPinv ( C2+ R2 )

    return plaintext


def time_Simple_Des():
    K=[1,0,1,0,0,0,0,0,1,0]
    P= [1, 0, 0, 1, 0, 1, 1, 1]

    # P=[1,0,1,0,1,0,1,0]
    # K=[1,1,0,1,0,0,1,1,0,1]

    start = time.time()

    for i in range(10**4):
        ciphertext=encrypt(P,K)
        decryped_Plaintext= decrypt(ciphertext,K)

    end = time.time()

    print('\n\n\n')
    print('elapsed time: ',end - start)


# Gia ton elegxo tis sostis ilopoiisis tou algorithmou, ton dokimasame se 
# 3 diaforetika paradigmata. Kai stis 3 periptosis ta klidia, to ciphertext kai
# to decrypted plaintext  pou ipologizetai apo ton algorithmo mas einai to idio me auta poy
# ipologizontai sta paradigmata.


# https://www.geeksforgeeks.org/simplified-data-encryption-standard-set-2/?ref=next_article
K=[1,0,1,0,0,0,0,0,1,0]
P= [1, 0, 0, 1, 0, 1, 1, 1]


# https://terenceli.github.io/assets/file/mimaxue/SDES.pdf
# P=[ 0,0,1,0,1,0,0,0]
# K=[ 1,1,0,0,0,1,1,1,1,0]

# https://math.umd.edu/~immortal/ClassNotes/simplifieddes.pdf
# P=[1,0,1,0,1,0,1,0]
# K=[1,1,0,1,0,0,1,1,0,1]



ciphertext=encrypt(P,K)
decryped_Plaintext= decrypt(ciphertext,K)


print("plaintext ",P)
print("K1: ",  getSubkeys(K)[0])
print("K2: ",  getSubkeys(K)[1])
print("ciphertext ", ciphertext)  
print("decrypted plaintext ", decryped_Plaintext)


# xronometrisi epidosis algorithmou

# time_Simple_Des()


