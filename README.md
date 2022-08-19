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

In the project there is a data.json which content is describing all
this requirements. After I run program with that json here's what it output:

```
Group D

monday:
        math
        informatics
        informatics

tuesday:
        chemistry
        history
        history
        russian

wednesday:
        literature
        literature
        pce
        pce
        chemistry

thursday:
        math
        physics
        physics
        biology
        russian

friday:
        math
        math
        physics
        physics
        biology

-----------------
Group D

monday:
        informatics
        history
        biology
        russian
        russian

tuesday:
        history
        pce
        biology

wednesday:
        chemistry
        pce
        math
        chemistry
        literature

thursday:
        physics
        math
        math
        informatics

friday:
        literature
        physics
        math
        informatics
        informatics

-----------------
Group D

monday:
        russian
        physics
        history
        history
        physics

tuesday:
        math
        math
        chemistry

wednesday:
        history
        informatics
        informatics
        russian

thursday:
        literature
        literature
        pce
        chemistry
        history

friday:
        literature
        biology
        biology
        literature
        pce

-----------------
Group D

monday:
        biology
        biology
        physics
        pce
        pce

tuesday:
        literature
        biology
        math

wednesday:
        physics
        math
        biology
        history

thursday:
        informatics
        chemistry
        literature
        chemistry
        informatics

friday:
        chemistry
        chemistry
        history
        russian
        russian

-----------------
```