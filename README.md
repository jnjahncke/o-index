# O-index
This project started in Neurohackademy, Seattle in August 2023 (http://neurohackademy.org/). The goal of this project is to create an automated interface where you can type a name, and be given an o-index.

* An o-index is a comrehensive rating of how open a scientist is. This mimics the h-index, but weights the scientist on if they have open source articles, share code, etc.

# Contributors (ABC order):
* Jennifer Jahncke 
* Emily Lecy  
* Tania Miramontes  
* Emily Pickup  

# The process behind creating the O-index

## STEP 1: Find all papers contributed to by an author of interest
We start by placing an authors name into our application. This will then search said name on pubmed. The pubmed page for the author is then scraped for the PMIDs of each paper that they have contributed to.

## STEP 2: Classify text to find markers of openness  
Each paper an author is listed under is then scraped to determine how open source the paper is. Each paper is scraped for the following catagories:

   ** data shared : is the data publically available 
   ** code relevant : is code needed to analyze this data. If not, code sharing will not be counted against the score
   ** preprint available : was a preprint distributed
   ** data upon request : is the data publically shared
   ** code shared : is code publically availbale 
   ** code upon request : is the code available if asked 
   
If a predefined phrase for each catagory (see keywords.csv) is seen in the text, the catagory is given a binary value of 1.
   
## STEP 3: Calculate the O-index
*

# DISCLAIMER: Comparison of the O-index across fields
*The O-index is defined by an equation that weights variables of code and data openness. If code is not relevant to a paper, the o-index is calculated without coding varibales considered, resulting in larger o-indices being created. Thus, it is not recommended to compater O-indices across fields.