import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv("medical_examination.csv", sep=",")

# Add 'overweight' column
df['overweight'] = 0
for i in range(0,len(df)):
    if df["weight"][i]/(((df["height"][i])/100)**2)>25:
        df["overweight"][i]=1
    else:
        df["overweight"][i]=0


# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
for i in range(0,len(df)):
    if df["cholesterol"][i]==1:
        df["cholesterol"][i]=0
        if df["gluc"][i]==1:
         df["gluc"][i]=0
        else:
         df["gluc"][i]=1    
    elif df["cholesterol"][i]!=1:
       df["cholesterol"][i]=1
       if df["gluc"][i]==1:
         df["gluc"][i]=0
       else:
         df["gluc"][i]=1  

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = df.reset_index().melt(id_vars=["cardio"],value_vars=['cholesterol','gluc', 'smoke', 'alco', 'active','overweight'])



    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat=pd.DataFrame(data=df_cat.value_counts(), columns=["total"]).sort_index().reset_index()

    # Draw the catplot with 'sns.catplot()'
    sns.catplot(data=df_cat, x="variable", y="total", hue="value", kind="bar",col="cardio")


    # Get the figure for the output
    fig = sns.catplot(data=df_cat, x="variable", y="total", hue="value", kind="bar",col="cardio")


    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df.loc[(df['ap_lo'] <= df['ap_hi'])&
                 (df['height'] >= df['height'].quantile(0.025))&
                 (df['height'] <= df['height'].quantile(0.975))&
                 (df['weight'] >= df['weight'].quantile(0.025))&
                 (df['weight'] <= df['weight'].quantile(0.975))]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))



    # Set up the matplotlib figure
    fig, ax = fig, ax = plt.subplots(figsize=(11, 9))

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corr, mask=mask, vmin=-0.16, vmax=0.3, center=0, annot=True, fmt=".1f", cbar_kws={"shrink": 0.5, 'ticks': [-0.08, 0.00, 0.08, 0.16, 0.24]})


    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
