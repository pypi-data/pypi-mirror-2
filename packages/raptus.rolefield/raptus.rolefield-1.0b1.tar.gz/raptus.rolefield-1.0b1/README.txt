Introduction
============

raptus.rolefield provides two archetypes fields which assign
local roles to one or multiple users.

Example
-------

::

    RoleField(
        name='editor',
        required=1,
        acquire=False,
        role='Editor',
        write_permission=DelegateEditorRole,
        vocabulary=SomeVocabularyProvidingUserIds,
        widget=SelectionWidget(
            label=_('label_editor', default=u'Editor'),
        ),
    ),
    MultiRoleField(
        name='reviewers',
        required=1,
        acquire=False,
        role='Reviewer',
        write_permission=DelegateReviewerRole,
        vocabulary=SomeVocabularyProvidingUserIds,
        widget=MultiSelectionWidget(
            label=_('label_reviewers', default=u'Rreviewers'),
        ),
    ),
