
import time
import numpy as np

def divide_data(n_reconstructions, ratio = [.8,.1,.1], test_set = True, random = False):
	"""
	Divide dataset into training, validation and test set
	Inputs:
		n_reconstructions - number of reconstructions in dataset
		ratio - ratio of data given to each set (training,validation,test)
		test_set - if one wants to have test set
		random - indexes are choosen randomly if True
	Outputs:
		i_train,i_valid,i_test - indexes of training, validation  and test set
	"""

	assert np.sum(ratio) == 1.

	if test_set:
		assert len(ratio) == 3

	else:
		assert len(ratio) == 2
			
	if random:
		np.random.seed(0)

		r = np.arange(n_reconstructions)
		np.random.shuffle(r)

		i_train = r[:int(ratio[0]*n_reconstructions)]
		i_valid = r[int(ratio[0]*n_reconstructions):int((ratio[0]+ratio[1])*n_reconstructions)]

		if test_set:
			i_test  = r[int((ratio[0]+ratio[1])*n_reconstructions):]

	else :
		r = np.arange(n_reconstructions)
		i_valid = r[(r+1) % int(ratio[1]*100) == 0]

		if test_set:
			i_test  = r[(r+2) % int(ratio[2]*100) == 0]
			i_train = r[((r+1) % int(ratio[1]*100) != 0)*((r+2) % int(ratio[2]*100) != 0)]
		
		else:
			i_train = r[(r+1) % int(ratio[1]*100) != 0]

	if not(test_set):
		i_test = []

	return i_train,i_valid,i_test

def resize_NN_image(tomo, training = False):
	"""
	Resize image either for NN training or afterwards for comparison with original
	Inputs:
		tomo - original reconstruction
		training - True to transform from original -> NN , False to transform NN -> original 
	Outputs:
		tomo - reshaped reconstruction
	"""
	if training:
		tomo = np.swapaxes(tomo,1,2)
		tomo = np.lib.pad(tomo, ((0,0),(2,3),(2,2)), 'constant')
		tomo = tomo[:,np.newaxis,:,:]

	else:
		tomo = tomo[:,0,2:-3,2:-2]
		tomo = np.swapaxes(tomo,1,2)
	
	return tomo
