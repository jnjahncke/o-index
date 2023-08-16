# O-index

This project started in Neurohackademy, Seattle in August 2023 (http://neurohackademy.org/). The goal of this project is to create an automated interface where you can type a name, and be given an o-index.

* An o-index is a comrehensive rating of how open a scientist is with their publications. This mimics the h-index, but weights the scientist on if they have open source articles, share code, etc.

# Contributors (ABC order):

* Jennifer Jahncke 
* Emily Lecy  
* Tania Miramontes  
* Emily Pickup  

# The process behind creating the O-index:

## STEP 1: Find all papers contributed to by an author of interest

We start by placing an authors name into our application. This will then search said name on pubmed. The pubmed page for the author is then scraped for the PMIDs of each paper that they have contributed to.

## STEP 2: Classify text to find markers of openness 

Each paper an author is listed under is then scraped to determine how open source the paper is. Each paper is scraped for the following catagories and subcatagories:

   * data : 
       * data shared: the data is publically available online
       * data requested: the data can be requested for use
   * code :
       * code shared: the code is publically available online
       * code requested: the code can be requested for use
   
If a predefined phrase for each catagory (see keywords.csv) is seen in the manuscript text, the catagory is given a binary value. Values were weighted based on openness, with shared data recieving a value of 1, and requested data recieving a value of 0.5.

If code is not relevant to the paper, the O-index calculation will detect this and add an NaN to the code column. This will allow it to not impact the final O-index score for a paper.
   
## STEP 3: Calculate the O-index

The O-index is calculated for each paper summing the total instances of openness, and dividing by the total number of catagories. O-indices across papers were averaged to obtain an O-index for a specific author.

## STEP 4: Data visualization and meaning
1) Overall O-index: An O-index for the author will be displayed at the top of the GUI. This number averages the O-index for all papers the author is associated with.

2) Manuscript table: This table will include the catagory scores and an O-index for each paper an author has published, along with the papers PMID and year of publication

3) Change in O-index over time: A plot of the O-index for given years of publications is shown for an author to see the change in their O-index across years.

## Future Directions:

* Some papers do not have full text on Pubmed, but have links to other open access sites. In the future code should be modified to see this, and use the link to the full access paper, and scrape text there. 

* Add additional tools to check if stated shared data/code are real (e.g. check that the links work)

* Promote this new metric, and hope that it motivated scientists to be more open about their work!

* Openness was determined based on keywords found in text; however, it is possible that specific wording in manuscripts that express openness did not match our keywords. To improve accuracy of the O-index the following is suggested
    * Add more keywords to limit errors in assessing openness
    * Create an expression in which words can be used within the same sentence and be counted toward the O-index
        * E.g : The phrase "if requested, data will be shared " does not match current key words (the closest keyword is "data will be shared upon request". An expression that looks for the words data and request could more accurately show openness.

## Special Cosiderations:

* Many people go thorugh the process of changing their first/last names thoughout their career. To address this, our application includes an option to search two names, and make an o-index out of papers from both those names. 

* If you are running the code locally, you will have to input your own api key. This will allow you to be identified by NCBI servers. Users can obtain an API key now from the Settings page of their NCBI account (to create an account, visit http://www.ncbi.nlm.nih.gov/account/).

## Disclaimers:

* The O-index is defined by an equation that weights variables of code and data openness. If code is not relevant to a paper, the o-index is calculated without coding varibales considered, resulting in larger o-indices being created. Thus, it is not recommended to compater O-indices across fields.

* There are cases where there are papers that are open access, but the full text cannot be found due to our current method of scraping using PMIDs. In that case, the O-index will claim that the full text is available, but not have a count toward additional factors. This may inflate the index for specific papers. 

