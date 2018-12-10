# turtleflying

I love you.

## Motivation

The idea comes up from some subjective complaint (or confusion) of gevent:

1. does gevent take advantages of timerfd and signalfd on Linux?
2. does gevent make use of self-pipe trick to greenify Queue?
3. does gevent conform to pep-3156?
4. is gevent too obtrusive as a nonblocking IO patching library?

To be clear, all above is about my subjective taste and poor judgement, so please shut up if you have comments.

## Rationale

### 1. Monkey patch is the only access.

That's to say, APIs provides by gevent as followed won't exist here:

* gevent.pool
* gevent.queue
* gevent.spawn
* gevent.timeout
* gevent.server (ridiculous...)

Concerns are understood, but any code other than `monkey.patch_all()` shall be smelly due to intensive coupling.
Some issues will be taken care later.

### 2. Make use of Linux kernel API as much as possible.

Linux kernel is masterpiece which exposes massive APIs to compose high proformance works, but community persist to be blind.

Following APIs will be used broadly:

* timerfd
* signalfd
* eventfd
* epoll

### 3. Self-pipe trick is solution to all other blocking IO.

This will cover:

* thread-safe queue
* join (real or greenified) thread

### 4. PEP 3156 is followed.

Though I doubt what BDFL promotes for general async IO resolution, asyncio, but PEP 3156 is indeed awesome and I'd be happy to be a zealot.

### 5. Greenlet is cornerstone.

Of course.
