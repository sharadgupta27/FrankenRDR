#
# Import necessary libraries
#
import numpy as np
import os, sys


def detChirpFiles(TxTemp, RxTemp, reorder=True, conj=True):
  """
  This function determines the appropriate calibrated chirp file to use
  for range compression and returns the decoded calibrated chirp.
  This is solely based off the temperatures of the TxTemp and RxTemp.
  """
  calibRoot = '../calib/'
  calibName = 'reference_chirp'
  ext = '.dat'
  TxCalNames = ['m20tx', 'm15tx', 'm10tx', 'm05tx',
                'p00tx', 'p20tx', 'p40tx', 'p60tx']
  RxCalNames = ['m20rx', 'p00rx', 'p20rx', 'p40rx',
                'p60rx']
  #
  # Define vectors for Tx and Rx temps
  #
  Tx = [-20, -15, -10, -5, 0, 20, 40, 60]
  Rx = [-20, 0, 20, 40, 60]
  calibChirpFiles = []
  TxDiff = []
  RxDiff = []
  #
  # Find distance
  #
  TxDiff[:] = [abs(x - TxTemp) for x in Tx]
  RxDiff[:] = [abs(x - RxTemp) for x in Rx]
  #
  # Find the indices of the closest Tx and Rx value
  #
  calibTx = TxCalNames[TxDiff.index(min(TxDiff))]
  calibRx = RxCalNames[RxDiff.index(min(RxDiff))]
  #
  # Construct File name
  #
  calChirpFile = calibRoot + calibName + '_' + \
                 TxCalNames[TxDiff.index(min(TxDiff))] + '_' + \
                 RxCalNames[RxDiff.index(min(RxDiff))] + ext
  if os.path.isfile(calChirpFile):
    calChirp = np.fromfile(calChirpFile, dtype='<f')
    calChirp = calChirp[:2048] + 1j*calChirp[2048:]
    if conj:
      calChirp = np.conj(calChirp)
    return calChirp
  else:
    print('Calibrated chirp file not found...exiting.')
    sys.exit()


def chirpCompression(sci, calChirp, window, fil_type='Match'):
  """
    This function performs the chirp compression on a single SHARAD record
    Inputs:
      sci - decompressed science data
      calChirp - Complex conjugate of the cal. chirp spectrum
      fil_type  - Match or Inverse
  """
  Fc = (80/3 - 20)                                      # MHz
  dt = 3/80                                             # Microseconds
  t = np.arange(0,4096*dt, dt)                          # Time vector
  C = np.exp(2*np.pi*1j*Fc*t)                           # Complex exponential
  #
  # Check length of the science data
  #
  if len(sci) != 4096:
    echoes = np.zeros(4096, complex)
    echoes[:len(sci)] = sci
  echoes = echoes * C
  #
  # Compute the FFT
  #
  ecSpec = np.fft.fft(echoes)
  #
  # Shift the data into ascending frequency order
  #
  ecSpec = np.fft.fftshift(ecSpec)
  #
  # Take central 2048 samples
  #
  ecSpec = ecSpec[1024:3072]
  #
  # Perform Chirp compression
  #
  if fil_type == 'Match':
    temp = window * calChirp * ecSpec
  elif fil_type == "Inverse":
    temp = window * (ecSpec / calChirp)
  temp2 = np.fft.ifftshift(temp)
  decomp = np.fft.ifft(temp2)
  return decomp