"""Provide support for linking an external transaction manager with Zope's"""
import transaction


class VTM:
    """Mix-in class that provides transaction management support

    A sub class should call self._register() whenever it performs any
    transaction-dependent operations (e.g. sql statements).

    The sub class will need to override _finish, to finalize work,
    _abort, to roll-back work, and perhaps _begin, if any work is
    needed at the start of a transaction.

    A subclass that uses locking during transaction commit must
    defined a sortKey() method.

    The VTM variety can be mixed-in with persistent classes.
    """

    _v_registered = 0
    _v_finalize = 0

    def _begin(self):
        pass

    def registered(self):
        return self._v_registered

    def _register(self):
        if not self._v_registered:
            try:
                transaction.get().register(Surrogate(self))
                self._begin()
                self._v_registered = 1
                self._v_finalize = 0
            except:
                pass

    def tpc_begin(self, *ignored):
        pass

    commit = tpc_begin

    def _finish(self):
        raise NotImplementedError

    def _abort(self):
        raise NotImplementedError

    def tpc_vote(self, *ignored):
        self._v_finalize = 1

    def tpc_finish(self, *ignored):
        if self._v_finalize:
            try:
                self._finish()
            finally:
                self._v_registered = 0
                self._v_finalize = 0

    def abort(self, *ignored):
        try:
            self._abort()
        finally:
            self._v_registered = 0
            self._v_finalize = 0

    tpc_abort = abort

    def sortKey(self, *ignored):
        """ The sortKey method is used for recent ZODB compatibility which
            needs to have a known commit order for lock acquisition.  Most
            DA's talking to RDBMS systems do not care about commit order, so
            return the constant 1
        """
        return 10


class Surrogate:

    def __init__(self, db):
        self._p_jar = db
        self.__inform_commit__ = db.tpc_finish
        self.__inform_abort__ = db.tpc_abort
