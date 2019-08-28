## CS 378 Virtualization (Fall 2019)

Welcome to CS 378 Virtualization for undergrads. This is a course designed to expose undergraduate students to the latest in virtualization technologies such as virtual machines, containers, serverless, etc. The course also has a significant project component to be completed over the course of the semester. *Do not take this course if you are not comfortable reading, editing, and writing code*. 

 This course will introduce students to
  a range of exciting topics including:
  <ul>
    <li>Basics of Virtual Machines</li>
    <li>Basics of Containers</li>
    <li>How CPU is Virtualized</li>
    <li>How Storage is Virtualized</li>
    <li>How Network is Virtualized</li>
    <li>Nested Virtualization</li>
    <li>Hardware Features Assisting Virtualization</li>
    <li>Deploying Virtual Machines</li>
    <li>Orchestrating Containers</li>
    <li>Datacenters and Virtualization</li>
  </ul>

Aside from teaching you the concepts behind virtualization, this course is meant to get you familiar with the commonly used tools and software. You should get used to using virtual machines, and containers. You will gain more experience with Git, and with real-world code bases.

**Piazza Link: [piazza.com/utexas/fall2019/cs378virtualization](http://piazza.com/utexas/fall2019/cs378virtualization)** 

**Canvas Link: [https://utexas.instructure.com/courses/1254479](https://utexas.instructure.com/courses/1254479)** 

**Class Timing and Location**: TuTh 3:30 pm - 5:00pm in **GDC 1.304**

**[Schedule](https://github.com/vijay03/cs378-f19/blob/master/schedule.md)**

**Instructor: [Vijay Chidambaram](https://www.cs.utexas.edu/~vijay/)**

Email: vijayc@utexas.edu

Office hours: 3-4 PM CST Wednesday and Friday, GDC 6.436

**TA: [Rohan Kadekodi](https://www.cs.utexas.edu/~rak/)**

Email: rak@cs.utexas.edu

Office hours: TBD

### Grading 

**20%** Midterm-1 <br>
**20%** Midterm-2 <br>
**30%** Project: implementing your own hypervisor <br>
**30%** Project: contributing to an open-source repository related to virtualization <br>

### Extra Credit

You can earn upto **1%** extra credit if your patches get accepted to any open-source repository related to virtualization. 

**0.5%**: Any patch at all, no restrictions, could be a one line fix to a simple bug.<br>
**0.5%**: This needs to be a more substantial patch, requiring technical thought and care. 

Note that these extra-credit activities will also serve you well in hunting for jobs or internships: getting a patch accepted in a project is impressive.

### Exams

There will be two midterms. There will not be a final exam.

Midterm 1: **Oct 10th** (tentatively) <br>
Midterm 2: **Nov 26th** (tentatively) <br>

Exams will be based on *application* of material learnt in class, and will not require remembering details such as which register is used for which function. You will be allowed one A4 sheet of paper on which you can bring notes for the exam.

Laptops, tablets, and ereaders are **banned** from exams. You should not need them in an exam, and they are far too flexible as communication devices to make enforcement of non-communication policies enforceable. Any use of a communication device for any reason in the exam room will earn an automatic zero on the exam.

### Projects

<p>There will be two big projects in the course. Students will work in
  groups of two or three for both projects.</p>

<p>The first project will involve building your own hypervisor. You
  will need to know the basics of operating systems, C, and assembly
  to complete this project.</p>

<p>The second project is open-ended, and will involve adding a new
  feature to any open-source project related to virtualization and
  containers. Students will propose what they want to do, get the
  proposal approved, and then present on what they did at the end of
  the semester. You are encouraged to add a useful feature to an
  open-source project (and potentially get it merged with the code
  base).</p>

<p>More details about the projects will be added shortly.</p>

### Deadlines (tentative)

**Oct 10** Midterm 1 <br>
**Oct 15** Project 1 due <br>
**Nov 26** Midterm 2 <br>
**Dec 3-5** In-class presentations about open-source contributions <br>
**Dec 12** Report due about open-source contributions <br>

### Course Policies

<p>Students with disabilities may request appropriate academic
accommodations from the Division of Diversity and Community
Engagement, Services for Students with Disabilities, 512-471-6259,
<a href="http://www.utexas.edu/diversity/ddce/ssd/">http://www.utexas.edu/diversity/ddce/ssd/</a>.</p>

<p><b>Religious Holy Days</b>: A student who is absent from an
examination or cannot meet an assignment deadline due to the
observance of a religious holy day may take the exam on an alternate
day or submit the assignment up to 24 hours late without penalty, if
proper notice of the planned absence has been given. Notice must be
given at least 14 days prior to the classes which will be missed. For
religious holy days that fall within the first 2 weeks of the
semester, notice should be given on the first day of the
semester. Notice must be personally delivered to the instructor and
signed and dated by the instructor, or sent certified mail. Email
notification will be accepted if received, but a student submitting
email notification must receive email confirmation from the
instructor.</p>

#### Collaboration 

1. The students are encouraged to do the projects in groups of two or three.
2. All exams are done individually, with absolutely no collaboration.
3. Each student must present.
4. I strongly encourage you to discuss the projects and assignments with
anyone you can. That's the way good science happens. But all work and
writeup for the assignment must be your own, and only your own.
5. As a professional, you should acknowledge significant contributions or
collaborations in your written or spoken presentations.
6. The student code of conduct
is <a href="http://www.cs.utexas.edu/users/ear/CodeOfConduct.html">here</a>. Intellectual
dishonesty can end your career, and it is your responsibility to stay
on the right side of the line. If you are not sure about something,
  ask.
7. **The penalty for cheating on an exam, project or assignment in
    this course is an F in the course and a referral to the Dean of
    Students office.**
8. You cross over from collaboration to cheating when you look at
    another person/team's source code. **Discussing ideas is okay,
  sharing code is not**.
9. You also may not look at any course project material relating to
  any project similar to or the same as this course's class
  projects. For example, you may not look at the work done by a
  student in past years' courses, and you may not look at similar
  course projects at other universities.
10. All submitted work must be new and original.

#### Late Policy

1. All projects/assignments must be submitted in class the day they
are due.
2. For each day a project/assignment is late, you lose 10% of the
  points for that project. So if you submit two days after the
  deadline, your maximum points on that project will be 80%.
3. In this class, it is always better to do the work (even late) than not
do it at all.
4. If you become ill: contact the instructor. A medical note is
 required to miss an exam.

### Acknowledgements

This course is inspired by (and uses material from) courses taught
  by <a href="http://www.cs.unc.edu/~porter/">Don
  Porter</a>, <a href="www.cs.utexas.edu/~ans">Alison
  Norman</a>, <a href="http://pages.cs.wisc.edu/~remzi/">Remzi
  Arpaci-Dusseau</a>, <a href="http://www.cs.utexas.edu/~simon/">Simon
  Peter</a>, and <a href="https://www.cs.utexas.edu/~rossbach/">Chris
  Rossbach</a>.
  
### Copyright

<p>Copyright Notice: These course materials, including, but not
  limited to, lecture notes, homeworks, and projects are copyright
  protected.  You must ask me permission to use these materials.</p>

<p>I do not grant to you the right to publish these materials for profit
  in any form. Any unauthorized copying of the class materials is a
  violation of federal law and may result in disciplinary actions
  being taken against the student or other legal action against an
  outside entity. Additionally, the sharing of class materials without
  the specific, express approval of the instructor may be a violation
  of the University's Student Honor Code and an act of academic
  dishonesty, which could result in further disciplinary action. This
  includes, among other things, uploading class materials to websites
  for the purpose of sharing those materials with other current or
  future students.
