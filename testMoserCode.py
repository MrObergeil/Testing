# coding: utf-8

# # Run time

# ## Setup

# In[237]:


import os
import datetime

import numpy as np
import pandas as pd
import tensorflow as tf

from consumer import *

# # Daten laden

# in diesem Fall laden wir die Daten direkt aus der Excel Datei, aber das wir von euch ersetzt.

# In[238]:


xlsx_path = '/home/pmf/Sensordaten/PM10_MW1_Graz_2015-2019.xlsx'
df = pd.read_excel(xlsx_path)[2:]
#df.reset_index(inplace=True)
#df=df.astype('float')




# In[239]:


#df = df[10000:10048]   # 48 zufällig ausgewählte hintereinanderfolgende Daten -> 1 Tag
df = dfAll

print(df)