#from __future__ import with_statement # for < 2.6
import os
import re
from django.db import connections, transaction
from mercurial import cmdutil, hg, ui as ui_, match as match_
from mercurial.node import short
from mutations.conf import settings
from mutations.models import MutationLog
from os.path import join as pjoin


re_mutation_file = re.compile(r'^%s/(?P<db_alias>%s)/.*\.py$' % (
        settings.MUTATIONS_ROOT, '|'.join(settings.DATABASES.keys())))


def yesno(msg):
    ans = None
    while ans not in ['y', 'N']:
        if ans is not None:
            print 'Please enter y or N'
        ans = raw_input(msg)
    return ans == 'y'


class Evolution(object):
    """
    A class for executing mutations in a mercurial repository, updating to
    the revision when the file was added to the repository and executing the
    mutation in that revision.
    """
    def __init__(self, path=None, interactive=None, dry=False, alldone=False):
        self.interactive = interactive
        self.dry = dry
        self.alldone = alldone
        if path is None:
            path = cmdutil.findrepo(os.getcwd()) or ""
        ui = ui_.ui()
        self.repo = hg.repository(ui, path)
        # update to tip, pulling is up to the user
        hg.update(self.repo, None)

    def evolve(self):
        """
        Iterate through all revisions and look for mutations and execute
        them using self.mutate if they are not deleted afterwards.
        """
        opts = {'rev': ['0:-1']} # move forward
        pats = ['re:%s/(%s).*\.py' % (settings.MUTATIONS_ROOT,
                '|'.join(settings.DATABASES.keys()))]
        match = match_.match(self.repo.root, self.repo.getcwd(), pats)
        def prepare(ctx, fns):
            pass
        mutations = []
        mutations_dict = {}
        for ctx in cmdutil.walkchangerevs(self.repo, match, opts, prepare):
            changenode = ctx.node()
            added, removed = self.repo.status(
                    self.repo.changelog.parents(
                    changenode)[0], changenode)[1:3]
            for fn in added:
                m = re_mutation_file.match(fn)
                # We also need to check if the added file already is in
                # the mutations list since merges makes things a bit more
                # complicated for us.
                if m and fn not in mutations:
                    mutations.append(fn)
                    mutations_dict[fn] = {
                        'fn': fn,
                        'ctx': ctx,
                        'db_alias': m.group('db_alias'),
                    }
            for x in removed:
                if re_mutation_file.match(x):
                    # shouldn't need to test this, but if a file can be added
                    # several tims maybe it can be deleted several times too.
                    if x in mutations:
                        mutations.remove(x)
        for mutation in mutations:
            self.mutate(**mutations_dict[mutation])
        hg.update(self.repo, None)

    def mutate(self, ctx=None, fn=None, db_alias=None):
        """
        Execute a mutation script.
        """
        revision = short(ctx.node())
        changeset = "%s:%s" % (ctx.rev(), revision)
        mutation = '%s@%s' % (fn, revision)
        mutation_display = '%s@%s' % (fn, changeset)
        if self.alldone:
            MutationLog.objects.using(db_alias).get_or_create(mutation=mutation)
            print 'Marked %s as done.' % mutation_display
            return
        try:
            MutationLog.objects.using(db_alias).get(mutation=mutation)
        except MutationLog.DoesNotExist:
            if not self.interactive or \
                    yesno('Do you want to mutate: %s? y/N ' % mutation_display):
                print 'Updating to revision %s' % changeset
                hg.update(self.repo, ctx.rev())
                print 'Mutating %s' % mutation_display
                execfile(pjoin(self.repo.root, fn), {}, {
                    'cursor': connections[db_alias].cursor(),
                    'commit_unless_managed': transaction.commit_unless_managed,
                    'dry': self.dry,
                })
                if not self.dry:
                    MutationLog.objects.using(db_alias).get_or_create(
                            mutation=mutation)
            elif self.interactive:
                print 'Skipping %s' % mutation_display
                if yesno('Do you want to mark %s as done? y/N '
                        % mutation_display):
                    MutationLog.objects.using(db_alias).get_or_create(
                            mutation=mutation)

