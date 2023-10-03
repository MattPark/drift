
import argparse
import random
import numpy as np
import matplotlib.pyplot as plt

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_samples', type=int, required=True)
    parser.add_argument('--num_sites', type=int, required=True)
    parser.add_argument('--max_offspring', type=float, required=True)
    parser.add_argument('--max_generations', type=int, default=10)
    return parser.parse_args()

def get_ac(P):
    return [sum(s) for s in zip(*P)]

def get_af(P):
    ac = get_ac(P)
    return [locus/len(P) for locus in ac]

def get_samples(num_samples, num_sites):
    return [[1 if j in random.sample(range(num_sites), random.randint(0, num_sites)) else 0 for j in range(num_sites)] for i in range(num_samples)]

def mate(mom, dad, num_offspring):
    return [[random.choice([mom[j], dad[j]]) for j in range(len(mom))] for i in range(num_offspring)]

def get_pairs(breeders):
    pairs = []
    while len(breeders) > 0:
        a = breeders.pop()
        if len(breeders) > 0:
            b = breeders.pop(random.randrange(len(breeders)))
            pairs.append([a,b])
    return pairs

def one_generation(P, max_offspring):
    _P = []
    pairs = get_pairs(list(range(len(P))))
    for pair in pairs:
        offspring = mate(P[pair[0]], P[pair[1]], random.randint(0, max_offspring))
        _P += offspring
    return _P

def n_generations(P, max_generations, max_offspring):
    AF = [get_af(P)]
    for i in range(max_generations):
        P = one_generation(P, max_offspring)
        if len(P) == 0:
            break
        AF.append(get_af(P))
    return AF

def line_plot_with_timestamp(AF, base_file_name):
    fig, ax = plt.subplots()
    for i in range(len(AF[0])):
        Y = [g[i] for g in AF]
        ax.plot(range(len(Y)), Y, label=str(i))
    ax.set_ylabel('Allele freq.')
    ax.set_xlabel('Generation')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.legend(frameon=False)
    fig.savefig(out_file)
    return out_file

def main_with_timestamp():
    try:
        args = get_args()
        
        # Validate inputs
        if args.num_samples <= 0:
            raise ValueError("Number of samples should be a positive integer.")
        if args.num_sites <= 0:
            raise ValueError("Number of sites should be a positive integer.")
        if args.max_offspring <= 0:
            raise ValueError("Maximum offspring should be a positive value.")
        if args.max_generations <= 0:
            raise ValueError("Maximum generations should be a positive integer.")

        run_name = '-'.join(['num_sites', str(args.num_sites),
                             'num_samples', str(args.num_samples),
                             'max_generations', str(args.max_generations),
                             'max_offspring', str(args.max_offspring)])
        
        P = get_samples(args.num_samples, args.num_sites)
        AF = n_generations(P, args.max_generations, args.max_offspring)
        line_plot_with_timestamp(AF, run_name)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
