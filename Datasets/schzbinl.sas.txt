DATA  one; INFILE  'C:\mixdemo\schizx1.dat';
INPUT id imps79 imps79b imps79o int tx week sweek txswk ;

/* get rid of observations with missing values */
IF imps79 > -9;

PROC FORMAT;
     VALUE imps79b 0 = 'le mild' 1 = 'ge moderate';
     VALUE tx      0 = 'placebo' 1 = 'drug';

/* fixed-effects logistic regression model */
PROC LOGISTIC DESCENDING;
MODEL imps79b = tx sweek tx*sweek;


/* random intercept logistic regression via GLIMMIX */
PROC GLIMMIX DATA=one METHOD=QUAD(QPOINTS=21) NOCLPRINT;
CLASS id;
MODEL imps79b(DESC) = tx sweek tx*sweek / SOLUTION DIST=BINARY LINK=LOGIT;
RANDOM INTERCEPT / SUBJECT=id;
RUN;


/* random trend logistic regression via GLIMMIX */
PROC GLIMMIX DATA=one METHOD=QUAD(QPOINTS=11) NOCLPRINT;
CLASS id;
MODEL imps79b(DESC) = tx sweek tx*sweek / SOLUTION DIST=BINARY LINK=LOGIT;
RANDOM INTERCEPT sweek / SUBJECT=id TYPE=UN GCORR SOLUTION;
ODS LISTING EXCLUDE SOLUTIONR; ODS OUTPUT SOLUTIONR=ebest2;
RUN;

/* print out the estimated random effects */
PROC PRINT DATA=ebest2;
RUN;


/* random intercept logistic regression model via NLMIXED */
PROC NLMIXED DATA=one QPOINTS=21;
PARMS b0=3.70 b_tx=-.40 b_sweek=-1.11 b_txsweek=-.42 varu=1;
z = b0 + b_tx*tx + b_sweek*sweek + b_txsweek*tx*sweek + u;
IF (imps79b=1) THEN
  p = 1 / (1 + EXP(-z));
ELSE
  p = 1 - (1 / (1 + EXP(-z)));
ll = LOG(p);
MODEL imps79b ~ GENERAL(ll);
RANDOM u ~ NORMAL(0,varu) SUBJECT=id;
ESTIMATE 'icc' varu/( (((ATAN(1)*4)**2)/3) + varu);
RUN;


/* random trend logistic regression model via NLMIXED */
PROC NLMIXED DATA=one QPOINTS=11;
PARMS b0=5.39 b1=-.03 b2=-1.50 b3=-1.02 v0=4.48 c01=0 v1=1;
z = b0 + b1*tx + b2*sweek + b3*tx*sweek + u0 + u1*sweek;
IF (imps79b=1) THEN
  p = 1 / (1 + EXP(-z));
ELSE
  p = 1 - (1 / (1 + EXP(-z)));
ll = LOG(p);
MODEL imps79b ~ GENERAL(ll);
RANDOM u0 u1 ~ NORMAL([0,0], [v0,c01,v1]) SUBJECT=id OUT=ebest2b;
ESTIMATE 're corr' c01/SQRT(v0*v1);
RUN;

/* print out the estimated random effects */
PROC PRINT DATA=ebest2b;
RUN;



