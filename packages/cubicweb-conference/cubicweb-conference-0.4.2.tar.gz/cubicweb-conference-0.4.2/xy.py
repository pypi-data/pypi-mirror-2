from yams import xy

xy.register_prefix('http://xmlns.com/foaf/0.1/', 'foaf')
xy.register_prefix('http://swrc.ontoware.org/ontology', 'swrc')



xy.add_equivalence('Conference', 'swrc:ConferenceEvent')
xy.add_equivalence('CWUser login', 'foaf:name')
xy.add_equivalence('Talk', 'swrc:Paper')
xy.add_equivalence('Talk title', 'swrc:title')
xy.add_equivalence('Talk description', 'swrc:abstract')
xy.add_equivalence('Talk description', 'swrc:abstract')
xy.add_equivalence('Talk has_attachments', 'swrc:hasRelatedDocument')
xy.add_equivalence('Talk leads', 'swrc:author')
