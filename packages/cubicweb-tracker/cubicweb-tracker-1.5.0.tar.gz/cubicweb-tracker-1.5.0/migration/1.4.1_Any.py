for v in rql('Any V, VP WHERE V is Version, '
             'V publication_date VP, V publication_date NULL, '
             'V in_state S, S name "published"').entities():
    v.set_attributes(publication_date=v.latest_trinfo().creation_date)
    print 'fixed publication date of', v.dc_long_title()
commit()
