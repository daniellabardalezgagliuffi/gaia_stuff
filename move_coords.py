def crossmatch(tmassra, tmassdec, tmassepoch, year, gaiara, gaiadec, gaiaepoch, pmra, pmdec):

    '''Check which one of the several gaia coordinates matches 
    the input 2mass coordinate. tmass coordinates will be repeated
    for each gaia match.
    '''
    from astropy import units as u
    from astropy.time import Time
    from Python.routines import jdutil   
    from astropy.coordinates import SkyCoord

    if isinstance(gaiara,float):
        nrows = 1
    else:
        nrows = len(gaiara)

    df = pd.DataFrame(index=np.arange(nrows),columns=['tmass_ra',
                      'tmass_dec','tmass_epoch','gaia_ra','gaia_dec',
                      'gaia_epoch','pmra','pmdec'])
    df['tmass_ra'] = tmassra
    df['tmass_dec'] = tmassdec
    df['tmass_epoch'] = tmassepoch
    #df['tmass_year'] = df['tmass_epoch'].map(lambda x: jdutil.jd_to_date(x)[0])
    df['tmass_year'] = year
    df['gaia_ra'] = gaiara
    df['gaia_dec'] = gaiadec
    df['gaia_epoch'] = gaiaepoch
    df['pmra'] = pmra
    df['pmdec'] = pmdec
    print('hey!')
    df['backwards_gaia_ra'] = df['gaia_ra'] + (df['tmass_year']-df['gaia_epoch'])*(1./3600000.)/np.cos(df['gaia_dec']/180.*np.pi)*df['pmra']
    df['backwards_gaia_dec'] = df['gaia_dec'] + (df['tmass_year']-df['gaia_epoch'])*(1./3600000.)*df['pmdec']
    print('got my coords!')
    backwardsgaia = SkyCoord(ra=df['backwards_gaia_ra'].values*u.deg,dec=df['backwards_gaia_dec'].values*u.deg)
    tmassoriginal = SkyCoord(ra=df['tmass_ra'].values*u.deg,dec=df['tmass_dec'].values*u.deg)
    print('got my skycoords!')
    df['separation'] = backwardsgaia.separation(tmassoriginal)
    print('done!')
    return df