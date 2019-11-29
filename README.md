# Seam Carving Content-Aware Image Resizing

## Introduction

This project implements the Seam Carving method from [Shai Avidan et al.](https://perso.crans.org/frenoy/matlab2012/seamcarving.pdf). It is only a class project so We only implemented a one-dimensional width reducing SeamCarver.

## Background

Effective image resizing should consider not only geometry but also image content, i.e., content-aware image resizing. [Seam carving](https://perso.crans.org/frenoy/matlab2012/seamcarving.pdf)  is a simple method, which builds on Hidden Markov Model (HMM), to achieve this. It resizes an image by successively deleting or duplicating a vertical/horizontal seam with lowest energy. In implementation, the optimal seam can be tracked using Viterbi algorithm. 

## Algorithm

See the [report](https://github.com/XudongOliverShen/SeamCarver/blob/master/Report.pdf).

## Usage

Firstly clone the project from this repo.

To reduce the width of an image to 100 pixels, use following command

```python
python main.py -i input_image.jpg -o output_image.jpg -w 100
```

## Example results

Gradually reducing the width, you will expect to the these output images.

![avatar](https://github.com/XudongOliverShen/SeamCarver/blob/master/images/example1.png)

The first 30 seams to be deleted are marked red in the original image for a simple illustration.

![avatar](https://github.com/XudongOliverShen/SeamCarver/blob/master/images/seams_30.jpg)

## Contributors

5. Xudong Shen (xudong.shen@u.nus.edu)
2. Ruixi Chen (ruixi@u.nus.edu)
