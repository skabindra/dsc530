#!/usr/bin/env python
# coding: utf-8

# # Examples and Exercises from Think Stats, 2nd Edition
# 
# http://thinkstats2.com
# 
# Copyright 2016 Allen B. Downey
# 
# MIT License: https://opensource.org/licenses/MIT
# 

# In[9]:


from __future__ import print_function, division

get_ipython().run_line_magic('matplotlib', 'inline')

import numpy as np

import nsfg
import first
import thinkstats2
import thinkplot


# Again, I'll load the NSFG pregnancy file and select live births:

# In[2]:


preg = nsfg.ReadFemPreg()
live = preg[preg.outcome == 1]


# Here's the histogram of birth weights:

# In[3]:


hist = thinkstats2.Hist(live.birthwgt_lb, label='birthwgt_lb')
thinkplot.Hist(hist)
thinkplot.Config(xlabel='Birth weight (pounds)', ylabel='Count')


# To normalize the distribution, we could divide through by the total count:

# In[4]:


n = hist.Total()
pmf = hist.Copy()
for x, freq in hist.Items():
    pmf[x] = freq / n


# The result is a Probability Mass Function (PMF).

# In[5]:


thinkplot.Hist(pmf)
thinkplot.Config(xlabel='Birth weight (pounds)', ylabel='PMF')


# More directly, we can create a Pmf object.

# In[6]:


pmf = thinkstats2.Pmf([1, 2, 2, 3, 5])
pmf


# `Pmf` provides `Prob`, which looks up a value and returns its probability:

# In[7]:


pmf.Prob(2)


# The bracket operator does the same thing.

# In[8]:


pmf[2]


# The `Incr` method adds to the probability associated with a given values.

# In[9]:


pmf.Incr(2, 0.2)
pmf[2]


# The `Mult` method multiplies the probability associated with a value.

# In[10]:


pmf.Mult(2, 0.5)
pmf[2]


# `Total` returns the total probability (which is no longer 1, because we changed one of the probabilities).

# In[11]:


pmf.Total()


# `Normalize` divides through by the total probability, making it 1 again.

# In[12]:


pmf.Normalize()
pmf.Total()


# Here's the PMF of pregnancy length for live births.

# In[13]:


pmf = thinkstats2.Pmf(live.prglngth, label='prglngth')


# Here's what it looks like plotted with `Hist`, which makes a bar graph.

# In[14]:


thinkplot.Hist(pmf)
thinkplot.Config(xlabel='Pregnancy length (weeks)', ylabel='Pmf')


# Here's what it looks like plotted with `Pmf`, which makes a step function.

# In[15]:


thinkplot.Pmf(pmf)
thinkplot.Config(xlabel='Pregnancy length (weeks)', ylabel='Pmf')


# We can use `MakeFrames` to return DataFrames for all live births, first babies, and others.

# In[16]:


live, firsts, others = first.MakeFrames()


# Here are the distributions of pregnancy length.

# In[17]:


first_pmf = thinkstats2.Pmf(firsts.prglngth, label='firsts')
other_pmf = thinkstats2.Pmf(others.prglngth, label='others')


# And here's the code that replicates one of the figures in the chapter.

# In[18]:


width=0.45
axis = [27, 46, 0, 0.6]
thinkplot.PrePlot(2, cols=2)
thinkplot.Hist(first_pmf, align='right', width=width)
thinkplot.Hist(other_pmf, align='left', width=width)
thinkplot.Config(xlabel='Pregnancy length(weeks)', ylabel='PMF', axis=axis)

thinkplot.PrePlot(2)
thinkplot.SubPlot(2)
thinkplot.Pmfs([first_pmf, other_pmf])
thinkplot.Config(xlabel='Pregnancy length(weeks)', axis=axis)


# Here's the code that generates a plot of the difference in probability (in percentage points) between first babies and others, for each week of pregnancy (showing only pregnancies considered "full term"). 

# In[19]:


weeks = range(35, 46)
diffs = []
for week in weeks:
    p1 = first_pmf.Prob(week)
    p2 = other_pmf.Prob(week)
    diff = 100 * (p1 - p2)
    diffs.append(diff)

thinkplot.Bar(weeks, diffs)
thinkplot.Config(xlabel='Pregnancy length(weeks)', ylabel='Difference (percentage points)')


