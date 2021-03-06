# R_t-uniformprior

This Python code calculates the effective reproduction number R_t from the daily infection data. I followed the methods of the paper https://academic.oup.com/aje/article/178/9/1505/89262 .

For each day, the R_t is assumed to be constant for the week ending in that day, and for each candidate value of R_t the likelihood is calculated based on the uniform prior distribution and the Gamma distrubtion for infectiveness (see below). 

In the present setting, the infection data are the numbers of symptomatic patients of COVID-19 in Italy based on the dates of sympton onset, available at https://www.epicentro.iss.it/coronavirus/sars-cov-2-dashboard .
The data are contained in sympdatadl.csv downloaded by the script download-iss.py .

For the Poisson distrubtion of infectiveness, we use the Gamma distribution used by the Italian national health institute (Istituto Superiore di Sanità), as explained in https://www.iss.it/primo-piano/-/asset_publisher/o4oGR9qmvUz9/content/id/5477037 .
