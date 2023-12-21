# command: python first_analyzer.py /path_of_rootfile/name_of_rootfile.root /path_of_rootfile/output_name.root
# Takes the rootfile as input and computes the defined variables and fills the respective histograms.

import sys
import numpy as np
import ROOT
from array import array

###########################################################################

try:
  input = raw_input
except:
  pass

if len(sys.argv) < 3:
  print(" To use the code type: python first_analyzer.py /path/delphes_file.root /path/output.root")
  sys.exit(1)

ROOT.gSystem.Load("libDelphes")

try:
        ROOT.gInterpreter.Declare('#include "classes/DelphesClasses.h"')
        ROOT.gInterpreter.Declare('#include "external/ExRootAnalysis/ExRootTreeReader.h"')
except:
        pass

# Parameters
M_PI = 3.14
############################################

inputFile = sys.argv[1]
print("Input file :")
print(inputFile)

outputFile = sys.argv[2]
print("output file :")
print(outputFile)

# Create chain of root trees
chain = ROOT.TChain("Delphes")
chain.Add(inputFile)

# Create object of class ExRootTreeReader
treeReader = ROOT.ExRootTreeReader(chain)
numberOfEntries = treeReader.GetEntries()

# Getting the required branches from Delphes ROOT file.
branchJet = treeReader.UseBranch("Jet")
branchPtcl = treeReader.UseBranch("Particle")

# Book histograms
Nbins = 800
histJet = ROOT.TH1F("Lxy1_tau50", "Tau Decay", Nbins, 0, 100) # shift so we have the jets at two

print('will analyse ', numberOfEntries, ' entries')

