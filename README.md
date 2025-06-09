# Daniel Mishler Python data collector

A generalized script designed to gather robust performance
data in an automated manner.

Designed and used by Daniel Mishler beginning from 2023.
Its main purpose is to allow for the collection of data
following specific error bounds. For example, it is
capable of collecting multiple elements of data in
some given application and persisting at collecting
the data until the gaussian error of each attribute
collected is less than, say, 3%. You can then access
the mean and standard error for easy plotting afterward.

I have no intentions of commercializing this - it's just
fooling around with Python. If anyone finds use in
wading through my code, I welcome them to use it.
