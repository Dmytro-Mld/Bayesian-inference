import random

# Cipher table. There columns represent open text, rows represent keys and elements at the intersection are cipher texts  
CIPHER_TABLE = [
    [10,    13,	8,	18,	12,	7,	0,	6,	14,	1,	9,	17,	2,	16,	5,	4,	11,	3,	19,	15],
    [14,    17,	11,	9,	10,	6,	13,	15,	5,	1,	8,	19,	4,	7,	12,	16,	18,	0,	2,	3],
    [8,	    14,	4,	5,	6,	2,	13,	19,	11,	16,	3,	1,	18,	15,	12,	7,	10,	0,	9,	17],
    [13,    5,	14,	11,	0,	15,	4,	17,	2,	19,	12,	10,	7,	16,	3,	8,	1,	18,	9,	6],
    [12,    10,	6,	4,	5,	16,	9,	8,	19,	1,	3,	13,	18,	7,	15,	2,	11,	14,	17,	0],
    [15,    19,	9,	1,	8,	12,	2,	0,	10,	3,	16,	6,	17,	4,	13,	18,	7,	11,	5,	14],
    [16,    14,	4,	7,	11,	1,	17,	9,	15,	18,	2,	12,	3,	0,	6,	19,	8,	10,	13,	5],
    [2,	    5,	3,	11,	15,	19,	13,	9,	1,	6,	18,	4,	8,	16,	10,	7,	12,	14,	0,	17],
    [13,    8,	3,	10,	12,	18,	15,	5,	2,	7,	0,	14,	9,	19,	17,	1,	11,	6,	16,	4],
    [7,	    2,	18,	12,	10,	0,	16,	19,	5,	1,	15,	9,	4,	8,	6,	11,	17,	13,	14,	3],
    [13,    18,	4,	15,	3,	1,	11,	12,	16,	6,	19,	0,	8,	14,	10,	17,	9,	7,	2,	5],
    [3,	    16,	9,	12,	17,	11,	15,	19,	18,	4,	13,	6,	14,	8,	5,	1,	7,	10,	0,	2],
    [13,    4,	17,	12,	2,	8,	16,	6,	0,	15,	5,	18,	14,	11,	10,	3,	1,	9,	19,	7],
    [2,	    4,	1,	19,	3,	16,	11,	6,	15,	14,	13,	12,	17,	9,	0,	7,	8,	10,	5,	18],
    [5,	    14,	9,	0,	1,	7,	17,	15,	10,	13,	19,	3,	4,	8,	11,	16,	6,	2,	12,	18],
    [15,    8,	3,	1,	2,	13,	16,	9,	18,	0,	14,	7,	6,	11,	12,	19,	4,	10,	5,	17],
    [7,	    0,	14,	15,	17,	16,	18,	5,	19,	4,	12,	10,	8,	6,	9,	2,	3,	13,	11,	1],
    [18,    17,	7,	8,	3,	4,	1,	12,	15,	13,	2,	16,	11,	19,	9,	0,	14,	10,	6,	5],
    [1,	    16,	12,	9,	14,	2,	5,	13,	10,	11,	15,	19,	8,	17,	6,	3,	18,	0,	4,	7],
    [17,    0,	10,	19,	3,	6,	1,	13,	14,	15,	9,	4,	18,	5,	12,	11,	8,	16,	2,	7],
]

# Probability distribution of the open text space
PROB_OPEN_TEXT = [0.24, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04]

# Probability distribution of the key space
PROB_KEY = [0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]

def compute_ciphertext_probability(prob_m: list, prob_k: list, cipher_table: list[list]) -> list:
    n = len(prob_m)

    prob_ciphertext = [0 for i in range(n)]

    for m in range(n):
        for k in range(n):
            c = cipher_table[k][m]
            prob_ciphertext[c] += prob_k[k] * prob_m[m]
    
    return prob_ciphertext

def compute_open_text_ciphertext_probability(prob_m: list, prob_k: list, cipher_table: list[list]) -> list[list]:
    n = len(prob_m)

    prob = [[0 for j in range(n)] for i in range(n)]

    for m in range(n):
        for k in range(n):
            c = cipher_table[k][m]
            prob[m][c] += prob_k[k] * prob_m[m]
    
    return prob

def compute_open_text_if_ciphertext_probability(prob_m_c: list[list], prob_c: list) -> list[list]:
    n = len(prob_m_c)

    prob = [[0 for j in range(n)] for i in range(n)]

    for m in range(n):
        for c in range(n):
            prob[m][c] += prob_m_c[m][c] / prob_c[c]
 
    return prob

def compute_optimal_deterministic_decision_function(prob_m_if_c: list[list]) -> list:
    n = len(prob_m_if_c)

    rez = [0 for c in range(n)]

    for c in range(n):
        prob = prob_m_if_c[0][c]
        for m in range(n):
            if prob < prob_m_if_c[m][c]:
                prob = prob_m_if_c[m][c]
                rez[c] = m
 
    return rez

def compute_optimal_stochastic_decision_function(prob_m_if_c: list[list]) -> list:
    n = len(prob_m_if_c)

    rez = [[0 for m in range(n)] for c in range(n)]

    for c in range(n):
        max_prob_id = [0]
        prob = prob_m_if_c[0][c]
        for m in range(n):
            if prob < prob_m_if_c[m][c]:
                prob = prob_m_if_c[m][c]
                max_prob_id = [m]
            elif prob == prob_m_if_c[m][c]:
                max_prob_id.append(m)
        
        coef = 1  / len(max_prob_id)
        for id in max_prob_id:
            rez[c][id] = coef
 
    return rez