# ### Biasing and unbiasing PMFs
# 
# Here's the example in the book showing operations we can perform with `Pmf` objects.
# 
# Suppose we have the following distribution of class sizes.

# In[20]:


d = { 7: 8, 12: 8, 17: 14, 22: 4, 
     27: 6, 32: 12, 37: 8, 42: 3, 47: 2 }

pmf = thinkstats2.Pmf(d, label='actual')


# This function computes the biased PMF we would get if we surveyed students and asked about the size of the classes they are in.

# In[10]:


def BiasPmf(pmf, label):
    new_pmf = pmf.Copy(label=label)

    for x, p in pmf.Items():
        new_pmf.Mult(x, x)
        
    new_pmf.Normalize()
    return new_pmf


# The following graph shows the difference between the actual and observed distributions.

# In[22]:


biased_pmf = BiasPmf(pmf, label='observed')
thinkplot.PrePlot(2)
thinkplot.Pmfs([pmf, biased_pmf])
thinkplot.Config(xlabel='Class size', ylabel='PMF')


# The observed mean is substantially higher than the actual.

# In[23]:


print('Actual mean', pmf.Mean())
print('Observed mean', biased_pmf.Mean())


# If we were only able to collect the biased sample, we could "unbias" it by applying the inverse operation.

# In[24]:


def UnbiasPmf(pmf, label=None):
    new_pmf = pmf.Copy(label=label)

    for x, p in pmf.Items():
        new_pmf[x] *= 1/x
        
    new_pmf.Normalize()
    return new_pmf


# We can unbias the biased PMF:

# In[25]:


unbiased = UnbiasPmf(biased_pmf, label='unbiased')
print('Unbiased mean', unbiased.Mean())


# And plot the two distributions to confirm they are the same.

# In[26]:


thinkplot.PrePlot(2)
thinkplot.Pmfs([pmf, unbiased])
thinkplot.Config(xlabel='Class size', ylabel='PMF')


# ### Pandas indexing
# 
# Here's an example of a small DataFrame.

# In[27]:


import numpy as np
import pandas
array = np.random.randn(4, 2)
df = pandas.DataFrame(array)
df


# We can specify column names when we create the DataFrame:

# In[28]:


columns = ['A', 'B']
df = pandas.DataFrame(array, columns=columns)
df


# We can also specify an index that contains labels for the rows.

# In[29]:


index = ['a', 'b', 'c', 'd']
df = pandas.DataFrame(array, columns=columns, index=index)
df


# Normal indexing selects columns.

# In[30]:


df['A']


# We can use the `loc` attribute to select rows.

# In[31]:


df.loc['a']


# If you don't want to use the row labels and prefer to access the rows using integer indices, you can use the `iloc` attribute:

# In[32]:


df.iloc[0]


# `loc` can also take a list of labels.

# In[33]:


indices = ['a', 'c']
df.loc[indices]


# If you provide a slice of labels, `DataFrame` uses it to select rows.

# In[34]:


df['a':'c']


# If you provide a slice of integers, `DataFrame` selects rows by integer index.

# In[35]:


df[0:2]


# But notice that one method includes the last elements of the slice and one does not.
# 
# In general, I recommend giving labels to the rows and names to the columns, and using them consistently.

# ## Exercises

# **Exercise:** Something like the class size paradox appears if you survey children and ask how many children are in their family. Families with many children are more likely to appear in your sample, and families with no children have no chance to be in the sample.
# 
# Use the NSFG respondent variable `numkdhh` to construct the actual distribution for the number of children under 18 in the respondents' households.
# 
# Now compute the biased distribution we would see if we surveyed the children and asked them how many children under 18 (including themselves) are in their household.
# 
# Plot the actual and biased distributions, and compute their means.

# In[5]:


resp = nsfg.ReadFemResp()


# In[6]:


pmf = thinkstats2.Pmf(resp.numkdhh, label='numkdhh')


# In[7]:


thinkplot.Pmf(pmf)
thinkplot.Config(xlabel='Number of children', ylabel='PMF')


# In[11]:


biased = BiasPmf(pmf, label='biased')


# In[12]:


thinkplot.PrePlot(2)
thinkplot.Pmfs([pmf, biased])
thinkplot.Config(xlabel='Number of children', ylabel='PMF')


# In[13]:


pmf.Mean()


# In[14]:


biased.Mean()







