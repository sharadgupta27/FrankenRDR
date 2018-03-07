'''
  This python function reads a specified auxiliary data file associated with the
  Italian EDR products.
'''
#
# Import necessary libraries
#
import os
import struct

def readAuxFile(fname):
  """
    This function simply reads a specified auxiliary data file.
    Will return an empty array if the file is not found.
    Input:
      fname = path the the file (can be relative or absolute)
    Output:
      auxFile = Python file object (or blank array if file is not found)
  """
  #
  # Check if file exists
  #
  if os.path.isfile(fname):
    #
    # The file exists so open file
    #
    auxFile = open(fname, 'rb')
  else:
    print('{} not found. Please check path and try again'.format(fname))
    auxFile = []
  return auxFile

def readRow(_file, rowNum, rowLen=267):
  """
    Since the auxiliary data files are so large, this function will read in a
    a given row of data rather than the entire file
    Input:
      _file: Python file object or path the file
      rowNum: The row associated with the necessary data block (i.e. SHARAD pulse)
      rowLen (optional): The byte length of the row (for EDR Aux files this is 267 bytes.
    Output:
      auxData: Python dictionary containing the relevent information from one row of the
               auxiliary file.
  """
  if type(_file) is str:
    _file = open(_file, 'rb')
  #
  # Point to appropriate row within the binary data
  #
  _file.seek(rowNum*267)
  #
  # Each row is composed of 267 bytes
  #
  rawData = _file.read(267)
  #
  # Set up dictionary
  #
  auxData ={'SCET_BLOCK_WHOLE': struct.unpack(">I", rawData[0:4])[0],
            'SCET_BLOCK_WHOLE': struct.unpack(">H", rawData[4:6])[0],
            'EPHEMERIS_TIME': struct.unpack(">d", rawData[6:14])[0],
            'GEOMETRY_EPOCH': 'ERROR', 
            'SOLAR_LONGITUDE': struct.unpack(">d", rawData[37:45])[0],
            'ORBIT_NUMBER': struct.unpack(">i", rawData[45:49])[0],
            'X_MARS_SC_POSITION_VECTOR': struct.unpack(">d", rawData[49:57])[0],
            'Y_MARS_SC_POSITION_VECTOR': struct.unpack(">d", rawData[57:65])[0],
            'Z_MARS_SC_POSITION_VECTOR': struct.unpack(">d", rawData[65:73])[0],
            'SPACECRAFT_ALTITUDE': struct.unpack(">d", rawData[73:81])[0],
            'SUB_SC_EAST_LONGITUDE': struct.unpack(">d", rawData[81:89])[0],
            'SUB_SC_PLANETOCENTRIC_LATITUDE': struct.unpack(">d", rawData[89:97])[0],
            'SUB_SC_PLANETOGRAPHIC_LATITUDE': struct.unpack(">d", rawData[97:105])[0],
            'X_MARS_SC_VELOCITY_VECTOR': struct.unpack(">d", rawData[105:113])[0],
            'Y_MARS_SC_VELOCITY_VECTOR': struct.unpack(">d", rawData[113:121])[0],
            'Z_MARS_SC_VELOCITY_VECTOR': struct.unpack(">d", rawData[121:129])[0],
            'MARS_SC_RADIAL_VELOCITY': struct.unpack(">d", rawData[129:137])[0],
            'MARS_SC_TANGENTIAL_VELOCITY': struct.unpack(">d", rawData[137:145])[0],
            'LOCAL_TRUE_SOLAR_TIME': struct.unpack(">d", rawData[145:153])[0],
            'SOLAR_ZENITH_ANGLE': struct.unpack(">d", rawData[153:161])[0],
            'SC_PITCH_ANGLE': struct.unpack(">d", rawData[161:169])[0],
            'SC_YAW_ANGLE': struct.unpack(">d", rawData[169:177])[0],
            'SC_ROLL_ANGLE': struct.unpack(">d", rawData[177:185])[0],
            'MRO_SAMX_INNER_GIMBAL_ANGLE': struct.unpack(">d", rawData[185:193])[0],
            'MRO_SAMX_OUTER_GIMBAL_ANGLE': struct.unpack(">d", rawData[193:201])[0],
            'MRO_SAPX_INNER_GIMBAL_ANGLE': struct.unpack(">d", rawData[201:209])[0],
            'MRO_SAPX_OUTER_GIMBAL_ANGLE': struct.unpack(">d", rawData[209:217])[0],
            'MRO_HGA_INNER_GIMBAL_ANGLE': struct.unpack(">d", rawData[217:225])[0],
            'MRO_HGA_OUTER_GIMBAL_ANGLE': struct.unpack(">d", rawData[225:233])[0],
            'DES_TEMP': struct.unpack(">f", rawData[233:237])[0],
            'DES_5V': struct.unpack(">f", rawData[237:241])[0],
            'DES_12V': struct.unpack(">f", rawData[241:245])[0],
            'DES_2V5': struct.unpack(">f", rawData[245:249])[0],
            'RX_TEMP': struct.unpack(">f", rawData[249:253])[0],
            'TX_TEMP': struct.unpack(">f", rawData[253:257])[0],
            'TX_LEV': struct.unpack(">f", rawData[257:261])[0],
            'TX_CURR': struct.unpack(">f", rawData[261:265])[0],
            'CORRUPTED_DATA_FLAG': struct.unpack(">h", rawData[265:267])[0]
          }
  return auxData


def detCalibChirp(TxTemp, RxTemp):
  """
  This function determines the appropriate calibrated chirp file to use
  for range compression. This is solely based off the temperatures
  of the Tx and Rx.
  """
  calibRoot = '../calib/'
  calibName = 'reference_chirp'
  ext = '.dat'
  TxCalNames = ['m20tx', 'm15tx', 'm10tx', 'm05tx', 
                'p00tx', 'p20tx', 'p40tx', 'p60tx']
  RxCalNames = ['m20rx', 'p00rx', 'p20rx', 'p40rx', 'p60rx']
  #
  # Define vectors for Tx and Rx temps
  #
  Tx = [-20, -15, -10, -5, 0, 20, 40, 60]
  Rx = [-20, 0, 20, 40, 60]
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
  if not os.path.isfile(calChirpFile):
    calChirpFile = []
  return calChirpFile

def main():
  global auxFile
  fname = '../data/e_0168901_001_ss19_700_a_a.dat'
  fname = '../data/e_1601301_001_ss19_700_a_a.dat'
  rowNum = range(0, 10504) 
  auxFile = readAuxFile(fname)
  if auxFile != []:
    for _row in rowNum:
      AuxData = readRow(auxFile, _row) 
      print(AuxData['TX_TEMP'], AuxData['RX_TEMP'])
      detCalibChirp(AuxData['TX_TEMP'], AuxData['RX_TEMP'])
    return
  else:
    return

if __name__ == '__main__':
  main()
