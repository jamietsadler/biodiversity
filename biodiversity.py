#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# ## Load Data and Inspect

# In[2]:


observations = pd.read_csv("observations.csv")
observations.head()


# In[4]:


observations.shape


# In[6]:


species = pd.read_csv("species_info.csv")
species.head()


# In[7]:


species.shape


# In[8]:


observations.park_name.nunique()


# ## Step 2: Distributions

# In[17]:


oberservations_park = observations.groupby("park_name").sum().reset_index()
oberservations_park.head()


# In[21]:


ax = sns.barplot(data=oberservations_park, x="park_name", y="observations")
plt.title("Total No. of Observations Across National Parks")
ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")


# In[22]:


species.category.nunique()


# In[24]:


print(f"species shape: {species.shape}")
print(f"observations shape: {observations.shape}")


# In[29]:


species.groupby("category").size()


# In[30]:


print(f"number of conservation statuses:{species.conservation_status.nunique()}")
print(f"unique conservation statuses:{species.conservation_status.unique()}")


# In[31]:


species.fillna('No Intervention', inplace=True)
species.groupby("conservation_status").size()


# In[32]:


species.head()


# In[36]:


conservation_status = species[species.conservation_status != "No Intervention"].groupby(["category", "conservation_status"]).count().reset_index()
conservation_status.head()


# In[39]:


conservation_pivot = conservation_status.pivot(index="category", columns="conservation_status", values="common_names")
conservation_pivot.head()


# In[40]:


ax = conservation_pivot.plot(kind="bar", stacked=True)


# In[41]:


species['is_protected'] = species.conservation_status != 'No Intervention'


# In[42]:


species.head()


# In[61]:


category = species.groupby(["category", "is_protected"]).scientific_name.nunique().reset_index()    .pivot(index="category", columns="is_protected", values="scientific_name").reset_index()
category.columns = ['category', 'not_protected', 'protected']
category.head()


# In[71]:


category["percent_protected"] = np.around(100*category.protected/(category.protected+category.not_protected))
category.head(10)


# In[66]:


## Chi Contigency to deterrrmine if there is significatn diference between protection rates of different species


# In[68]:


from scipy.stats import chi2_contingency


# In[69]:


##Between Mammals and Fish
contingency1 = [[30, 146], [11, 115]]
chi2_contingency(contingency1)


# p -value above 0.05, not significant

# In[73]:


##Between mammals and reptiles
contingency2 = [[5, 73], [30, 146]]
chi2_contingency(contingency2)


# p-value is less than 0.05, showing mammals statistivally more likely to need protection than reptiles

# ## Analysis of bat species

# In[74]:


species['is_bat'] = species.common_names.str.contains(r"\bBat\b", regex = True)


# In[75]:


species.head(10)


# In[76]:


bats = species[species.is_bat]


# In[77]:


bats.head()


# In[78]:


bat_observations = bats.merge(observations)


# In[80]:


bat_observations.head(10)


# In[84]:


obs_by_park = bat_observations.groupby(["park_name", "is_protected"]).observations.sum().reset_index()


# In[85]:


obs_by_park


# In[97]:


plt.figure(figsize=(16, 4))
x = sns.barplot(data=obs_by_park, x="park_name", y="observations", hue="is_protected")
plt.xlabel("Park")
plt.ylabel("Observations")
plt.title("Observations of Bat Species in National Parks")
#plt.xticks(rotation=30)
ax.set_xticks(range(4))


# In[ ]:




