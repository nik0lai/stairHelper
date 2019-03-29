#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Class to run staircase procedure.



@author: Nicolas Sanchez-Fuenzalida
"""

# Modules ----------------


# Class definition --------


class staircase_helper:
    
    def __init__(self, dv0 = 1, conv_p = .75, stepsize = (3), reversals = [10]):
        
        # Save inputs
        s = self
        s.dv = dv0              # Initial value
        s.p = conv_p            # Converge on this probability
        s.reversals = reversals
        s.stepsize = stepsize   # Step size
                
        # Calculate stuff
        s.factor = s.p / (1 - s.p) # Calculate factor
        
        # Trackers
        s.dvs = []              # Track all dvs values
        s.dvs_on_rev = []       # Track dvs values on reversals
        s.trial_number = 0      # Trial counter
        s.revn = 0              # Reversal counter
        
        # Indicators
        s.staircase_over = False    # Is the staircase over?
        s.first_trial = True        # Is this the first trial?
        
        # Last ans trackers
        s.last_answers = [None, None, None, None]
        
    def new_trial(self, is_correct):
        s = self
        
        if not s.staircase_over:
            
            if not s.first_trial:
                
                # How many steps?


test_stair = staircase_helper(dv0 = 10, conv_p=.75, stepsize=3, reversals=10)






        