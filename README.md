

# Problem Statement:

Create a mechanism to analyze past years H1B immigration data trends w.r.t visa application processing. 
1. TOP 10 OCCUPATIONS for visa applications that are CERTIFIED, along with the certified percentage for each occupation w.r.t to all certified occupations
2. Top 10 STATES for visa applications that are CERTIFIED, along with the certified percentage for each state w.r.t to all certified states

# Output 

The Program must create 2 output files:
* `top_10_occupations.txt`: Top 10 occupations for certified visa applications
* `top_10_states.txt`: Top 10 states for certified visa applications


Approach:
 I used Python and Python’s OrderedDict structure is the basic data structure used to solving this problem. Python’s DictWriter parses a csv file and produces a list of OrderedDicts which are sorted and grouped to produce the desired results. Using the list of ORderedDicts makes the code very  simple and readable for filtering, grouping as well as writing to file without having to modify/create a new data structure. 

Run instructions:

Python3 ./src/H1bStats.py ./input/<input_file_name> <cert_fieldname> <occupation_fieldname> <state_fieldname>

Examples:
Python3 ./src/H1bStats.py ./input/H1B_FY_2014.csv STATUS LCA_CASE_SOC_NAME LCA_CASE_WORKLOC1_STATE

python3 ./src/H1BStats.py ./input/h1b_input.csv CASE_STATUS SOC_NAME WORKSITE_STATE