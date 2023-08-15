# O-index
This project started in Neurohackademy, Seattle in August 2023 (http://neurohackademy.org/). The goal of this project is to create an automated interface where you can type a name, and be given an o-index.

* An o-index is a comrehensive rating of how open a scientist is. This mimics the h-index, but weights the scientist on if they have open source articles, share code, etc.

# Contributors (ABC order):
* Jennifer Jahncke 
* Emily Lecy  
* Tania Miramontes  
* Emily Pickup  

# The process behind creating the O-index:

## STEP 1: Find all papers contributed to by an author of interest
We start by placing an authors name into our application. This will then search said name on pubmed. The pubmed page for the author is then scraped for the PMIDs of each paper that they have contributed to.

## STEP 2: Classify text to find markers of openness  
Each paper an author is listed under is then scraped to determine how open source the paper is. Each paper is scraped for the following catagories:

   * data shared : is the data publically available 
   * code relevant : is code needed to analyze this data. If not, code sharing will not be counted against the score
   * preprint available : was a preprint distributed
   * data upon request : is the data publically shared
   * code shared : is code publically availbale 
   * code upon request : is the code available if asked 
   
If a predefined phrase for each catagory (see keywords.csv) is seen in the text, the catagory is given a binary value of 1.
   
## STEP 3: Calculate the O-index
The O index is calculated by  summing the total instances of openness, and  dividing by the total number of catagories. An O-index was created for each paper an author has contributed to, and averaged across papers to get a final O-index for an author. 

## STEP 4: Data visualization and meaning


## Future Directions: 
* Some papers do not have full text on Pubmed, but have links to other open access sites. In the future code should be modified to see this, and use the link to the full access paper, and scrape text there. 

* Add additional tools to check if stated shared data/code are real (e.g. check that the links work)

* Promote this new metric, and hope that it motivated scientists to be more open about their work!

## Special Cosiderations:
* Many people go thorugh the process of changing their first/last names thoughout their career. To address this, our application includes an option to search two names, and make an o-index out of papers from both those names. 

## DISCLAIMERS: Comparison of the O-index across fields
* The O-index is defined by an equation that weights variables of code and data openness. If code is not relevant to a paper, the o-index is calculated without coding varibales considered, resulting in larger o-indices being created. Thus, it is not recommended to compater O-indices across fields.

* There are cases where there are papers that are open access, but the full text cannot be found due to our current method of scraping using PMIDs. In that case, the O-index will claim that the full text is available, but not have a count toward additional factors. This may inflate the index for specific papers. 