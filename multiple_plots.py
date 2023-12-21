#testing if ROOT works
import ROOT

#filenames
filename0 = #enter filename0
#histogram name from previous code, it must match
histoname0 = 'Lxy11'
################
filename1 = 'enter filename1
histoname1 = 'Lxy21'
################
filename2 = 'enter filename2
histoname2 = 'Lxy31'

ROOT.gROOT.SetBatch(True)
c = ROOT.TCanvas("c","c",800,600)

#read root file
f0 = ROOT.TFile(filename0,"READ")
h0 = f0.Get(histoname0)
h0.Scale(1/h0.Integral())
#################
f1 = ROOT.TFile(filename1,"READ")
h1 = f1.Get(histoname1)
h1.Scale(1/h1.Integral())
#################
f2 = ROOT.TFile(filename2, "READ")
h2 = f2.Get(histoname2)
h2.Scale(1/h2.Integral())

#normalize histograms
#h0.Scale(1/h0.Integral())
#h1.Scale(1/h1.Integral())

#set the color
h0.SetLineColor(ROOT.kGreen)
h1.SetLineColor(ROOT.kRed)
h2.SetLineColor(ROOT.kBlue)

#set linewidth
h0.SetLineWidth(2)
h1.SetLineWidth(2)
h2.SetLineWidth(2)

#set axis title, latex can be used
h0.GetXaxis().SetTitle(r'L_{xy}/[mm]')
h0.GetYaxis().SetTitle("A.U.")

#switch off stats box
h0.SetStats(0)

#set label sizes 
h0.GetYaxis().SetLabelSize(0.05)
h0.GetYaxis().SetTitleSize(0.05)
h0.GetXaxis().SetLabelSize(0.05)
h0.GetYaxis().SetTitleSize(0.05)
h0.SetTitle("")

mean1 = h0.GetMean()
mean2 = h1.GetMean()
mean3 = h2.GetMean()

#legend
legend = ROOT.TLegend(0.65,0.7,0.85,0.85)
legend.AddEntry(h0,"D1, Mean: %.2f" % mean1)
legend.AddEntry(h1,"D2, Mean: %.2f" % mean2)
legend.AddEntry(h2,"D3, Mean: %.2f" % mean3)
legend.SetLineWidth(0)

#now you can draw the histogram, hist e is a drawing option 
h0.Draw('hist e')
h1.Draw('same hist e')
h2.Draw('same hist e')
legend.Draw('same hist e')

#set axis offsets (only needed for one histogram)
h0.GetXaxis().SetTitleOffset(1.4)
h0.GetYaxis().SetTitleOffset(1.4)
#set axis ranges
h0.GetXaxis().SetRangeUser(-1, 40)
h0.GetYaxis().SetRangeUser(1E-3, 1.3)

#set margins on canvas
c.SetRightMargin(0.09)
c.SetLeftMargin(0.15)
c.SetBottomMargin(0.15)

#write something on canvas

t1 = ROOT.TLatex(0.15, 0.92,"#bf{#sqrt{s} = 91.2 GeV}")
t1.SetNDC(ROOT.kTRUE)
t1.Draw()

#save the canvas
c.Print("%s.pdf"%(histoname0))
