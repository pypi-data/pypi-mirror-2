# repository specific stuff ####################################################

try:
    from cubicweb import server
except ImportError: # no server installation
    pass
else:

    options = (
        ('check-revision-interval',
         {'type' : 'int',
          'default': 5*60,
          'help': 'interval between checking of new revisions in repositories \
(default to 5 minutes).',
          'inputlevel': 2,
          'group': 'vcsfile',
          }),
        ('check-revision-commmit-every',
         {'type' : 'int',
          'default': 1,
          'help': 'after how much new imported revisions the transaction \
should be commited (default to 1, e.g. on each revision).',
          'inputlevel': 2,
          'group': 'vcsfile',
          }),
        ('import-revision-content',
         {'type' : 'yn',
          'default': True,
          'help': 'Import content of file touched by a revision. This may \
cause performance issue when scaling.',
          'inputlevel': 2,
          'group': 'vcsfile',
          }),
        )

