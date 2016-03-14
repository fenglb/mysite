Follow last blog about qNMR, now this blog shows the demo about how to quantitative analysis using NMR spectroscopic tools. Here, we quantified the content of the mixture included glycine and alanine...

##1. Introduction

You can referece the last post about what's qNMR. Here we will shows How's qNMR.

##2. Experimental

1H NMR experiments were carried out using Bruker 5mm CPBBO spectrometer operating at 600.13 MHz, 298K. The typical acquisition parameters optimized for qNMR were as follows: bruker pulse program `zg30`, acquisition time 2.73s, sweep width 12019.2 Hz, relaxation delay 10s( this parameter must be optimized, and more than five times the longest T1 ). 64k data points after 32 scans, and an exponential line-broadening function of 0.3 Hz applied to FID.

##3. Materials

59.21mg of Glycine ( Sangon Biotech, 99%) and 53.49mg of $\beta$-Alanine ( Sangon Biotech 98.5%) were accurately weighed by a Sartorius analytical balances with a readability 0.01 mg, and transferred into an 5mm NMR tube (Schott NMR sample tubes), with adding $D\_2O$ solvent( 99.9% purity with TMS).

##3. Results and Discussion

Figure 1. 1H NMR spectra of the mixture of Glycine and $\beta$-Alanine in $D\_2O$ solvent.
![qnmr_glycine](/media/BlogPost/images/qnmr_glycine_alanine_1.png)

Figure 2. 1H NMR spectra of Glycine NH2 with coupling C13 and $\beta$-Alanine CH2 with coupling.
![qnmr_glycine](/media/BlogPost/images/qnmr_glycine_alanine_2.png)

Table 1.

Name     |  Molar Weight | Num. Proton         | Purity  | W        | Intergral | S/N
---------|---------------|---------------------|---------|----------|-----------|--------
Glycine  | 75.07         |  2(NH2,3.56ppm)     | 0.99    | 59.21mg  |   100     | 92375
$\beta$-Alanine|89.09    |  2(CH2,3.18ppm)     | 0.985   | 53.40mg  |  75.3427  | 35340
$\beta$-Alanine|89.09    |  2(CH2,2.56ppm)     | 0.985   | 53.40mg  |  75.3822  | 67547

As qNMR's theory, the intensity of the 1H signal is directly proportional to the number of protons that give rise to the signal, as following:

$$
  \frac{number-of-proton-in-glycine-NH2}{number-of-proton-in-beta-Alanine-CH2} = 
  \frac{59.21mg/75.07}{53.40mg/89.09} \simeq \frac{100}{(75.3427+75.3822)/2}
$$

the bais is 1.1%.

Table 2. with C13 satillate

Name     | Integral
---------|---------
Glycine  |  100
$\beta$-Alanine|75.6207
$\beta$-Alanine|75.4550

the bais is 0.8%.

##4. Conclusion