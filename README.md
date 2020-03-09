# AWGN-Channel-Performance-Analysis
A Python based android app that uses Kivy. 
Python 3.7 
Used Kivygarden to plot the graphs
Buildozer was used to generate the apk file. 
The app takes a number from the user which it then uses to generate a random bitstream. 
The bitstream has additive white gaussian noise added to it, and subsequently the bitstream is recovered from it. 
Comparing the original bistream with the recovered one, the number of bits in error are calculated. 
From the number of bits in error the BER is calculated and visually depicted on a semilog graph.
