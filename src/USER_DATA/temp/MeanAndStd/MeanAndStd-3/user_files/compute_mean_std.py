# -*- coding: utf-8 -*-
# @Author: Elena Graverini
# @Date:   2015-06-27 13:34:57
# @Last Modified by:   Elena Graverini
# @Last Modified time: 2015-08-06 15:46:41


def read_from_file(filename):
    # This function is kindly provided to you.
    # Thank the assistants! :)
    my_distr = []
    with open(filename, 'rb') as f:
        for line in f:
            my_distr.append(float(line))
    return my_distr


def compute_mean(distr):
    # Write a function that returns the mean
    # of a given sample. The input is a data sample in list
    # format, and the output will be a number.
    # Replace "mean = 0." with the function body.
    mean = 0.
    return mean


def compute_std(distr):
    # Write a function that returns the standard deviation
    # of a given sample. The input is a data sample in list
    # format, and the output will be a number.
    # Replace "std = 0." with the function body.
    std = 0.
    return std


# After your studies, please write either "yes" or "no"
# in the following variable, in place of "answer".
# Please enclose the answer with quotation marks,
# as in the example:
compatible_with_RRLyrae = "answer"


if __name__ == '__main__':
    # You can use the "main" to test your code.
    # Code that follows the "if __name__ == '__main__':" snippet
    # is only executed when you execute this script with
    # "python compute_mean_std.py", and will not run when your
    # functions will be tested by us.
    # Example:
    # print compute_mean(my_distr)
    # print compute_std(my_distr)
    pass
