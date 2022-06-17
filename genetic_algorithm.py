from cmath import inf
import random
import os
file_path = 'data.txt'
max_weight = random.randint(30,100)
def generateProduct(size):
    with open('data.txt', 'a') as f:
        f.write(str(max_weight) + "\n")
        f.write("name, " + "weight, " + "value" + "\n")

    for i in range(size):
        weight = random.randint(1,25)
        value = random.randint(5,30)
        element1 = random.randint(65,90)
        element2 = random.randint(97,122)
        element3 = random.randint(97,122)
        element4 = random.randint(97,122)
        element5 = random.randint(97,122)
        element6 = random.randint(97,122)
        arr = [chr(element1), chr(element2), chr(element3), chr(element4), chr(element5), chr(element6)]
        name = "".join(arr)
        with open('data.txt', 'a') as f:
            f.write(name + "," + str(weight) + "," + str(value) + "\n" )

if os.path.exists(file_path):
    if os.stat(file_path).st_size == 0:
        generateProduct(20)
else:
    generateProduct(20)   

''' 
    since I have 20 elements I hava to make  the size of the chromosome to  20
    so lets make the size of the size 20 and if selelected we make 1 and if not we make it 0
    what types of function to  write 

    1. Fitness Function

    2. Chromosome Initialization

    3. Initialize the population

    4. Fitness Evaluation

    5. Roulette Selection

    6. Crossover

    7. Mutation

'''


'''
-> Here we have the chromosome size equale to 20 as we have 20 items
    population size — number of individuals in the population
    parent count — number of parents that are selected from the population 
    on the base of the roulette selection. The parent count must be less than the population size.


    probability of ones in a new chromosome — probability which is used for initial population generation.
    It is the probability of one in the initial chromosome. High values may lead to the generation 
    of many individuals with fitness equal to zero. This parameter is specific to our method of 
    generation of the initial chromosome. This parameter is meaningless if your choice is any other method.



    probability of crossover — the probability of crossover i.e., if the child inherits the gene of both parents or 1.
    probability of mutation — the probability of mutation. I recommend starting at the value of 1/chromosome size 
    and increasing later as you see the change
'''

# lets write algorithm to generate chromome
def chromosome_generator(size, weights, weight_limit, probability):
    total_weight = inf
    while total_weight>weight_limit:
        chromosome = [0 for _ in range(size)]
        for i in range(len(chromosome)):
            prob = random.uniform(0,1)
            if prob<probability:
                chromosome[i] = 1
        '''
            Now it is the time to check the generated chromosome is zero fitness free
        '''
        total_weight = 0
        for i in range(len(chromosome)):
            total_weight+=chromosome[i]*weights[i]
    return chromosome

def create_full_chromosome_ppln(population_size, weight_limit, chromosome_size, weights, prob, parent = []):
    cur_generation = []
    if parent:
        cur_generation.extend(parent)
    while len(cur_generation)<population_size:
        curent_parent  = chromosome_generator(chromosome_size, weights, weight_limit, prob)
        cur_generation.append(curent_parent)
    return cur_generation


# lets write fitness function first
def fitness_function(weights, values, weight_limit, chromosome):
    cur_weight = 0
    cur_cost = 0
    for i in range(len(chromosome)):
        cur_weight+=chromosome[i]*weights[i]
    if cur_weight>weight_limit:
        return 0, cur_weight
    for i in range(len(chromosome)):
        cur_cost+=chromosome[i]*values[i]
    return cur_cost, cur_weight

def fitness_evaluate(population, weights, values, weight_limit):
    value_fit = []
    weight_fit = []
    tot_value = sum(values)
    for i in range(len(population)):
        cur_chromosome = population[i]
        value, weight = fitness_function(weights, values, weight_limit, cur_chromosome)  
        value_fit.append(value/(tot_value+1))
        weight_fit.append(weight)
    return value_fit, weight_fit
def selection(population, fitness_score, num_children):
    total_fit = sum(fitness_score)
    relative_fits = [fitness_score[i]/total_fit for i in range(len(fitness_score))]
    # print(len(relative_fits))
    cum_prob = [fitness_score[0]]
    for i in range(1, len(relative_fits)):
        cur = cum_prob[i-1] + relative_fits[i]
        cum_prob.append(cur)

    selected = []
    while len(selected)!=2 :
        for i in range(num_children):
            rate = random.uniform(0, 1)
            for index in range(len(population)):
                if cum_prob[index]>rate:
                    selected.append(population[i])
                    if len(selected)==2:
                        return selected
                    break

    return selected

def crossover(chromosome1, chromosome2, probanility_crossover):
    crossover_point = random.randint(0, 20)
    rate = random.uniform(0, 1)
    if rate<probanility_crossover:
        chromosome1[crossover_point:], chromosome2[crossover_point:] = chromosome2[crossover_point:], chromosome1[crossover_point:]
    return chromosome1, chromosome2

def mutation(chromosome, probability_mutation):
    for i in range(len(chromosome)):
        rate = random.uniform(0, 1)
        if rate<probability_mutation:
            if chromosome[i]:
                 chromosome[i] =  0
            else:
                chromosome[i] = 1
    return chromosome


weights = []
values = []
items = []
with open("data.txt","r") as text_file:
    line_reader=text_file.readlines()
    for line in line_reader:
        line_list=line.strip().split(",")
        try:
            item=line_list[0]
            weight=int(line_list[1])
            weights.append(weight)
            value=int(line_list[2])
            values.append(value)
            items.append((line_list[0],weight,value))
        except:
            continue
max_weight = 73 #random.randint(60, 100)

print(max_weight)

population_size = 8
chromosome_size = 20
create_pobability = 0.1
crossover_probability = 0.5
mutation_probability = 0.05
weight_fit = [0.000005]
accuracy = 0
parent = []
ans = []

def fitness_zero_checker(chromosome, weight, weight_limit):
    tot_weigh = 0
    for i in range(len(chromosome)):
        tot_weigh+=chromosome[i]*weight[i]
    return tot_weigh<=weight_limit


while abs(accuracy-90)>10:
    cur_generation = create_full_chromosome_ppln(population_size, max_weight, chromosome_size, weights, create_pobability, parent)
    value_fit, weight_fit = fitness_evaluate(cur_generation, weights, values, max_weight)

    selected = selection(cur_generation, value_fit, 2)
    crossover_one = []
    chromosome1, chromosome2  = selected
    chr1, chr2  = crossover(chromosome1, chromosome2, crossover_probability)
    crossover_one.extend([chr1, chr2])

    mutated_one = []
    for chromosome in crossover_one:
        mut = mutation(chromosome, mutation_probability)
        while not fitness_zero_checker(mut, weights, max_weight):
            mut = mutation(mut, mutation_probability)
        mutated_one.append(mut)
            
    for chromosome in mutated_one:
        
        my_weight = 0
        my_value = 0
        for i in range(len(chromosome)):
            my_weight+=chromosome[i]*weights[i]
            my_value+=chromosome[i]*values[i]
        if accuracy<(my_weight/max_weight)*100:
            accuracy = (my_weight/max_weight)*100
            ans = [my_weight, my_value, chromosome]

print("accuracy =>",accuracy)
print("weight=>", ans[0])
print("value=>", ans[1])

chromosome = ans[2]
for i in range(len(chromosome)):
    if chromosome[i]:
        print(items[i][0])