def loss_func_od_df(od_df: list) -> list:
    n = len(od_df)

    ls_func_res = [[1 for i in range(n)] for j in range(n)]

    for c in range(n):
        m = od_df[c]
        ls_func_res[m][c] = 0

    return ls_func_res

def average_losses(prob_m_c: list[list], ls_func: list[list]) -> float:
    n = len(ls_func)
    al = 0

    for m in range(n):
        for c in range(n):
            al += prob_m_c[m][c] * ls_func[m][c]

    return al

def loss_func_os_df(os_df: list) -> list:
    n = len(os_df)
    rez = [[0 for i in range(n)] for i in range(n)]

    #chosing your message number and ciphertext number

    for c in range(n):
        for m in range(n):
            for t in range(n):
                if t != m:
                    rez[c][m] += os_df[c][t]

    return rez

def bayesian_decision_from_stochastic_decision_function(prob_m_c: list[list], c) -> int:
    n_ = len(prob_m_c)

    decisional_prob_m = [0 for m in range(n_)]
    for m_ in range(1, n_, 1):
        decisional_prob_m[m_] = prob_m_c[m_][c] + decisional_prob_m[m_ - 1]
    
    p = random.uniform(0, decisional_prob_m[-1])
    for m in range(n_):
        if decisional_prob_m[m] >= p:
            return m

# Perform tests with error epsilon be allowed
def perform_tests(size: int, prob_c: list, prob_m_c: list[list], prob_m_if_c: list[list], od_df: list, os_df: list, epsilon: float=pow(10, -9)):
    # Test: sum P(c) = 1
    sum = 0
    for p_i in prob_c:
        sum += p_i

    if sum < 1.0 - epsilon and sum > 1.0 + epsilon:
        raise ValueError(f"sum should be 1 but it is {sum} instead")

    # Test: sum P(m, c) = 1
    sum = 0
    for l in prob_m_c:
        for p in l:
            sum += p

    if sum < 1 - epsilon and sum > 1 + epsilon:
        raise ValueError(f"sum should be 1 but it is {sum:0.3f} instead")
    
    # Test: sum_{m \in M} P(m, c) = 1
    for c in range(size):
        sum = 0
        for m in range(size):
            sum += prob_m_if_c[m][c]

        if sum < 1 - epsilon and sum > 1 + epsilon:
            raise ValueError(f"sum should be 1 but it is {sum:0.3f} instead")
        
    # Test: sum_{c \in C} P(m, c) = 1
    for m in range(size):
        sum = 0
        for c in range(size):
            sum += prob_m_if_c[m][c]

        if sum < 1 - epsilon and sum > 1 + epsilon:
            raise ValueError(f"sum should be 1 but it is {sum:0.3f} instead")

def print_table_float(table: list[list[float]], precision: int=3):
    for l in table:
        for c in range(len(l) - 1):
            print(f"{l[c]:0.{precision}f}", end=", ")
        
        print(f"{l[-1]:0.{precision}f}")

def print_list_float(l: list[float], precision: int=3):
    for c in range(len(l) - 1):
        print(f"{l[c]:0.{precision}f}", end=", ")
    
    print(f"{l[-1]:0.{precision}f}")

def main():
    # P(C)
    prob_c = compute_ciphertext_probability(prob_m=PROB_OPEN_TEXT, prob_k=PROB_KEY, cipher_table=CIPHER_TABLE)
    print("P(C)")
    print_list_float(prob_c, precision=2)
    print("")

    # P(M, C)
    prob_m_c = compute_open_text_ciphertext_probability(prob_m=PROB_OPEN_TEXT, prob_k=PROB_KEY, cipher_table=CIPHER_TABLE)
    print("P(M, C)")
    print_table_float(prob_m_c)
    print("")

    # P(M | C)
    prob_m_if_c = compute_open_text_if_ciphertext_probability(prob_m_c=prob_m_c, prob_c=prob_c)
    print("P(M | C)")
    print_table_float(prob_m_if_c)
    print("")

    # delta_D(C)
    od_df = compute_optimal_deterministic_decision_function(prob_m_if_c=prob_m_if_c)
    print("delta_D(C)")
    print(od_df)
    print("")

    # delta_S(M, C)
    os_df = compute_optimal_stochastic_decision_function(prob_m_if_c=prob_m_if_c)
    print("delta_S(M, C)")
    print_table_float(os_df, precision=1)
    print("")

    # Example instance of Delta_S function
    os_df_instance = [bayesian_decision_from_stochastic_decision_function(prob_m_c=os_df, c=c) for c in range(len(prob_c))]
    print("delta_S(C) instance")
    print(os_df_instance)
    print("")

    #loss_func_od_df
    ls_func_od_df = loss_func_od_df(od_df=od_df)        #function returns a 20x20 table meaning "0" if sigma(C)=M and "1" if sigma(C)!=M
    print("loss function of delta_D(M, C)")
    print_table_float(ls_func_od_df, precision=1)
    print("")

    #average_loss_func_od_df
    av_ls_od_df = average_losses(prob_m_c=prob_m_c, ls_func=ls_func_od_df)
    print("average losses of delta_D(M, C)")
    print(av_ls_od_df)
    print("")

    #loss_func_os_df
    ls_func_os_df = loss_func_os_df(os_df=os_df)
    print("loss function of delta_S(M, C)")
    print_table_float(ls_func_os_df, precision=1)
    print("")

    #average_loss_func_os_df
    av_ls_os_df = average_losses(prob_m_c=prob_m_c, ls_func=ls_func_os_df)
    print("average losses of delta_S(M, C)")
    print(av_ls_os_df)
    print("")


    perform_tests(size=20, prob_c=prob_c, prob_m_c=prob_m_c, prob_m_if_c=prob_m_if_c, od_df=od_df, os_df=os_df)



if __name__ == "__main__":
    main()