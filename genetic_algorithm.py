import matplotlib.pyplot as plt
import random
import os
file_path = 'my-file.txt'
max_weight = random.randint(30,100)
def generateProduct(size):
    with open('my-file.txt', 'a') as f:
        f.write(str(max_weight) + "\n")
        f.write("name, " + "weight, " + "value" + "\n")

    for _ in range(size):
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
        with open('my-file.txt', 'a') as f:
            f.write(name + "," + str(weight) + "," + str(value) + "\n" )

if os.path.exists(file_path):
    if os.stat(file_path).st_size == 0:
        generateProduct(20)
else:
    generateProduct(20)   

def chromosome_generator(size, weights, weight_limit, probability):
    total_weight = float("inf")
    while total_weight>weight_limit:
        chromosome = [0 for _ in range(size)]
        for i in range(len(chromosome)):
            prob = random.uniform(0,1)
            if prob<probability:
                chromosome[i] = 1
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
    relative_fits = [fitness_score[i]/(total_fit+0.1) for i in range(len(fitness_score))]
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
with open("my-file.txt","r") as text_file:
    line_reader=text_file.readlines()
    max_weight = int(line_reader[0])
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


def fitness_zero_checker(chromosome, weight, weight_limit):
    tot_weigh = 0
    for i in range(len(chromosome)):
        tot_weigh+=chromosome[i]*weight[i]
    return tot_weigh<=weight_limit
def genetic_algoritm(item_size):
    population_size = 6
    chromosome_size = item_size
    create_pobability = 0.5
    crossover_probability = 0.5
    mutation_probability = 0.05
    accuracy = 0
    parent = []
    ans = [0, 0, []]
    epochs = 0
    best_chromosome = [0]*chromosome_size
    best_value = 0
    best_weight = 0
    top_va = 0
    while abs(accuracy-100)>20 or epochs<50:
        epochs+=1
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
            top_va = max(top_va, my_value)
            cur_accurancy = (my_weight/max_weight)*100
            if my_value > ans[1]:
                accuracy = cur_accurancy
                ans = [my_weight, my_value, chromosome]
            if ans[1]>best_value:
                best_chromosome = ans[2]
                best_value = ans[1]
                best_weight = ans[0]
    ans = [best_weight, best_value, best_chromosome]
    chromosome = ans[2]
    return ans
best_weight1, best_value1, chr1 =  genetic_algoritm(10)
best_weight2, best_value2, chr2 =  genetic_algoritm(15)
best_weight3, best_value3, chr3 =  genetic_algoritm(20)
num_selected1 = chr1.count(1)
num_selected2 = chr2.count(1)
num_selected3 = chr3.count(1)



  
left = [best_value1, best_value2, best_value3]
  
height = [10, 15, 20]
  
tick_label = ['10 data & weight '+ str(best_weight1), '15 data & weight '+str(best_weight2), '20 data & weight '+str(best_weight3)]
  
plt.bar(height, left,  tick_label = tick_label,
        width = 0.8, color = ['red', 'green', 'yellow'])
  
plt.xlabel(('red = ' + str(num_selected1)+ ' item selected, ' + 'green = '+ str(num_selected2)+ ' item selected, '+ 'yellow = '+ str(num_selected3) + ' item selected'))
plt.ylabel('Max_value we get')
plt.title('The knapsack problem with genetic algorithm with weight limit '+str(max_weight))
  
plt.show()




