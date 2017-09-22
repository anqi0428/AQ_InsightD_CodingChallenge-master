# Table of Contents

1. [Features Preview] (README.md# features-preview)
2. [Packages] (README.md#packages)
3. [Details of Implementation] (README.md#details-of-implementation)
4. [Repo directory structure] (README.md#repo-directory-structure)
5. [Optional Features Can Be Realized] (README.md#optional-features-can-be-realized)


## Features Preview

This is designed to avoid fraud transactions in real life. 
The processing efficiency for justifying the 4th-degree relationship is approximately 1k per minute. All can be finished in a blink.
For the file submitted, it includes functions to realize the required features, respectively detects whether there's existed 1-degree, 2-degree or 4-degree relationships between the two before they transfer money to each other.
Optional features can be embedded into the functions if carefully adjusted the data structure for "Graph", a class included in the file.

## Packages

The required packages can be imported using codes below:

* import numpy as np 
* import pandas as pd
* from collections import defaultdict

## Details of implementation

[Back to Table of Contents] (README.md#table-of-contents)

Carefully thinking through this coding challenge, it's not difficlut to figure out the essense of the problem is to find the shortest path between the users. Yet there's existed classic algorithms like BFS and Dijkstra, a unique algorithm is designed and implemented.

### Input

The oringial files from Insight Data are transfered into a acceptable new file for python. New input can be find in this repository. If original files are used, please follow the instruction in the code file.

### Output

THe code process each line in `new_stream_payment.txt`, which is pre-processed like the input file, and for each payment, there is a output a line containing one of two words, `trusted` or `unverified`. 

`trusted` means the two users involved in the transaction have previously paid one another (when implementing Feature 1) or are part of the "friends network" (when implementing Feature 2 and 3).

`unverified` means the two users have not previously been involved in a transaction (when implementing Feature 1) or are outside of the "friends network" (when implementing Features 2 and 3)

The output is written to a text file in the `paymo_output` directory. 

## Repo directory structure
[Back to Table of Contents] (README.md#table-of-contents)

Repo Structure:

	├── README.md 
	├── run.sh
	├── src
	│   └── antif_1st_final_ver.py
	|   └── antif_2nd_final_ver.py
	|   └── antif_4th_final_ver.py
	├── paymo_input
	│   └── batch_payment.txt
	|   └── stream_payment.txt
	├── paymo_output
	│   └── output1.txt
	|   └── output2.txt
	|   └── output3.txt
	└── insight_testsuite
	 	   ├── run_tests.sh
		   └── tests
	        	└── test-1-AQ
        		    ├── paymo_input
        		    │   └── batch_payment.txt
        		    │   └── stream_payment.txt
        		    └── paymo_output
        		        └── output1.txt
        		        └── output2.txt
        		        └── output3.txt
        		

## Optional Features Can Be Realized
[Back to Table of Contents] (README.md#table-of-contents)

Though only the required features are realized, there's still more can be done.
Adding distance features to class "Graph" and use the amount of former payment to update the distance, we can easily find out how strong the relationship between the two people. Then using a revised algorithm we can lower the probability of fraud.
Or, by stracting key words in comments, we can find how what these people usually get money for and hence allocate some parameter to denote the probability of these people involved in a fraud.
