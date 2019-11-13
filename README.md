# sport-index-analysis

An analysis of all the sport indexes based on the sport linked datasets 

# Process
The `index_fetcher.py` script will download all the live sport datasets and extracts information about the sport topics which are the name and the `url` (`primaryTopicOf`) relationship and stores that information into a CSV file (`results.csv`). The repository already contains the datasets folder with all the sport live datasets.

The `cwork_fetcher.py` script will download the first page of CreativeWorks and store them into the cworks folder. Further processing of the files will include the extraction of the CreativeWorks categories and `modifiedDate` for each one of them. This information is added in the `results.csv` file. We expect maximum 20 creativeWorks per index (total number for each page in CreativeWorks API) so the final spreadsheet will contain the following information 

```
,,,index,,cw1_modifiedDate,cw1_category,...,cw20_modifiedDate,cw20_category
```

## Analysis
The `sport-creative-works-analysis.ipynb` has further analysis of the `results.csv` file. It can be rerun using Jupyter notebooks. 
Installation:
In the terminal run:
```
pip install jupyterlab
```

Then in the folder dir run

```
jupyter notebook
```
Browse to the `sport-creative-works-analysis.ipynb` to run the notebook. 