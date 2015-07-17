# -*- coding: utf-8 -*-
Theta = exp.get_theta()

# Increment overall count
Theta['n'] = Theta.get('n', 1) + 1
exp.set_theta(Theta)

