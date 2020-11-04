#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Description

"""

import torch

import numpy as np

from ptranking.ltr_global import ltr_seed
from ptranking.ltr_adversarial.eval.ltr_adversarial import AdLTREvaluator

np.random.seed(seed=ltr_seed)
torch.manual_seed(seed=ltr_seed)


if __name__ == '__main__':

    """
    >>> Learning-to-Rank Models <<< 
    
    (2) Adversarial Optimization
    -----------------------------------------------------------------------------------------
    | Pointwise | IRGAN_Point % IRFGAN_Point                                                |
    -----------------------------------------------------------------------------------------
    | Pairwise  | IRGAN_Pair % IRFGAN_Pair                                                  |
    -----------------------------------------------------------------------------------------
    | Listwise  | IRGAN_List % IRFGAN_List                                                  |
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
    | IRGAN_MQ2008_Semi                                                                      |
    -----------------------------------------------------------------------------------------

    """

    debug = False  # in a debug mode, we just check whether the model can operate

    config_with_json = True  # specify configuration with json files or not

    models_to_run = [
        #'IRGAN_Point',
        #'IRGAN_Pair',
        #'IRGAN_List'
        #'IRFGAN_Point',
        #'IRFGAN_Pair',
        'IRFGAN_List'
    ]

    evaluator = AdLTREvaluator()

    if config_with_json:  # specify configuration with json files
        # the directory of json files
        #dir_json = '/home/dl-box/WorkBench/ExperimentBench/ALTR/ecir2021/irgan/mq2008_json/'
        #dir_json = '/home/dl-box/WorkBench/ExperimentBench/ALTR/ecir2021/irgan/mq2008_semi_json/'

        dir_json = '/home/dl-box/WorkBench/ExperimentBench/ALTR/ecir2021/irfgan/mq2008_json/'
        #dir_json = '/home/dl-box/WorkBench/ExperimentBench/ALTR/ecir2021/irfgan/mq2008_semi_json/'

        #dir_json = '/Users/dryuhaitao/WorkBench/Dropbox/CodeBench/GitPool/irgan_ptranking/testing/ltr_adversarial/json/'

        for model_id in models_to_run:
            evaluator.run(debug=debug, model_id=model_id, config_with_json=config_with_json, dir_json=dir_json)

    else:  # specify configuration manually
        data_id = 'MQ2008_Super'

        ''' location of the adopted data '''
        dir_data = '/Users/dryuhaitao/WorkBench/Corpus/' + 'LETOR4.0/MQ2008/'
        #dir_data = '/home/dl-box/WorkBench/Datasets/L2R/LETOR4.0/MQ2008/'
        #dir_data = '/Users/solar/WorkBench/Datasets/L2R/LETOR4.0/MQ2008/'

        ''' output directory '''
        dir_output = '/Users/dryuhaitao/WorkBench/CodeBench/Bench_Output/NeuralLTR/ALTR/'
        #dir_output = '/home/dl-box/WorkBench/CodeBench/PyCharmProject/Project_output/Out_L2R/Listwise/'
        #dir_output = '/Users/solar/WorkBench/CodeBench/PyCharmProject/Project_output/Out_L2R/'

        grid_search = False # with grid_search, we can explore the effects of different hyper-parameters of a model

        for model_id in models_to_run:
            evaluator.run(debug=debug, model_id=model_id, data_id=data_id, dir_data=dir_data, dir_output=dir_output, grid_search=grid_search)
