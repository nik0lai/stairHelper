#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Class to run staircase procedure.



@author: Nicolas Sanchez-Fuenzalida
"""

# Modules ----------------


# Class definition --------


class staircase_helper:
    
    def __init__(self, dv0 = 1, conv_p = .75, stepsize = (3), reversals = [10],
                 stepdown_rule = 1):
        # Save space writing s instead of self
        s = self

        # Save inputs
        s.dv = dv0                      # Initial value
        s.p = conv_p                    # Converge on this probability
        s.reversals = reversals         # Number of reversals to run
        s.stepsize = stepsize           # Step size
        s.stepdown_rule = stepdown_rule # Corrects in a row before step down
                
        s.factor = s.p / (1 - s.p)      # Calculate adjustment factor
        
        # Trackers
        s.dvs = []                      # Track all dvs values
        s.dvs_on_rev = []               # Track dvs values on reversals
        s.trial_number = 0              # Trial counter
        s.revn = 0                      # Reversal counter
        
        # Indicators
        s.staircase_over = False        # Is the staircase over?
        s.first_trial = True            # Is this the first trial?
        
        # Last ans trackers
        s.last_answers = [None] * stepdown_rule
        s.previous_is_corect = None
        
    def new_trial(self, is_correct):
        # Save space writing s instead of self
        s = self

        # If staircase not over ------------
        if not s.staircase_over:
             s.trial_number += 1
             s.dvs.append(s.dv)
             s.last_answers = [is_correct] + s.last_answers[:-1]
            
             # If not first trial ------------
             if not s.first_trial:
                
                # Check if reversal ---------
                if is_correct != s.previous_is_corect:
                    s.revn  += 1
                    reversal = True
                else:
                    reversal = False
                
                # Save dv on reversal
                if reversal:
                    s.dvs_on_rev.append(s.dv)
                    
            # Update dv ----------------------
             if is_correct and (s.last_answers == [True] * s.stepdown_rule):
                 s.dv -= (s.stepsize / float(s.factor))
             else:
                 s.dv += s.stepsize

             # If max. number of reversals end staircase
             if s.revn >= s.reversals:
                 s.staircase_over = True
                 
             # First trial over
             s.first_trial = False
             # Update last correct/incorrect answer
             s.previous_is_corect = is_correct
     
    def get_treshold(self):
        # Save space writing s instead of self
        s = self
        # Return treshold only if staircase is over
        if s.staircase_over:
            return np.mean(s.dvs_on_rev)
        else:
            print '\n\nStaircase is not over yet.\n' 




test_stair = staircase_helper(dv0 = 10, conv_p=.75, stepsize=3, reversals=10)

is_correct = True



        