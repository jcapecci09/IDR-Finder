"""I've first decided to create a naive model 

Author: Jcapecci09
"""


# Amino acids with disorder promoting regions = 1
# Amino acids with order promoting regions = -1
# Amino acids not associated with either = 0 
scoring_matrix = {
    'A': 1,  'R': 1,  'N': -1, 'D': 0,  'C': -1,
    'Q': 1,  'E': 1,  'G': 1,  'H': 0,  'I': -1,
    'L': -1, 'K': 1,  'M': 0,  'F': -1, 'P': 1,
    'S': 1,  'T': 0,  'W': -1, 'Y': -1, 'V': -1
}

# 1. Parse sequences
# 2. sliding glass window: most 21 amino acids, but atleast 5 amino acids
# 3. When do we determine disordered region? 
# - Maybe we just go by residue for now? Let's create a really bad model
#     --> lets say for each amino acid we calculate its score and look at the next 7 amino acids
#     --> If we have 5 points we determine it as a disorered region
#     --> If the residue before was determine to be a disordered residue we carry over 3 points
#     --> Ex:
#           ARKPMKSEGFVMHDQTKESLN
#           A: 1 + 1 + 1 + 1 + 0 + 1 + 1 + 1 = 7 --> disordered
#           R: 3 + 1 + 1 + 1 + 0 + 1 + 1 + 1 + 1 = 12 --> disordered
#           K: 3 + 1 + 1 + 0 + 1 + 1 + 1 + 1 + -1 = 10 --> disordered
#           P: 3 + 1 + 0 + 1 + 1 + 1 + 1 + -1 + -1 =  6 --> disordered
#           M: 3 + 0 + 1 + 1 + 1 + 1 + -1 + -1 + 0 = 5 --> diordered
#           K: 3 + 1 + 1 + 1 + 1 + -1 + -1 + 0 + 0 = 5 --> disordered
#           S: 3 + 1 + 1 + 1 + -1 + -1 + 0 + 0 + 0 = 4 --> ordered    
# 4. Then we can iteravily go back over our answers and remove any disorered sequences that aren't 5-21 amino acids
# have to consider edge cases: end of sequence
# Maybe do a window instead? Look at 3 amino acids before and 3 after?