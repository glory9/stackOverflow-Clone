# StackOverflow-Clone
I built a search engine on a 10 GB StackOverflow SQL Database

## Tools used
- Flask
- jQuery
- SQL Server Express
- Pyodbc
- HTML/CSS/JS

## How it works

### Database
* A copy of StackOverflow's SQL database up to 2010 was used in this project. 

### Modules
* `get_top_questions` returns the top matching questions based on given key words when called in the `main.py` script.
* The `SearchEngine` Module contains the definition for the `get_top_questions` method as well as other helper functions that make up the logic used in extracting matching questions from the sql database.

### Searching Logic
* When a search query string is received from the frontend, it is parsed and the generated key words are passed to the `SearchEngine` Module.
* The `SearchEngine` module extracts a list of matching question IDs for each keyword. For each key word, a HashMap which maps question IDs to the number of times the question with the corresponding ID contains any of the keywords is updated. 
* After all matching IDs have been compiled, top 10 IDs with the most matches are then extracted using a max heap (to optimize sorting runtime) and returned

### Optimizing the search
* While working on the project, I realized the SQL server response was really slow. To optimize the search time, I limited maximum the number of keywords searched to 6. 
* Also, while parsing the search query string, words with less than 3 characters are filtered out as they will have a lower chance of affecting the search results and can potentially slow down the search request if included.
