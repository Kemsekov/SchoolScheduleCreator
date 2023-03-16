# Motivation
Imagine you have a several classes in school which attain 
same disciplines in different proportions and you need to 
create a schedule in which each group attend
required amount of lessons of each discipline per week.
At the same time you restricted on how much lessons per day one group
can handle and how much lessons each teacher can perform in a day.

Also, it would be inconvenient to have like 4 math's in a row
on the monday, so you also need to limit on how much same type of
lessons can happen in a day.

Also, teacher cannot be in two places simultaneously, so we need to avoid
cases when group A and group B have math as first lesson in the same day.

You need to create a schedule that perfectly fits all this requirements,
so teachers don't overdo themselves, students have a stable amount
of lessons each day and their workload is stable.

So this python program builds a 'smart' flow graph from given data, finds
max flow, creates a schedule for the whole week for each of given group and
reorder it a bit. By doing this we successfully creating perfect schedule
for both teachers and students.

# Dependencies
    networkx-2.8.5

# Expected output

In the project there is a data.json which content is describing all
this requirements. After I run program with that json here's what it output:

```
Group A

monday:
        informatics
        math
        math

tuesday:
        informatics
        chemistry
        chemistry
        literature

wednesday:
        history
        history
        pce
        pce
        literature

thursday:
        physics
        physics
        math
        biology
        russian

friday:
        biology
        physics
        russian
        math
        physics

-----------------
Group B

monday:
        math
        biology
        biology

tuesday:
        chemistry
        informatics
        informatics
        ---
        history

wednesday:
        informatics
        informatics
        history
        literature
        pce

thursday:
        literature
        pce
        chemistry
        physics
        math

friday:
        physics
        math
        math
        russian
        russian

-----------------
Group C

monday:
        biology
        informatics
        history

tuesday:
        pce
        russian
        history
        history

wednesday:
        physics
        physics
        russian
        informatics
        math

thursday:
        math
        history
        literature
        literature
        chemistry

friday:
        pce
        chemistry
        literature
        literature
        biology

-----------------
Group D

monday:
        history
        literature
        pce

tuesday:
        russian
        math
        physics
        biology
        russian

wednesday:
        chemistry
        math
        biology
        physics
        chemistry

thursday:
        chemistry
        biology
        history
        informatics

friday:
        chemistry
        literature
        biology
        informatics
        pce

-----------------
```
