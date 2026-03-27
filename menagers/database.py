# might reuse -> from pantry_wrapper import *

from dataclasses import dataclass
from sqlite3.dbapi2 import Connection
import os, json, time, functools, sqlite3, database_cache
from dotenv import load_dotenv
from functools import cache, lru_cache
from pathlib import Path


import psycopg


# Load password from .env file

load_dotenv()

# Get the connection string from the .env file
connection_string = os.getenv("password")

connection = psycopg.connect(connection_string)

cursor = connection.cursor()

def timer(func):
	@functools.wraps(func)  
	def wrapper(*args, **kwargs):
			t = time.time()
			
			result = func(*args, **kwargs) 
			print(func.__name__ + ": " + str(time.time() - t))
			return result 
	return wrapper
			

@timer
@lru_cache(maxsize=32)
def check_table(table, *content): # returns True if table exsits else creates the database

	cache = database_cache.check_cache(table)
	if cache[1]:
		return True
	else:
		

				# check if table exsits
				
				
			cursor.execute("""
				SELECT EXISTS (
				SELECT FROM information_schema.tables 
				WHERE table_name = """ + f"'{table}');")

			table_exsits = cursor.fetchone()[0]

			if not table_exsits: 

				print("database doesn't exist")
				
				# creating the table
				try: 
					print("creating the database")

					# if the table dosen't exist and the user gave data create a new table with the data
					if content:
						
						cursor.execute("""CREATE TABLE """ + f"{table} ({content[0]})")
						
					
				# if the creating faild print the error
				except Exception as e: 
					print(f"couldn't create the database: {e} ")

			# if the table exsits		
			else:
				return True



@timer
def get_table(table):
	
	cache = database_cache.check_cache(table)
	
	if cache[1]:
		return cache[0]
	else:
	
			if check_table(table):

				
					# get every user data
					cursor.execute(f"SELECT json_agg(t) FROM (SELECT * FROM {table} ORDER BY id LIMIT 3) t;")

					
					
					# cache the data
					database_cache.cache(table, cursor.fetchall())
			
					return(cursor.fetchall())

		
		


@timer
def get_player(table, player_id):

	# todo add a cache check here before going to the online database
	if check_table(table):
		
		cursor.execute(f"SELECT * FROM {table} WHERE id = {player_id};")
		return (cursor.fetchall())


def get_from_player(key, table, player_id):

		# todo add a cache check here before going to the online database
	if check_table(table):
		
		cursor.execute(f"SELECT {key} FROM {table} WHERE id = {player_id};")
		return (cursor.fetchall())



@timer
def add_player_data(key, value, player_id, table):
		
		# todo make the changes go to the cash so the datas will always be the same
		
		# do only if the table exists
		if check_table(table):
			
			cursor.execute(f"SELECT {key} FROM {table} WHERE id = {player_id}")
			original_value = cursor.fetchall()[0][0]

			
			# check for multiple data type cases
			# todo might need to add more cases here
			if isinstance(original_value, int):
				new_value = int(original_value) + int(value)
				
			elif isinstance(original_value, list):
				new_value = original_value.append(value)
			else:
				new_value = original_value + value
				
			cursor.execute(f"UPDATE users SET {key} = {str(new_value)} WHERE id = {str(player_id)};")



@timer
def update_player_data(key, value, player_id, table):

		# todo make the changes go to the cash so the datas will always be the same
		
	# check if table exsits 
	if check_table(table):

		# selecting the user id
		cursor.execute(f"SELECT * FROM {table} WHERE id = 199")

		# fetching the selected data, if its not empty means the user exsits else the user is not in the table
		result = cursor.fetchone()
	
		if result:
				
				# if the user exists updating the input value to input key
				
				cursor.execute(f"UPDATE {table} SET {key} = %s WHERE id = %s;", (str(value),str(player_id)))
				
		else:
				print("User not found")





get_table("users")
check_table("users")
add_player_data("cash", "10", "199", "users")

