def move_coords(tmassra, tmassdec, tmassepoch, gaiara, gaiadec, gaiaepoch, pmra, pmdec):

    '''Check which one of the several gaia coordinates matches 
    the input 2mass coordinate. tmass coordinates will be repeated
    for each gaia match.
    
    Need to download jdutil package:
    https://gist.github.com/jiffyclub/1294443
    that converts julian date to year
    
    All inputs are np.arrays or pd.Series. Shape of arrays are: repeated 2MASS coordinates on tmassra, tmassdec for as many Gaia matches per 2MASS coordinate
    
    tmassra, tmassdec, gaiara, gaiadec =  2MASS and Gaia coordinates in degrees
    tmassepoch = 2MASS epoch in julian date - as downloaded straight from Vizier
    gaiaepoch = 2015.5 for DR2 and 2015.0 for DR1
    pmra, pmdec = proper motions in RA and Dec in mas/yr

    '''
    
    import pandas as pd
    import numpy as np
    from astropy import units as u
    from astropy.time import Time
    import jdutil
    from astropy.coordinates import SkyCoord
    from astropy import units as u

    if isinstance(gaiara,float):
        nrows = 1
    else:
        nrows = len(gaiara)

    df = pd.DataFrame(index=np.arange(nrows),columns=['tmass_ra','tmass_dec','tmass_epoch',
                                                      'gaia_ra','gaia_dec','gaia_epoch','pmra','pmdec'])
    df['tmass_ra'] = tmassra
    df['tmass_dec'] = tmassdec
    df['tmass_epoch'] = tmassepoch
    df['tmass_year'] = df['tmass_epoch'].map(lambda x: jdutil.jd_to_date(x)[0])
    df['gaia_ra'] = gaiara
    df['gaia_dec'] = gaiadec
    df['gaia_epoch'] = gaiaepoch
    df['pmra'] = pmra
    df['pmdec'] = pmdec

    df['backwards_gaia_ra'] = df['gaia_ra'] + (df['tmass_year']-df['gaia_epoch'])*(1./3600000.)/np.cos(df['gaia_dec']/180.*np.pi)*df['pmra']
    df['backwards_gaia_dec'] = df['gaia_dec'] + (df['tmass_year']-df['gaia_epoch'])*(1./3600000.)*df['pmdec']

    backwardsgaia = SkyCoord(ra=df['backwards_gaia_ra'].values*u.deg,dec=df['backwards_gaia_dec'].values*u.deg)
    tmassoriginal = SkyCoord(ra=df['tmass_ra'].values*u.deg,dec=df['tmass_dec'].values*u.deg)

    df['separation'] = backwardsgaia.separation(tmassoriginal)

    return df
