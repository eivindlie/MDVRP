import trainer

generations = 1000
crossover_rate = 0.4
heuristic_mutate_rate = 0
inversion_mutate_rate = 0.2
depot_move_mutate_rate = 0
best_insertion_mutate_rate = 0.2

if __name__ == '__main__':
    current_problem = 'p13'
    trainer.load_problem('../data/' + current_problem)
    trainer.initialize()
    best_solution = trainer.train(generations, crossover_rate, heuristic_mutate_rate, inversion_mutate_rate,
                                  depot_move_mutate_rate, best_insertion_mutate_rate, intermediate_plots=True)

    if best_solution:
        trainer.save_solution(best_solution, '../solutions/' + current_problem)

    # for i in range(13, 24):
    #     if i < 10:
    #         n = '0' + str(i)
    #     else:
    #         n = str(i)
    #     print('p' + n)
    #     load_problem('../data/p' + n)
    #     initialize()
    #     best_solution = train(generations, crossover_rate, heuristic_mutate_rate, inversion_mutate_rate,
    #           intermediate_plots=True, log=True)
    #     save_solution(best_solution, '../solutions/p' + n)
