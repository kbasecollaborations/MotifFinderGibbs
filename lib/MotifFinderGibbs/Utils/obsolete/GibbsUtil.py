import sys
import os
import json

class GibbsUtil:
  def build_gibbs_command(inputFilePath, motifLen):
      if not os.path.exists('/kb/module/work/tmp/gibbs'):
         os.mkdir('/kb/module/work/tmp/gibbs')
      outputFilePath = '/kb/module/work/tmp/gibbs/gibbs_output_' + str(motifLen) +  '.txt'

      length = '8'
      command = 'Gibbs ' + inputFilePath + ' ' + str(motifLen) + ' -n > ' + outputFilePath
      return command

  def run_gibbs_command(command):
      os.system(command)

  def parse_gibbs_output(path):
      outputFileList = []
      for filename in os.listdir(path):
          outputFileList.append(path + '/' + filename)

      motifList = []
      for outputFilePath in outputFileList:
          gibbsFile = open(outputFilePath,'r')

          motifDict = {}
          pwmList = []
          processPWM = False
          processLoc = False
          gotSig = False
          motifIncluded = False

          #TODO: keeping p-value as -1 until I understand the output stats better
          motifDict['Locations'] = []
          for line in gibbsFile:
              if processLoc is True:
                  if '****' in line:
                      processLoc = False
                      gotSig = False
                      motifDict['p-value'] = -1.0
                      for m in motifList:
                          if motifDict['Iupac_signature'] == m['Iupac_signature']:
                              motifIncluded = True
                      if not motifIncluded:
                         motifList.append(motifDict)
                      motifDict = {}
                      motifDict['Locations'] = []
                      motifIncluded = False
                      pwmList = []
                  #add motif to list from here
                  elif 'Num Motifs' not in line:
                      elems = line.split()
                      if not gotSig:
                          motif = elems[4]
                          motifDict['Iupac_signature'] = motif
                          gotSig = True
                      locList = []
                      if len(line.split()) == 10:
                          locList.append(elems[9])
                          locList.append(elems[2])
                          locList.append(elems[6])
                          if elems[8] == 'F':
                              locList.append('+')
                          else:
                              locList.append('-')
                      elif len(line.split()) == 9:
                          locList.append(elems[8])
                          locList.append(elems[2])
                          locList.append(elems[5])
                          if elems[7] == 'F':
                              locList.append('+')
                          else:
                              locList.append('-')
                      motifDict['Locations'].append(locList)
              elif processPWM is True:
                  if 'Background' in line:
                      processPWM = False
                      motifDict['pwm'] = pwmList
                  elif '|' in line:
                      baseCount += 1
                      elems = line.split()
                      rowList = []
                      rowList.append(('A',float(elems[2])))
                      rowList.append(('C',float(elems[4])))
                      rowList.append(('G',float(elems[5])))
                      rowList.append(('T',float(elems[3])))
                      pwmList.append(rowList)
                  elif len(line.split()) == 0:
                      if baseCount < motifLength:
                          rowList = []
                          rowList.append(('A',.25))
                          rowList.append(('C',.25))
                          rowList.append(('G',.25))
                          rowList.append(('T',.25))
                          pwmList.append(rowList)



              elif 'columns' in line:
                  motifLength = int(line.split()[0])
                  processLoc = True
              elif 'Motif probability model' in line:
                  processPWM = True
                  baseCount = 0

      return motifList
