class job:
    def __init__(self, n, bt, at):
        # name
        self.name = n

        # turnaround time
        self.tat = 0

        # burst time
        self.bt = bt
        # time left
        self.tl = bt
        # wait time
        self.wt = 0

        # arrival time
        self.at = at

        # completion time
        self.ct = -1

        self.current = False

    def __str__(self):
        return str(f'Name:{self.name} TAT:{self.tat} BT:{self.bt} WT:{self.wt} AT:{self.at} CT:{self.ct}')

class rdq:
    def __init__(self):
        self.q = []

    def updatewaittime(self, time):
        for job in self.q:
            if job.ct == -1 and job.current is False:
                job.wt += time

    def addjob(self, j):
        self.q.append(j)

    def getjobs(self):
        return self.q

    def sortfcfs(self):
        self.q.sort(key=lambda x: x.at)

    def sortsjn(self):
        self.q.sort(key=lambda x: x.bt)

    def sortsrt(self):
        self.q.sort(key=lambda x: x.tl)

    def sortalph(self):
        self.q.sort(key=lambda x: x.name)

    def reset(self):
        for job in self.q:
            # turnaround time
            job.tat = 0
            # wait time
            job.wt = 0
            # completion time
            job.ct = -1
            # time left
            job.tl = job.bt


class main:
    def __init__(self):
        pass

    clock = 0
    currentjob = None
    queue = rdq()
    queue.addjob(job('A', 1, 5))
    queue.addjob(job('B', 5, 3))
    queue.addjob(job('C', 8, 14))
    queue.addjob(job('D', 26, 8))

    # fcfs
    print('FCFS')
    clock = 0
    queue.reset()
    queue.sortfcfs()
    for x in range(len(queue.getjobs())):
        currentjob = queue.getjobs()[x]
        clock += currentjob.bt
        currentjob.ct = clock
        currentjob.tat = currentjob.bt + currentjob.wt
        queue.getjobs()[x] = currentjob
        queue.updatewaittime(currentjob.bt)

    tottat = 0.0
    totwt = 0.0
    queue.sortalph()
    for job in queue.getjobs():
        tottat += job.tat
        totwt += job.wt
        print(job)

    tottat = tottat / len(queue.getjobs())
    totwt = totwt / len(queue.getjobs())

    print('FCFS Average TAT: ' + str(tottat))
    print('FCFS Average WT: ' + str(totwt))
    print()

    # sjn
    print('SJN')
    clock = 0
    queue.reset()
    queue.sortsjn()
    for x in range(len(queue.getjobs())):
        currentjob = queue.getjobs()[x]
        clock += currentjob.bt
        currentjob.ct = clock
        currentjob.tat = currentjob.bt + currentjob.wt
        queue.getjobs()[x] = currentjob
        queue.updatewaittime(currentjob.bt)

    tottat = 0.0
    totwt = 0.0
    queue.sortalph()
    for job in queue.getjobs():
        tottat += job.tat
        totwt += job.wt
        print(job)

    tottat = tottat / len(queue.getjobs())
    totwt = totwt / len(queue.getjobs())

    print('SJN Average TAT: ' + str(tottat))
    print('SJN Average WT: ' + str(totwt))
    print()

    # srt
    # until all jobs time left vars are 0
    queue.reset()
    currentjob = None
    clock = 0
    while True:
        new = False
        for job in queue.getjobs():
            if job.at == clock:
                if currentjob is not None:
                    if job.bt < currentjob.tl:
                        for j in queue.getjobs():
                            if j.name == currentjob.name:
                                j = currentjob
                                j.current = False
                        job.current = True
                        currentjob = job
                        # print('New Current Job: ' + str(currentjob))
                        new = True

                else:
                    job.current = True
                    currentjob = job
                    # print('New Current Job: ' + str(currentjob))
                    new = True

        if currentjob is not None and new is False:
            if currentjob.tl == 1:
                currentjob.tl = currentjob.tl - 1
                currentjob.ct = clock
                currentjob.tat = currentjob.bt + currentjob.wt
                currentjob.wt = currentjob.wt - currentjob.at
                for job in queue.getjobs():
                    if job.name == currentjob.name:
                        job = currentjob
                        job.current = False
                # print('Job Finished: ' + str(currentjob))
                queue.sortsrt()
                for job in queue.getjobs():
                    if job.tl != 0 and clock > job.at:
                        job.current = True
                        currentjob = job
                        # ('New Current Job: ' + str(currentjob))
                        break
            else:
                currentjob.tl = currentjob.tl - 1

        queue.updatewaittime(1)
        # print('Clock: ' + str(clock) + '\tCurrent Job: ' + str(currentjob))
        clock = clock + 1

        done = True
        for job in queue.getjobs():
            if job.tl > 0:
                done = False

        if done:
            print('\nSRT')
            tottat = 0.0
            totwt = 0.0
            for job in queue.getjobs():
                tottat += job.tat
                totwt += job.wt
                print(job)

            tottat = tottat / len(queue.getjobs())
            totwt = totwt / len(queue.getjobs())

            print('SRT Average TAT: ' + str(tottat))
            print('SRT Average WT: ' + str(totwt))
            break

    # round robin
    quanta = 3
    queue.reset()
    currentjob = None
    clock = 0
    count = 0
    index = 0
    queue.sortfcfs()
    while True:

        if currentjob is None:
            if queue.getjobs()[index].at >= clock:
                currentjob = queue.getjobs()[index]
                queue.getjobs()[index].current = True

        elif count == quanta:
            count = -1
            queue.getjobs()[index] = currentjob
            queue.getjobs()[index].current = False
            flag = True
            while flag:
                if index != len(queue.getjobs()) - 1:
                    index = index + 1
                else:
                    index = 0
                if queue.getjobs()[index].tl > 0 and (queue.getjobs()[index].at >= clock or queue.getjobs()[index].bt > queue.getjobs()[index].tl):
                    flag = False

            queue.getjobs()[index].current = True
            currentjob = queue.getjobs()[index]
            # print('New Current Job: ' + str(currentjob))

        else:
            if currentjob.tl == 1:
                currentjob.tl = currentjob.tl - 1
                currentjob.ct = clock
                currentjob.tat = currentjob.bt + currentjob.wt
                currentjob.wt = currentjob.wt
                count = -1
                queue.getjobs()[index] = currentjob
                queue.getjobs()[index].current = False
                if index != len(queue.getjobs()) - 1:
                    index = index + 1
                else:
                    index = 0

                queue.getjobs()[index].current = True
                currentjob = queue.getjobs()[index]
                # print('New Current Job: ' + str(currentjob))
            else:
                currentjob.tl = currentjob.tl - 1



        queue.updatewaittime(1)
        # print('Clock: ' + str(clock) + '\tCurrent Job: ' + str(currentjob))
        clock = clock + 1
        count = count + 1

        done = True
        for job in queue.getjobs():
            if job.tl > 0:
                done = False

        if done:
            print('\nRR')
            tottat = 0.0
            totwt = 0.0
            queue.sortalph()
            for job in queue.getjobs():
                tottat += job.tat
                totwt += job.wt
                print(job)

            tottat = tottat / len(queue.getjobs())
            totwt = totwt / len(queue.getjobs())

            print('RR Average TAT: ' + str(tottat))
            print('RR Average WT: ' + str(totwt))
            break