"""
    Run move_coords.py first. Resulting df is the input.
    Input is a df with the following columns:
    INDEX = same for a group of Gaia matches to one 2MASS coordinate
    tmass_ra, tmass_dec, gaia_ra, gaia_dec, backwards_gaia_ra, backwards_gaia_dec = coordinates in degrees. backwards_gaia_ra, backwards_gaia_dec result from the move_coords.py code.
    separation = between original 2MASS coordinate and "backtracked" Gaia coordinates to the 2MASS epoch, in arcsec.
    Short Name = name of the source as hhmm+ddmm
    """

def plot_coords(count,subdf):
    
    import numpy as np
    import pandas as pd
    from tqdm import tqdm
    import matplotlib.pyplot as plt
    import seaborn as sns
    import matplotlib
    matplotlib.rc('xtick', labelsize=16)
    matplotlib.rc('ytick', labelsize=16)
    font = {'size'   : 16}
    matplotlib.rc('font', **font)
    from matplotlib import rc
    font = {'family' : 'serif',
        'serif':[],
        'weight' : 'bold',
            'size'   : 16}
    rc('font', **font)
    rc('text', usetex=True)
    sns.set_style('white')
    from numpy import ma
    
    fig = plt.figure(figsize=((9,6)))
    plt.plot(subdf['tmass_ra'],subdf['tmass_dec'],'*',markersize=25)
    plt.plot(subdf['backwards_gaia_ra'],subdf['backwards_gaia_dec'],'o',markersize=15)
    plt.plot(subdf['gaia_ra'],subdf['gaia_dec'],'o',markersize=10)
    for i in subdf.index:
        if pd.notnull(subdf.loc[i,'backwards_gaia_ra']) == True:
            plt.annotate(subdf.index[i],xy=(subdf.loc[i,'backwards_gaia_ra'],subdf.loc[i,'backwards_gaia_dec']),xycoords='data',fontsize=16)
        else:
            plt.annotate(subdf.index[i],xy=(subdf.loc[i,'gaia_ra'],subdf.loc[i,'gaia_dec']),xycoords='data',fontsize=16)        
    plt.legend(['2MASS','Backwards 2MASS','Gaia'],fontsize=16)
    plt.xlabel('RA',fontsize=16)
    plt.ylabel('Dec',fontsize=16)
    plt.tight_layout()
    plt.savefig(folder+'coord_check'+str(count)+'_'+subdf.loc[0,'Short Name']+'.jpg')       #
    plt.pause(0.5)
    plt.close()

# This piece of code divides the full df into subdf grouped by the same INDEX, containing all the Gaia matches to one 2MASS coordinate pair.

df['best'] = np.nan
for i in tqdm(range(df['INDEX'].nunique())):
    subdf = df.groupby('INDEX').get_group(i).reset_index()
    if np.isnan(subdf['separation'].idxmin()) == False:
        df.loc[subdf['index'][subdf['separation'].idxmin()],'best'] = 1
        plot_coords(i,subdf)


