# Recommendation system for movie

## Data_set
- first column : user_id
- second column : movie_id
- third column : rating
- user_id, movie_id must be integer and rating can be real number(integer is recommended)


## Usage

``` 
$ python MF.py [data_set_name] [data_size]
```

### parsing args
- **[data_set_name]** : data set file name (contains file extention)
- **[data_size]** : number of rows to take from data set file

### example
```
$ python MF.py ratings.csv 1000
```
- It means that "takes 1000 rows from ratings.csv file"
