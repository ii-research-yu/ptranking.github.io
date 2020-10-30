#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Description

"""

import numpy as np

from ptranking.ltr_global import ltr_seed
from ptranking.ltr_tree.eval.ltr_tree import TreeLTREvaluator

np.random.seed(seed=ltr_seed)


if __name__ == '__main__':

    """
    >>> Tree-based Learning-to-Rank Models <<<
    
    (3) Tree-based Model
    -----------------------------------------------------------------------------------------
    | LightGBMLambdaMART                                                                    |
    -----------------------------------------------------------------------------------------
    
    >>> Supported Datasets <<<
    -----------------------------------------------------------------------------------------
    | LETTOR    | MQ2007_Super %  MQ2008_Super %  MQ2007_Semi %  MQ2008_Semi                |
    -----------------------------------------------------------------------------------------
    | MSLRWEB   | MSLRWEB10K %  MSLRWEB30K                                                  |
    -----------------------------------------------------------------------------------------
    | Yahoo_LTR | Set1 % Set2                                                               |
    -----------------------------------------------------------------------------------------
    | ISTELLA_LTR | Istella_S | Istella | Istella_X                                         |
    -----------------------------------------------------------------------------------------
    
    """

    debug = True  # in a debug mode, we just check whether the model can operate

    config_with_json = False  # specify configuration with json files or not

    evaluator = TreeLTREvaluator()

    if config_with_json:  # specify configuration with json files
        # the directory of json files
        dir_json = '/Users/dryuhaitao/WorkBench/Dropbox/CodeBench/GitPool/wildltr_ptranking/testing/ltr_tree/json/'

        evaluator.run(debug=debug, model_id='LightGBMLambdaMART', config_with_json=config_with_json, dir_json=dir_json)

    else:
        data_id = 'MQ2008_Super'
        #data_id = 'MSLRWEB30K'

        dir_data = '/home/dl-box/WorkBench/Datasets/L2R/LETOR4.0/MQ2008/'
        #dir_data = '/Users/solar/WorkBench/Datasets/L2R/LETOR4.0/MQ2008/'
        #dir_data = '/Users/dryuhaitao/WorkBench/Corpus/' + 'LETOR4.0/MQ2008/'
        #dir_data = '/Users/dryuhaitao/WorkBench/Corpus/Learning2Rank/MSLR-WEB30K/'

        #data_id  = 'Istella_S'
        #dir_data = '/home/dl-box/WorkBench/Datasets/L2R/ISTELLA_L2R/'

        ''' output directory '''
        #dir_output = '/Users/dryuhaitao/WorkBench/CodeBench/Bench_Output/NeuralLTR/Listwise/'
        dir_output = '/home/dl-box/WorkBench/CodeBench/PyCharmProject/Project_output/Out_L2R/Listwise/'
        #dir_output = '/Users/solar/WorkBench/CodeBench/PyCharmProject/Project_output/Out_L2R/'

        grid_search = False  # with grid_search, we can explore the effects of different hyper-parameters of a model

        evaluator.run(debug=debug, model_id='LightGBMLambdaMART',
                      data_id=data_id, dir_data=dir_data, dir_output=dir_output, grid_search=grid_search)
