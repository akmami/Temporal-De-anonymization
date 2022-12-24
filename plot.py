#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 12:49:06 2022

@author: akmami
"""

import matplotlib.pyplot as plt
import numpy as np

x = [0, 1, 2, 3, 4, 5, 6, 7]
t1t2 = [76.78, 80.32, 90.83, 83.7, 81.2, 88.2, 83.08, 83.44]
t2t3 = [27.18, 27.4, 26.38, 27.36, 23.7, 25.81, 24.47, 26.36]

plt.plot(x, t1t2, x, t2t3)
plt.ylabel('average distance')
plt.xlabel('distance threshold')
plt.show()