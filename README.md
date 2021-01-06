

#  [Data Engineering Project] Spoitfy Data Project 

<center><img src="https://user-images.githubusercontent.com/53164959/103773047-d0393700-506d-11eb-8b74-e1e158c55def.png" width="500" height="300"></center>

## :globe_with_meridians: Introduction 

The main motivation of this project is to experience a full cycle of so-called 'big data' environment. The biggest challenge for those with a strong background in Statistics and Math is to perform data analysis without any resort to data uploaded at Kaggle. In this project, we will go through a whole process of data training from scratch. 

This simple task can divide into two major sections, one of which is related to acquiring or crawling data directly from Spotify AP while the other is to perform data analysis on the collected information. 

## :globe_with_meridians: Sections

- Part 1: Collection of Data From Spotify API
  - Creating a database and tables for data storage
  - Choosing one of the two given formats; 
    - Pandas DataFrame (python3)
    - MySQL 

- Part 2: Build up Amazon Web Services RDS 
  - Connecting to a DB instance running the MySQL databse engine

- Part 3: Data Analysis 

## :globe_with_meridians: Special Notes

:pencil2:  _AWD RDS(Amazon Relational Database Service)_

In order to connect to Database instance, we need to first obtain an endpoint and port value from the AWS Management Console. 
Right after acquisition of the information, we are now able to connect to a DB instance using MySQL client by typing the below command line. 

```sql
mysql -h endpoint -P port_number -u masteruser -p
```

As for the detailed information on how to construct a database and create tables, see the folder called 

:pencil2: ER diagarm displaying tables and their relationhips 







  
