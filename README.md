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
- **[data_set_name]** : ratings.csv (contains file extention)
- **[data_size]** : 1000 (must be integer)

### example
```
$ python MF.py ratings.csv 1000
```
- It means that takes 1000 rows from ratings.csv file
