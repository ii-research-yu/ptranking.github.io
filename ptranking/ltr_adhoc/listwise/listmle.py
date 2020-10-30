#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Description

"""

import torch

from ptranking.base.ranker import NeuralRanker

class LogCumsumExp(torch.autograd.Function):
	'''
	The PyTorch OP corresponding to the operation: log{ |sum_k^m{ exp{pred_k} } }
	'''
	@staticmethod
	def forward(ctx, input):
		'''
		In the forward pass we receive a context object and a Tensor containing the input;
		we must return a Tensor containing the output, and we can use the context object to cache objects for use in the backward pass.
		Specifically, ctx is a context object that can be used to stash information for backward computation.
		You can cache arbitrary objects for use in the backward pass using the ctx.save_for_backward method.
		:param ctx:
		:param input: i.e., batch_preds of [batch, ranking_size], each row represents the relevance predictions for documents within a ltr_adhoc
		:return: [batch, ranking_size], each row represents the log_cumsum_exp value
		'''

		m, _ = torch.max(input, dim=1, keepdim=True)    #a transformation aiming for higher stability when computing softmax() with exp()
		y = input - m
		y = torch.exp(y)
		y_cumsum_t2h = torch.flip(torch.cumsum(torch.flip(y, dims=[1]), dim=1), dims=[1])    #row-wise cumulative sum, from tail to head
		fd_output = torch.log(y_cumsum_t2h) + m # corresponding to the '-m' operation

		ctx.save_for_backward(input, fd_output)

		return fd_output


	@staticmethod
	def backward(ctx, grad_output):
		'''
		In the backward pass we receive the context object and
		a Tensor containing the gradient of the loss with respect to the output produced during the forward pass (i.e., forward's output).
		We can retrieve cached data from the context object, and
		must compute and return the gradient of the loss with respect to the input to the forward function.
		Namely, grad_output is the gradient of the loss w.r.t. forward's output. Here we first compute the gradient (denoted as grad_out_wrt_in) of forward's output w.r.t. forward's input.
		Based on the chain rule, grad_output * grad_out_wrt_in would be the desired output, i.e., the gradient of the loss w.r.t. forward's input
		:param ctx:
		:param grad_output:
		:return:
		'''

		input, fd_output = ctx.saved_tensors
		#chain rule
		bk_output = grad_output * (torch.exp(input) * torch.cumsum(torch.exp(-fd_output), dim=1))

		return bk_output


apply_LogCumsumExp = LogCumsumExp.apply


class ListMLE(NeuralRanker):
	'''
	ListMLE: Fen Xia, Tie-Yan Liu, Jue Wang, Wensheng Zhang, and Hang Li. 2008. Listwise Approach to Learning to Rank: Theory and Algorithm.
	In Proceedings of the 25th ICML. 1192–1199.
	'''
	def __init__(self, sf_para_dict=None):
		super(ListMLE, self).__init__(id='ListMLE', sf_para_dict=sf_para_dict)

	def inner_train(self, batch_preds, batch_stds, **kwargs):
		if 'presort' in kwargs and kwargs['presort']:
			target_batch_preds, target_batch_stds = batch_preds, batch_stds
		else:
			target_batch_stds, batch_sorted_inds = torch.sort(batch_stds, dim=1, descending=True)
			target_batch_preds = torch.gather(batch_preds, dim=1, index=batch_sorted_inds)

		batch_logcumsumexps = apply_LogCumsumExp(target_batch_preds)
		batch_loss = torch.sum(batch_logcumsumexps - target_batch_preds)

		self.optimizer.zero_grad()
		batch_loss.backward()
		self.optimizer.step()

		return batch_loss
