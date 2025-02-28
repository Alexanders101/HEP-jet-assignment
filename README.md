HEP jet assignment - Data preparation
===
[![ArXiv](https://img.shields.io/badge/arxiv-2010.09206-green)](https://arxiv.org/abs/2010.09206)
![Matplotlib](https://img.shields.io/badge/matplotlib-3.2.2-blue)
![Numpy](https://img.shields.io/badge/numpy-1.19.0-blue)
![h5py](https://img.shields.io/badge/h5py-3.1.0-blue)
![Pandas](https://img.shields.io/badge/pandas-1.0.5-blue)
![Uproot](https://img.shields.io/badge/uproot-3.11.7-blue)
![tqdm](https://img.shields.io/badge/tqdm-4.54.1-blue)
![llvmlite](https://img.shields.io/badge/llvmlite-0.37.0-blue)
![numba](https://img.shields.io/badge/numba-0.54.1-blue)
[![Docker image](https://img.shields.io/badge/Docker%20Image-stable-orange)](https://hub.docker.com/layers/109102354/davidho9717/centos/SVJsimulation-cdr/images/sha256-01f8a8f229cc71a4d68697a4cbb4fd36b38e3c02af6469b5afc16c0a3aaff586?context=explore)

## Abstract 
This is a repository for the jet assignment project using state-of-the-art Machine Learning method.

There is two main part in the repository, `madgraph` and `analysis_script`. The `madgraph` folder contains the configuration and auto-run script for generating Monte Carlo simulation data.

## Madgraph
In this project, we generate the data base on the follwing model.

1. Fully hadronic top decay[[link]](https://github.com/davidho27941/HEP-jet-assignment/tree/v2/madgraph/pptt_preparation):  
```p p > t t~ QED=0, (t > W+ b, W+ > j j), (t~ > w- b~, w- > j j )```  
2. Standard Model Higgs boson produced in association with top quarks[[link]](https://github.com/davidho27941/HEP-jet-assignment/tree/v2/madgraph/ppttH_preparation):  
```p p > t t~ h , (t > W+ b, W+ > j j), (t~ > w- b~, w- > j j ), (h > b b~ )```  
3. Four top production(fully hadronic decay)[[link]](https://github.com/davidho27941/HEP-jet-assignment/tree/v2/madgraph/four_top_preparation):  
```p p > t t~ t t~ QED=0, (t > W+ b, W+ > j j), (t~ > w- b~, w- > j j )```  
4. Semi-leptonic top decay[[link]](https://github.com/davidho27941/HEP-jet-assignment/tree/v2/madgraph/ttbar-semi-lep_preparation):  
```p p > t t~ QED=0, (t > W+ b, W+ > j j), (t~ > W- b~, W- > l- vl~)```  

## Analysis 

The script for analysis events can be found in this [folder](https://github.com/davidho27941/HEP-jet-assignment/tree/v2/analysis_script).

The supported analysis method in this repository is:
1. Delta R matching(truth matching)
2. Chi-square reconstruction(Only available for two models)
3. Cutflow
4. Gaussian fitting for finding $\sigma$ for reconstructed invariant mass. 

A full version can be found in [HackMD](https://hackmd.io/@davidho9713/SylPrl80D) page.

###### tags: `Particle Physics`, `Machine Learning`, `Top quark`, `Transformer`, `SPA-Net`, `SPAttER`

