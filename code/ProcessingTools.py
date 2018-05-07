import numpy as np


def ProcessingPresum(data, instrPresum, presum_proc):
  #
  # Presum factor
  #
  presum_fac = int(presum_proc / instrPresum)
  #
  # Get current column count of data
  #
  ncols = np.shape(data)[0]
  #
  # Output columns
  #
  outputCols = int(np.ceil( ncols / presum_factor )) 
  presumRec = np.zeros([2048, outputCols], complex)
  #
  # Now perform the presumming
  #
  for _i in range(0, ncols, presum_fac):
    presumRec[:,int(_i/4)] = np.sum(EDRData[:,_i:_i+int(presum_fac)], axis=1)
  return presumRec


def makeWindow(win_type, length=2048, beta=0):
  """
    Function for writing a windowing function
    Inputs:
      win_type: 0 -- Uniform weighting
                1 -- Cosine Bell (not working)
                2 -- Hann Window
                3 -- Hamming Window
  *** NOTE *** This will eventually include a generalized Hamming function
  """
  #
  # Construct the window function
  #
  win_str ='Window function applied to data: '
  if win_type == 0:
    window = np.ones(2048)                                      # Uniform weighting
    win_str += 'Uniform weighting'
  elif win_type == 1:
    #
    # Cosine bell
    window = np.ones(2048)                                      # Uniform weighting
    win_str += 'Uniform weighting'
  elif win_type == 2:
    window = np.bartlett(length)
    win_str += 'Bartlett Window'
  elif win_type == 3:
    window = np.hanning(length)
    win_str += 'Hanning Window'
  elif win_type == 4:
    window = np.hamming(length)
    win_str += 'Hamming Window'
  elif win_type == 5:
    window = np.blackman(length)
    win_str += 'Blackman Window'
  elif win_type == 6:
    window = np.kaiser(length, beta)
    win_str += 'Kaiser Window'
  else:
    writeLog(_log, 'WARNING: No windowing function selected!')
  return window, win_str