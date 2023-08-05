sync_schema_props_perms(('Ticket', 'type', 'String'))
rql('Set T type "enhancement" where T is Ticket, T type "story"')
commit()
