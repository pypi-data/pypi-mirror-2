###########################################################################################
10-scenario instances 
###########################################################################################

CPLEX 10.1 EF values after 2 days of CPU time (values reported in CMS paper):

1ef10   152701.58 (1.32% optimality gap) - proved optimal by CPLEX 12.1 (16 threads, 3200 seconds real wall-clock time).
2ef10   148531.92 (1.54% optimality gap)
3ef10   148781.07 (1.13% optimality gap)
4ef10   159805.00 (2.15% optimality gap)
5ef10   153352.16 (1.68% optimality gap)

Using CPLEX 11.2 and PH, on Sandia's sleipnir server. Times are wall-clock time.

No fixing of continuous variables (or waiting for their convergence), as the resulting EF MIP is solvable.
Slamming after iteration 100, but not really - we haven't defined variable slam priorities. Cycle breaking 
when length exceeds 30.

Quadratic run results:

runph --model-directory=models --instance-directory=XXXX --max-iterations=100 --rho-cfgfile=config/rhosetter1.0.cfg --enable-ww-extensions --ww-extension-cfgfile=config/XXX.cfg --solve-ef 

Immediate fixing results (with wwph-immediatefixing.cfg).

1ef10: 11m59s, solution=156611.92, 17 PH iterations
2ef10: 4m26s,  solution=149138.58, 9  PH iterations
3ef10: 7m2s,   solution=151230.45, 9  PH iterations
4ef10: 5m28s,  solution=161215.44, 12 PH iterations
5ef10: 4m20s,  solution=154286.86, 10 PH iterations

Fix lag = 10 (with wwph-fixlag10.cfg).

1ef10: 29m34s, solution=153542.68, 56 PH iterations
2ef10: Converges in 44 iterations. After solving remaining EF, objective=149048.82***OLD***
3ef10: 30m55s, solution=149973.90, 33 PH iterations
4ef10: Converges in 85 iterations. After solving remaining EF, objective=161147.9 - exhibits a lot of cycle-breaking.***OLD***
5ef10: Converges in 51 iterations. After solving remaining EF, objective=153279.42***OLD***

Fix lag = 20 (with wwph-fixlag20.cfg).

1ef10: Converges in 64 iterations.  After solving remaining EF, objective=153542.68***OLD***
2ef10: Converges in 110 iterations. After solving remaining EF, objective=149048.82***OLD***
3ef10: Converges in 67 iterations.  After solving remaining EF, objective=149973.9***OLD***
4ef10: ***FAILS TO CONVERGE - SLAMMING PRIORITIES ARE REQUIRED.***OLD***
5ef10: Converges in 81 iterations.  After solving remaining EF, objective=153279.42***OLD***

Linearized run results: 

--bounds-cfgfile=config/xboundsetter.cfg --linearize-nonbinary-penalty-terms=8

Immediate fixing results (with wwph-immediatefixing.cfg).

1ef10: 14m54s, solution=155385.4,  26 PH iterations
2ef10: 6m8s,   solution=150550.36, 10 PH iterations 
3ef10: 11m52s, solution=152887.93, 27 PH iterations
4ef10: 3m53s,  solution=161215.44, 7  PH iterations
5ef10: 4m48s,  solution=154286.86, 12 PH iterations 

###########################################################################################
50-scenario instances 
###########################################################################################

CPLEX 11.2 EF results:

1ef50: 
2ef50: 
3ef50:
4ef50: 
5ef50: 

Quadratic run results:

runph --model-directory=models --instance-directory=XXXX --max-iterations=100 --rho-cfgfile=config/rhosetter1.0.cfg --enable-ww-extensions --ww-extension-cfgfile=config/XXX.cfg --solve-ef 

Immediate fixing results (with wwph-immediatefixing.cfg).

1ef10: 372m51s, solution=161096.56, 54 PH iterations
2ef10: 
3ef10: 
4ef10: 
5ef10: 