for entry in range(0, numberOfEntries):
  treeReader.ReadEntry(entry)
  #supposedly shows the amount of jets
  njets = branchJet.GetEntries()

  #print(njets)
  #histJet.Fill(njets)
  for iptcl in range(branchPtcl.GetEntries()):
      if branchPtcl.At(iptcl).PID == 9990016:           
         D1pos = branchPtcl.At(iptcl).D1
         D2pos = D1pos+1
         D3pos = branchPtcl.At(iptcl).D2

         #PIDs of Daughters
         D1PID = branchPtcl.At(D1pos).PID
         D2PID = branchPtcl.At(D2pos).PID
         D3PID = branchPtcl.At(D3pos).PID

         #Coordinates of Daughters
         D1x = branchPtcl.At(D1pos).X
         D1y = branchPtcl.At(D1pos).Y

         D2x = branchPtcl.At(D2pos).X
         D2y = branchPtcl.At(D2pos).Y

         D3x = branchPtcl.At(D3pos).X
         D3y = branchPtcl.At(D3pos).Y
         #print('D1', D1x, D1y, 'D2', D2x, D2y, 'D3', D3x, D3y)
         #print(D1PID,D2PID,D3PID)
         '''
         I found out that D3, sometimes D2, is mostly the Tauon by typing
         if D1PID == 15:
         print('Daughter1 is a Tauon')
         and so on
         '''
         if abs(D1PID) == 15:
            #histJet.Fill(D1PID)
            d1pos = branchPtcl.At(D1pos).D1
            d2pos = branchPtcl.At(D1pos).D2
            m1pos = branchPtcl.At(d1pos).M1
            m1PID = branchPtcl.At(m1pos).PID
            #print('D1',m1pos, m1PID, D1PID)
            #print('D1',branchJet.GetEntries())

            d1x = branchPtcl.At(d1pos).X
            d1y = branchPtcl.At(d1pos).Y
            L1xy = np.sqrt((d1x-D1x)**2+(d1y-D1y)**2)
            histJet.Fill(L1xy)


            if abs(d1pos-d2pos) == 1:
               #histJet.Fill(D1PID)
               d1PID = branchPtcl.At(d1pos).PID
               #d2PID = branchPtcl.At(d1pos+1).PID
               d3PID = branchPtcl.At(d2pos).PID
               histJet.Fill(d3PID)

               #more information out of pions
               if abs(d1PID) == 111:
                  Epion = branchPtcl.At(d1pos).E
                  Px = branchPtcl.At(d1pos).Px
                  Py = branchPtcl.At(d1pos).Py
                  m = branchPtcl.At(d1pos).Mass
                  m_trans = np.sqrt(m**2 + Px**2 + Py**2)
                  #histJet.Fill(m_trans)
               #elif abs(d2PID) == 111:
                    #Epion = branchPtcl.At(d1pos+1).E
                    #Px = branchPtcl.At(d1pos+1).Px
                    #Py = branchPtcl.At(d1pos+1).Py
                    #m = branchPtcl.At(d1pos+1).Mass
                    #m_trans = np.sqrt(m**2 + Px**2 + Py**2)
                    #histJet.Fill(m_trans)
               elif abs(d3PID) == 111:
                    Epion = branchPtcl.At(d2pos).E
                    Px = branchPtcl.At(d2pos).Px
                    Py = branchPtcl.At(d2pos).Py
                    m = branchPtcl.At(d2pos).Mass
                    m_trans = np.sqrt(m**2 + Px**2 + Py**2)
                    #histJet.Fill(m_trans)
               #print('D1', d1PID, d2PID, d3PID)
               #histJet.Fill(d3PID)
               #print('D1', d1pos, d2pos)
               #print('D1', d2pos-d1pos)
         elif abs(D2PID) == 15:
              #histJet.Fill(D2PID)
              d1pos = branchPtcl.At(D2pos).D1
              d2pos = branchPtcl.At(D2pos).D2

              m1pos = branchPtcl.At(d1pos).M1
              m1PID = branchPtcl.At(m1pos).PID
              #print('D2',branchJet.GetEntries())
              #print('D2', m1pos, m1PID, D2PID)
              #print('D2', d1pos,d2pos)
              #print('D3', d2pos - d1pos)

              d2x = branchPtcl.At(D2pos).X
              d2y = branchPtcl.At(D2pos).Y
              L2xy = np.sqrt((d2x-D2x)**2+(d2y-D2y)**2)
              #histJet.Fill(L2xy)

              if abs(d1pos-d2pos) == 1:
                 #histJet.Fill(D2PID)
                 d1PID = branchPtcl.At(d1pos).PID
                 #d2PID = branchPtcl.At(d1pos+1).PID
                 d3PID = branchPtcl.At(d2pos).PID
                 histJet.Fill(d3PID)
                 #info about pions
                 if abs(d1PID) == 111:
                    Epion = branchPtcl.At(d1pos).E
                    Px = branchPtcl.At(d1pos).Px
                    Py = branchPtcl.At(d1pos).Py
                    m = branchPtcl.At(d1pos).Mass
                    m_trans = np.sqrt(m**2 + Px**2 + Py**2)
                    #histJet.Fill(m_trans)
                 #elif abs(d2PID) == 111:
                      #Epion = branchPtcl.At(d1pos+1).E
                      #Px = branchPtcl.At(d1pos+1).Px
                      #Py = branchPtcl.At(d1pos+1).Py
                      #m = branchPtcl.At(d1pos+1).Mass
                      #m_trans = np.sqrt(m**2 + Px**2 + Py**2)
                      #histJet.Fill(mtrans)
                 elif abs(d3PID) == 111:
                      Epion = branchPtcl.At(d2pos).E
                      Px = branchPtcl.At(d2pos).Px
                      Py = branchPtcl.At(d2pos).Py
                      m = branchPtcl.At(d2pos).Mass
                      m_trans = np.sqrt(m**2 + Px**2 + Py**2)
                      #histJet.Fill(m_trans)

         elif abs(D3PID) == 15:
              #histJet.Fill(D3PID)
              d1pos = branchPtcl.At(D3pos).D1
              d2pos = branchPtcl.At(D3pos).D2

              m1pos = branchPtcl.At(d1pos).M1
              m1PID = branchPtcl.At(m1pos).PID
              #print('D3',branchJet.GetEntries())
              #print('D3', m1pos, m1PID, D3PID)

              #print('D3', d1pos,d2pos)
              #print('D3', d2pos - d1pos)
              d3x = branchPtcl.At(D3pos).X
              d3y = branchPtcl.At(D3pos).Y
              L3xy = np.sqrt((d3x-D3x)**2+(d3y-D3y)**2)
              #histJet.Fill(L3xy)

              if abs(d1pos-d2pos) == 1:
                 d1PID = branchPtcl.At(d1pos).PID
                 #d2PID = branchPtcl.At(d1pos+1).PID
                 d3PID = branchPtcl.At(d2pos).PID
                 #print('D3', d1PID, d2PID, d3PID)
                 histJet.Fill(d3PID)
                 #info about pions
                 if abs(d1PID) == 111:
                    Epion = branchPtcl.At(d1pos).E
                    Px = branchPtcl.At(d1pos).Px
                    Py = branchPtcl.At(d1pos).Py
                    m = branchPtcl.At(d1pos).Mass
                    m_trans = np.sqrt(m**2 + Px**2 + Py**2)
                    #histJet.Fill(m_trans)
                 #elif abs(d2PID) == 111:
                      #Epion = branchPtcl.At(d1pos+1).E
                      #Px = branchPtcl.At(d1pos+1).Px
                      #Py = branchPtcl.At(d1pos+1).Py
                      #m = branchPtcl.At(d1pos+1).Mass
                      #m_trans = np.sqrt(m**2 + Px**2 + Py**2)
                      #histJet.Fill(m_trans)
                 elif abs(d3PID) == 111:
                      Epion = branchPtcl.At(d2pos).E
                      Px = branchPtcl.At(d2pos).Px
                      Py = branchPtcl.At(d2pos).Py
                      m = branchPtcl.At(d2pos).Mass
                      m_trans = np.sqrt(m**2 + Px**2 + Py**2)
                      #histJet.Fill(m_trans)

         if branchJet.GetEntries() >0: #change the number: if you want jet1 -> >0, jet2 -> >1 and jet3 -> >2
            jet1 = branchJet.At(0)
            #jet2 = branchJet.At(1)
            #jet3 = branchJet.At(2)
            #transverse momentum
            pt1 = jet1.PT
            #pt2 = jet2.PT
            #pt3 = jet3.PT
            #print(jet1.PT)
            #calculating momentum
            eta1 = jet1.Eta
            #eta2 = jet2.Eta
            #eta3 = jet3.Eta
            p1 = pt1*np.cosh(eta1)
            #p2 = pt2*np.cosh(eta2)
            #p3 = pt3*np.cosh(eta3)

            #histJet.Fill(pt3)

         '''
         for jt in range(njet):
             pt = branchJet.At(jt).PT
             #print(pt)
             histJet.Fill(pt)
             print(njets)
             #calculating momentum
             eta = branchJet.At(jt).Eta
             p = pt*np.cosh(eta)
             #print(p)
             #histJet.Fill(p)
             #find daughters
         '''
         #references to generated particles
         #ptcl = branchJet.At(iptcl).Particles


# write histograms
histlist = ROOT.TList()
histlist.Add(histJet)

# write output file
rootFile = ROOT.TFile(outputFile, "RECREATE")
histlist.Write()
rootFile.Close()

