#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Helper class to run staircase. This is a modification of Sam Mathias' 
Kaernbach's (1991) adaptive staircase procedure 
(https://gist.github.com/sammosummo/71bcde28572937380785).

Now it's possible to use any step down rule and to export of the 
staircase data.

BE AWARE,  although you can aim to virtually any accuracy percentage, 
the final accuracy rate depends largely on the dv initial value, the 
step size, the number of reversals and the step-down rule.

The script is working with the following library:
- Python         2.7.15 (packaged by conda-forge)
- numpy          1.15.4
- matplotlib     2.2.3

@author: Nicolas Sanchez-Fuenzalida
"""

# Modules ----------------
import numpy as np
import matplotlib.pyplot as plt

# Set class --------
class staircaseHelper:
    
    # Initialize staircase
    def __init__(self, dv0 = 1, conv_p = .75, stepsize = 3, reversals = 20,
                 stepdown_rule = 1, min_corr = None, max_corr = None):
        # Save space writing s instead of self
        s = self

        # Save inputs
        s.dv = dv0                      # Initial value
        s.p = conv_p                    # Converge on this probability
        s.reversals = reversals         # Number of reversals to run
        s.stepsize = stepsize           # Step size
        s.stepdown_rule = stepdown_rule # Corrects in a row before step down
        s.factor = s.p / (1 - s.p)      # Calculate adjustment factor
        
        # Min max corr
        # Check min and max values feeded
        if isinstance(min_corr, (int, float)) and isinstance(max_corr, (int, float)):
            if not min_corr < max_corr:
                raise Exception('max_corr has to be greater than min_corr. %d is not greater than %d.' % (max_corr, min_corr))
        
        # Min value correction. Activate if min_corr is a number
        if isinstance(min_corr, (int, float)):
            s.corr_min = True
            s.min_edge = min_corr
        else:
            s.corr_min = False
            s.min_edge = min_corr
        
        # Max value correction. Activate if min_corr is a number
        if isinstance(max_corr, (int, float)):
            s.corr_max = True
            s.max_edge = max_corr
        else:
            s.corr_max = False
            s.max_edge = max_corr

        # Trackers
        s.dvs = []                      # Track all dvs values
        s.dvs_on_rev = []               # Track dvs values on reversals
        s.trial_number = 0              # Trial counter
        s.revn = 0                      # Reversal counter
        s.reversal_on_trial = []        # Reversal trial
        s.is_correct_track = []         # Track corr/incorr booleans
        # Indicators
        s.staircase_over = False        # Is the staircase over?
        s.first_trial = True            # Is this the first trial?
        
        # Last ans trackers
        s.last_answers = [None] * stepdown_rule
        s.previous_is_corect = None
        
    # Advance trial (boolean)
    def new_trial(self, is_correct):
        # Save space writing s instead of self
        s = self

        # If staircase not over ------------
        if not s.staircase_over:
             s.trial_number += 1
             s.dvs.append(s.dv)
             s.last_answers = [is_correct] + s.last_answers[:-1]
             s.is_correct_track.append(is_correct)
            
             # If not first trial ------------
             if not s.first_trial:
                
                # Check if reversal ---------
                if is_correct != s.previous_is_corect:
                    s.revn  += 1
                    reversal = True
                    s.reversal_on_trial.append(s.trial_number)
                else:
                    reversal = False
                
                # Save dv on reversal
                if reversal:
                    s.dvs_on_rev.append(s.dv)
                    
            # Update dv ----------------------
             if is_correct:
                 # Correct, decrease signal
                 if (s.last_answers == [True] * s.stepdown_rule):
                     s.dv -= (s.stepsize / float(s.factor))
             else:
                 # Incorrect, increase signal
                 s.dv += s.stepsize
             # If prevent from going lower than min
             if s.corr_min:
                 s.dv = s.min_edge if (s.dv < s.min_edge) else s.dv
             # If prevent from going higher than max
             if s.corr_max:
                 s.dv = s.max_edge if (s.dv > s.max_edge) else s.dv
             # If max. number of reversals end staircase
             if s.revn >= s.reversals:
                 s.staircase_over = True
                 
             # First trial over
             s.first_trial = False
             # Update last correct/incorrect answer
             s.previous_is_corect = is_correct
    
    # Only when staircase is over (max. number of reversals reached), get
    # staircased treshold
    def get_treshold(self):
        # Save space writing s instead of self
        s = self
        # Return treshold only if staircase is over
        if s.staircase_over:
            return np.mean(s.dvs_on_rev)
        else:
            print '\n\nStaircase is not over yet.\n' 
    
    # Plot staircase evolution
    def plot_staircase(self, path = None):
        # Save space writing s instead of self
        s = self
        # Set number of trials as x axis and dv values on y axis
        x = np.arange(s.trial_number) + 1
        y = s.dvs
        # Plot
        plt.plot(x, y)
        plt.xlim(min(x), max(x))
        plt.ylim(min(y), max(y))
        plt.ylabel('Dv')
        plt.xlabel('Trial no.')
        
        if s.staircase_over:
            plt.hlines(s.get_treshold(), min(x), max(x), 'r')
        
        if not path:
            plt.show()
        else:
            plt.savefig(path)

    # Export staircase data (if no path feeded return array)
    def export_staircase(self, subNum = None, path = None):
        # Save space writing s instead of self
        s = self
        
        # Create vector indicating reversal on trials
        reversal_trials     = np.zeros(s.trial_number)
        s.reversal_on_trial = np.array(s.reversal_on_trial)-1
        reversal_trials[s.reversal_on_trial] = 1
        
        # Header for dataframe
        header = np.array(['sub_number', 'trial_no', 'dvs', 'reversal_trial', 'conv_p', 
                           'factor', 'reversals', 'stepsize', 'stepdown_rule', 'accuracy'])
        # Stack dataframe
        to_export = np.vstack(([subNum] * s.trial_number,
                               np.arange(s.trial_number) + 1, 
                               s.dvs,
                               reversal_trials,
                               [s.p] * s.trial_number,
                               [s.factor] * s.trial_number,
                               [s.reversals] * s.trial_number,
                               [s.stepsize] * s.trial_number,
                               [s.stepdown_rule] * s.trial_number,
                               [np.mean(s.is_correct_track)] * s.trial_number)).T
        # Add header                            
        to_export = np.vstack((np.array(header), to_export))
        
        if not path:
            return to_export
        else:
            np.savetxt(path, to_export, delimiter=",", fmt="%s")

# Define routine to test script. If the script is not imported but executed
# the folowwing routine will be executed.
def main():
    trials = np.random.randint(0, 2, 50)
    StaircaseHelper = staircaseHelper()
    for trial in trials:
        StaircaseHelper.new_trial(trial)
        if StaircaseHelper.staircase_over:
            break
    print 'Treshold: ' + str(StaircaseHelper.get_treshold())
    print StaircaseHelper.export_staircase()
    StaircaseHelper.plot_staircase()
# If script executed run main()
if __name__ == '__main__':
    main()