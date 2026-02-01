### II. Lookup Agenda

# This program finds agenda sessions in the data you imported.

# To complete this task, you will need to:
# 1. Parse command line arguments to retrieve lookup conditions
# 2. Get the table records which match the lookup conditions provided
# 3. Print the resulting records onto the screen

# We should be able to run your program as follows:\
# `$> ./lookup_agenda.py column value`

# Where:
# * column can be one of `["date", "time_start", "time_end", "title", "location", "description", "speaker"]`
# * value is the expected value for that field

# For example, suppose I have the following data in my database: 
# | Title         | Location      | Description               | Type                      |
# | ------------- | ------------- | ------------------------- | ------------------------- |
# | Breakfast     | Lounge        | Fresh fruits and pastries | Session                   |
# | Hangout       | Beach         | Have fun                  | Subsession of Breakfast   |
# | Lunch         | Price Center  | Junk food                 | Session                   |
# | Dinner        | Mamma Linnas  | Italian handmade pasta    | Session                   |
# | Networking    | Lounge	    | Let's meet		        | Subsession of Dinner      |


# Then the expected behavior is as follows:
# ```
# $> ./lookup_agenda.py location lounge
# Breakfast       Lounge    	        Fresh fruits and pastries   Session	                    # Returned because the location is lounge 
# Hangout	        Beach	            Have fun		            Subsession of Breakfast     # Returned because the parent session location is lounge
# Networking      Lounge	            Let's meet   	   	        Subsession of Dinner        # Returned because the location is lounge
# ```

# Please note:
# * Your program should look for both sessions and subsessions
# * For all matched session, you should return all its corresponding subsessions
# * We do not expect any specific output format as long as the results are distinguishable and all the information about that session is correct.
# * We are looking for an exact match for date, time_start, time_end, title, location and description.
# * For speaker, we will only pass one name at a time. We will expect all sessions where we can find this speaker, even though he may not be the only speaker.