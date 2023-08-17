# O-index: 

You can calculate your O-index online at https://tinyurl.com/3ens93fz - yay!

This project started in Neurohackademy, Seattle in August 2023 (http://neurohackademy.org/). The goal of this project is to create an automated interface where you can type an author name, and be given an o-index. 

* An o-index is a comrehensive rating of how open a scientist is with their publications. This index is created by weighing openness of both data, code, and manuscript availability.

This project was initially inspired by a past project, the O-factor: https://github.com/srcole/o-factor, which gives journals an openness factor, in attempt to inspire open access initiatives.

# Contributors (ABC order):

* Jennifer Jahncke 
* Emily Lecy  
* Tania Miramontes  
* Emily Pickup  

# The process behind creating the O-index:

## STEP 1: Find all papers contributed to by an author of interest:

We start by placing an authors name into our application. This name will be searched on pubmed, and the citations related to said author will be scraped for pubmed IDs.

## STEP 2: Classify text to find markers of openness:

Each paper an author is listed under is then scraped to determine how open source the paper is. Each paper is scraped for the following catagories and subcatagories:

   * data : 
       * data shared: the data is publically available online
       * data requested: the data can be requested for use
   * code :
       * code shared: the code is publically available online
       * code requested: the code can be requested for use
   * full text availability :
       * is the text publically avaiable, or does it have pay barriers
       
If a predefined phrase for each catagory (see keywords.csv) is seen in the manuscript text, the catagory is given a binary value. Values were weighted based on openness, with publically shared data/code recieving a value of 1, and requested data/code recieving a value of 0.5. If code is not relevant to a paper, the category will recieve a NaN scoring, and will not be counted toward the final O-score of that paper.

Papers that are not open and papers that are open but do not have a PMCID, and are therefore unable to be scraped, will recieve NaNs for both code and data sharing sections. 
   
## STEP 3: Calculate the O-index:

An O-score is calculated for each paper summing the total instances of openness, and dividing by the total number of catagories. O-score across papers were averaged to obtain an O-index for a specific author.

## STEP 4: Data visualization and meaning:
1) Overall O-index: An O-index for the author will be displayed at the top of the GUI. This number averages the O-score for all papers the author is associated with. An O-index can range between 0 and 1, with higher numbers showing an author is more 'open'.

2) Manuscript table: This table will include the catagory scores and an O-score for each paper an author has published, along with the papers PMID and year of publication.

3) Change in O-score over time: A plot of the average O-score for given years of publications are shown for an author to see the change in their O-score across years. Error bars are present for years in which more than one paper were published.

## Future Directions:

* Some papers do not have full text on Pubmed, but have links to other open access sites. In the future code should be modified to see this, and use the link to the full access paper, and scrape text there. 

* Add additional tools to check if stated shared data/code are real (e.g. check that the links work)

* Promote this new metric, and hope that it motivated scientists to be more open about their work!

* Openness was determined based on keywords found in text; however, it is possible that specific wording in manuscripts that express openness did not match our keywords. To improve accuracy of the O-index the following is suggested:
    * Add more keywords to limit errors in assessing openness
    * Create an expression in which words can be used within the same sentence and be counted toward the O-index
        * E.g : The phrase "if requested, data will be shared " does not match current key words (the closest keyword is "data will be shared upon request"). An expression that looks for the words data and request in the same sentence could more accurately show the openness of a paper.

## Special Considerations:

* If you are running the code locally, you will have to input your own api key. This will allow you to be identified by NCBI servers. Users can obtain an API key now from the Settings page of their NCBI account (to create an account, visit http://www.ncbi.nlm.nih.gov/account/).

## Disclaimers:

* The O-index is defined by an equation that weights variables of code and data openness for an authors published work. If code is not relevant to a paper, the o-index is calculated without coding varibales considered, resulting in differently weighted o-indices being created. Thus, it is not recommended to compare O-indices across fields.

* There are cases where there are papers that are open access, but the full text cannot be found due to our current method of scraping using PMIDs. In that case, the O-index will claim that the full text is available, but not have a count toward additional factors. This may inflate the index for specific papers. 