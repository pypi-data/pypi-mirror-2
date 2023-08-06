import time
from twisted.internet import defer


class Job(object):
    """
    Hold the details of a job that is being, or will be, processed by a
    L{ResizableDispatchQueue}.

    All jobs start out in the PENDING state. Then either of the following
    will eventually happen:

      1. The job is launched. State is set to UNDERWAY.

      2. The job is cancelled (self.cancel is called) without being
         launched.  The state is then set to CANCELLED.

    Once a job is UNDERWAY, the following may happen:

      1. The function that launches the job hits an error of some
         kind. State goes to FAILED.

      2. The job completes cleanly. State goes to FINISHED.

      3. The job (or, equivalently, the deferred that will receive the
         result) is cancelled. State is set to CANCELLED.

    In rough ASCII art the possible job state transitions are:

                               ->  FAILED
                              /
      PENDING  -->  UNDERWAY  -->  FINISHED
         |                    \
         ----------------------->  CANCELLED


    @ivar jobarg: The argument that will be passed to the function that
    processes the job.

    @ivar priority: The priority for the job. Lower means more important.

    @ivar queuedTime: The time the job entered the queue.

    @ivar startTime: The time processing on the job starts.

    @ivar stopTime: The time job processing stops. Processing stops due to
    one of: clean completion (state = FINISHED), failure during the
    processing (state = FAILED), or job cancellation (state = CANCELLED).

    @ivar finishedDeferred: a C{Deferred} that will fire when the job
    finished, with the job function result.

    @ivar state: The current state of the job, as described above.
    """

    PENDING = 0
    UNDERWAY = 1
    FINISHED = 2
    FAILED = 3
    CANCELLED = 4

    def __init__(self, jobarg, priority):
        self.jobarg = jobarg
        self.priority = priority
        self.queuedTime = time.time()
        self.startTime = None
        self.stopTime = None
        self.state = self.PENDING
        self.waiting = []  # Deferreds waiting on the result of this job.

    def launch(self, func):
        """
        Begin operation on this job by passing its job argument to C{func}.
        The call to func is made via defer.maybeDeferred.  When the job
        finishes, its result will be passed on to self.finishedDeferred in
        self._finish below. Arrange to cancel the in-progress work if
        cancel is called on the C{Deferred} we return.

        @param func: the function to call on self.jobarg.

        @raise: C{RuntimeError} if the job is not in the PENDING state.

        @return: A C{Deferred} that will fire (with self) after running
        func on self.jobarg. The result of that call will be in
        self.result.
        """
        if self.state != self.PENDING:
            raise RuntimeError('You cannot launch a job that is not pending.')
        else:
            self.startTime = time.time()
            self.state = self.UNDERWAY
            self._underwayDeferred = defer.maybeDeferred(func, self.jobarg)
            self._underwayDeferred.addCallbacks(self._finished, self._failed)

    def _finished(self, result):
        """
        The job finished cleanly. Record its finishing time, change state,
        set self.result, and pass on the result (as self, a completed job).
        """
        assert self.state == self.UNDERWAY
        self.stopTime = time.time()
        self.state = self.FINISHED
        self.result = result
        for d in self.waiting:
            d.callback(self)
        self.waiting = []

    def _failed(self, failure):
        """
        The job failed in some way (including possibly being cancelled). If
        it wasn't cancelled, record its finishing time and errback all
        waiting watchers.  If the job was cancelled, its completion details
        have already been set (by self.cancel, below).
        """
        if self.state != self.CANCELLED:
            assert self.state == self.UNDERWAY
            self.stopTime = time.time()
            self.state = self.FAILED
            self.failure = failure
            for d in self.waiting:
                d.errback(self)
            self.waiting = []

    def cancel(self):
        """
        Cancel the job, record the cancellation time, cancel the underway
        deferred (if any). Errback all waiting watchers.

        @param deferred: The deferred that is being cancelled (i.e.,
        self._underwayDeferred). Ignored.
        """
        self.stopTime = time.time()
        if self.state == self.UNDERWAY:
            self.state = self.CANCELLED
            self._underwayDeferred.cancel()
        self.state = self.CANCELLED
        for d in self.waiting:
            d.errback(self)
        self.waiting = []

    def _cancelWatcher(self, ignoredDeferred):
        """
        A C{Deferred} returned by self.watch has been cancelled.  Cancel
        the job by calling the public self.cancel method.

        @param ignoredDeferred: The deferred whose cancel method was
        called. Ignored.
        """
        self.cancel()

    def watch(self):
        """
        Watch this job.

        @return: a C{Deferred} that fires with the job result or fails if
        it is cancelled or hits an error.
        """
        if self.state in (self.PENDING, self.UNDERWAY):
            d = defer.Deferred(self._cancelWatcher)
            self.waiting.append(d)
            return d
        elif self.state == self.FINISHED:
            return defer.succeed(self)
        else:
            return defer.fail(self)
