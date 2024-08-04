#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os 
from pyairtable import Api



# In[ ]:


print(os.environ.get('AIRTABLE_TOKEN'))


# In[8]:


class Book_review:
    def __init__(self):
        self.API_key = Api(os.environ.get('AIRTABLE_TOKEN'))
        self.table = self.API_key.table('appuxTXD1DJAMZ9lP', 'tbl7MLun8q8cqt6N5')

    def get_book_rating (self, sort="ASC", max_records=10):
        if not sort:
            return self.table.all(max_records=max_records)
        elif sort == "ASC":
            rating = ["Rating"]
        elif sort == "DESC":
            rating = ["-Rating"]
        table = self.table.all(sort=rating, max_records=max_records)
        return table

    def add_book_rating(self, book_title, book_rating, note=None):
        fields = {'Book': book_title, 'Rating': book_rating, 'Notes':note}
        self.table.create(fields=fields)




# In[9]:


if __name__=="__main__":
    br = Book_review()
    print(br.get_book_rating(sort="DESC", max_records=2))
    


# In[5]:


if __name__=="__main__":
    br = Book_review()
    br.add_book_rating("Investing 101", 5.0, "Just something you can find on the internet")
    print(br.API_key)
    


# In[ ]:




