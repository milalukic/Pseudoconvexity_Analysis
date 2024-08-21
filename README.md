# Pseudoconvexity analysis of functions in Python

## Introduction
Probabilistic programs specify complicated probabilistic models in the form of computer programs. For instance, the program

1 𝑥 ~ uniform(0, 100)
2 𝑏 ~ normal(0.1∗𝑥+1, 1)
3 observe (𝑏, 6.29)

in lines 1-2 specifies a random variable x, sampled from the uniform distribution, and b sampled from the Gaussian distribution, where the mean is the function of the random variable x. Overall, probabilistic programs are a textual representation of probability distributions (in case of continuous variables, it is the density function; in the general case it is the cumulative distribution function). 

Probabilistic programs also enable automatic Bayesian inference, that for the initial (also called prior) distribution and subsequently computed data as evidence, updates the knowledge about the distribution, by computing the shape of the posterior distribution. For instance, one can use observe statement to specify these additional conditions. Writing “observe (b, 6.29)” before the return statement changes the distribution of the product, according to Bayes rule.
![image](https://github.com/user-attachments/assets/d3115dc6-4910-4e02-810b-18570d6d4661)

We recently developed AURA, a system for automatic inference in probabilistic programs using quantized reasoning. AURA computes precise sound bounds on the posterior distributions computed by probabilistic programs. In addition to computing bounds on a single posterior distribution, when data observations are fixed constants, AURA allows programmers to specify interval bounds on uncertainty of data observations. Then AURA can abstractly interpret an infinite set of posterior distributions and certify bounds on probabilistic queries over those distributions. The figures give an example of how AURA quantized the posterior distribution of the example program (a) and how it comptes the family of distributions if the observed data has perturbations, i.e., we consider the statement observe (b, 6.29 ± eps), where eps  ∈  [a,b].

AURA’s computation is guaranteed to be correct if the distributions in the program are psuedo-concave https://en.wikipedia.org/wiki/Pseudoconvex_function), a condition that is satisfied by many commonly used distributions, such as Gaussian, Beta, Gamma, etc. 

## Tasks
The goal of this project is to design and implement a technique for automatically identifying if a probabilistic program is pseudo-concave, by testing its underlying distribution function. 

There exist techniques for automatically testing if a given function (even defined on an interval domain) is pseudoconvex, e.g.:
Testing pseudoconvexity via interval computation;  https://link.springer.com/article/10.1007/s10898-017-0537-6 
Linear interval parametric approach to testing pseudoconvexity; https://link.springer.com/article/10.1007/s10898-020-00924-w 
