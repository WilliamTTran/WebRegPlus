<template>
  <div>
    <b-navbar toggleable="md" type="dark" variant="dark">
      <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>

      <b-navbar-brand href="#" @click="displayHome">WebReg+</b-navbar-brand>

      <b-collapse is-nav id="nav_collapse">

        <b-navbar-nav>
          <b-nav-item href="#" @click="displayScheduler">Scheduler</b-nav-item>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>

    <div class="my-5 mx-auto" style="min-width:400px; width:30%">
      <b-img src="https://cdn.discordapp.com/attachments/409622117403983883/500891211943378954/Untitled-2.png" fluid-grow alt="WebReg+" />
    </div>

    <div class="mx-auto" style="width:80%">
        <div v-if="isHome">
          <b-form-textarea id="textarea1"
                           v-model="courseText"
                           placeholder="Example: 'CSE 8A;CSE 8B;CSE 12;'"
                           :rows="3"
                           :max-rows="6">
          </b-form-textarea>
          <b-button class="my-4" variant="secondary" @click="generateCourseList">
            Generate Schedules!
          </b-button>
          <h2 class="mt-2 mb-4">
            Welcome to webReg+!
          </h2>
          <p>
            webReg+ is a new way to help you sign up for classes by generating possible year-long schedules for you.
            Each schedule contains the average GPA, average professor ratings, average hours per week, and more to
            help you choose the one that suits you the most. Afterwards, you can view each class individually which
            includes a podcast from the professor of that class, so you can look at their teaching style as well as
            a bunch of other helpful pieces of information.
          </p>
          <p>
            In order to get started, just enter in the courses that you have already taken in the format:
            "CSE 8A;CSE 8B;CSE 12;" where you have a course followed by a semicolon so that the algorithm can easily
            generate the schedule.
          </p>
        </div>

      <div v-if="!isHome" >
        <h2 class="mb-4">
          Available Schedules
        </h2>

        <!-- Select Schedule -->
        <b-table hover responsive :items="schedules" :fields="fields" style="cursor:pointer; background-color:white" @click="scheduleRowClicked"></b-table>

        <!-- Accordion List -->
        <h2 class="mt-2 mb-4">
          Fall
        </h2>
        <div role="tablist" v-for="item in fallItems">
          <b-card no-body class="mb-1">
            <b-card-header header-tag="header" class="p-1" role="tab">
              <b-btn block href="#" v-b-toggle="'fall' + item.course.replace(' ', '')" style="background-color:gray">
                <b-row>
                  <b-col>{{item.course}}</b-col>
                  <b-col>{{item.name}}</b-col>
                  <b-col>{{item.profName}}</b-col>
                </b-row>
              </b-btn>
            </b-card-header>
            <b-collapse :id="'fall' + item.course.replace(' ', '')" role="tabpanel">
              <b-card-body>
                <p class="card-text">
                  {{ item.description }}
                </p>
                <p v-if="item.prereqs">
                  Pre-requisites: {{ item.prereqs }}
                </p>
                <p v-if="item.profRec">
                  Professor Recommendation (CAPES): {{ item.profRec + '%' }}
                </p>
                <p v-if="item.rmpScore">
                  Professor Recommendation (RateMyProfessor): {{ item.rmpScore + '%'}}
                </p>
                <p v-if="item.studentRec">
                  Student Recommendation: {{ item.studentRec + '%' }}
                </p>
                <p v-if="item.studyHr">
                  Average Hours per week: {{ item.studyHr }}
                </p>
                  Units: {{ item.units }}
              </b-card-body>
            </b-collapse>
          </b-card>
        </div>
        <h2 class="mt-2 mb-4">
          Winter
        </h2>
        <div role="tablist" v-for="item in winterItems">
          <b-card no-body class="mb-1">
            <b-card-header header-tag="header" class="p-1" role="tab">
              <b-btn block href="#" v-b-toggle="'winter' + item.course.replace(' ', '')" style="background-color:gray">
                <b-row>
                  <b-col>{{item.course}}</b-col>
                  <b-col>{{item.name}}</b-col>
                  <b-col>{{item.profName}}</b-col>
                </b-row>
              </b-btn>
            </b-card-header>
            <b-collapse :id="'winter' + item.course.replace(' ', '')" role="tabpanel">
              <b-card-body>
                <p class="card-text">
                  {{ item.description }}
                </p>
                <p v-if="item.prereqs">
                  Pre-requisites: {{ item.prereqs }}
                </p>
                <p v-if="item.profRec">
                  Professor Recommendation (CAPES): {{ item.profRec + '%' }}
                </p>
                <p v-if="item.rmpScore">
                  Professor Recommendation (RateMyProfessor): {{ item.rmpScore + '%'}}
                </p>
                <p v-if="item.studentRec">
                  Student Recommendation: {{ item.studentRec + '%' }}
                </p>
                <p v-if="item.studyHr">
                  Average Hours per week: {{ item.studyHr }}
                </p>
                Units: {{ item.units }}
              </b-card-body>
            </b-collapse>
          </b-card>
        </div>
        <h2 class="mt-2 mb-4">
          Spring
        </h2>
        <div role="tablist" v-for="item in springItems">
          <b-card no-body class="mb-1">
            <b-card-header header-tag="header" class="p-1" role="tab">
              <b-btn block href="#" v-b-toggle="'spring' + item.course.replace(' ', '')" style="background-color:gray">
                <b-row>
                  <b-col>{{item.course}}</b-col>
                  <b-col>{{item.name}}</b-col>
                  <b-col>{{item.profName}}</b-col>
                </b-row>
              </b-btn>
            </b-card-header>
            <b-collapse :id="'spring' + item.course.replace(' ', '')" role="tabpanel">
              <b-card-body>
                <p class="card-text">
                  {{ item.description }}
                </p>
                <p v-if="item.prereqs">
                  Pre-requisites: {{ item.prereqs }}
                </p>
                <p v-if="item.profRec">
                  Professor Recommendation (CAPES): {{ item.profRec + '%' }}
                </p>
                <p v-if="item.rmpScore">
                  Professor Recommendation (RateMyProfessor): {{ item.rmpScore + '%'}}
                </p>
                <p v-if="item.studentRec">
                  Student Recommendation: {{ item.studentRec + '%' }}
                </p>
                <p v-if="item.studyHr">
                  Average Hours per week: {{ item.studyHr }}
                </p>
                Units: {{ item.units }}
              </b-card-body>
            </b-collapse>
          </b-card>
        </div>
        <h2 class="mt-2 mb-4">
          Current Quarter Calendar
        </h2>
        <b-table responsive small bordered :items="calendar" style="background-color:white"></b-table>
      </div>
    </div>
  </div>
</template>

<script>
    import data from './data.json';
    import scratch from '../scratch.js';
    /*const items = [
        { course: 'CSE 20', name: 'Secret Math', startTime: '8:00 am', endTime: '9:50 am', days: 'MWF',
            description: 'Basic discrete mathematical structures: sets, relations, functions, sequences, equivalence relations, partial orders, and number systems. Methods of reasoning and proofs: prepositional logic, predicate logic, induction, recursion, and pigeonhole principle. Infinite sets and diagonalization. Basic counting techniques; permutation and combinations. Applications will be given to digital logic design, elementary number theory, design of programs, and proofs of program correctness. Students who have completed Math 109 may not receive credit for CSE 20. Credit not offered for both Math 15A and CSE 20. Equivalent to Math 15A.'},
        { course: 'CSE 12', name: 'Data Structures', startTime: '10:30 am', endTime: '11:20 am', days: 'MTu', description: 'xd'},
        { course: 'CSE 15L', name: 'Unix Lab', startTime: '11:30 am', endTime: '1:20 pm', days: 'TuTh', description: 'xd'},
        { course: 'CSE 100', name: 'Super Data Structures', startTime: '5:00 pm', endTime: '6:50 pm', days: 'TuF', description: 'xd'}
    ];*/
    let fallItems = [];
    let winterItems = [];
    let springItems = [];
    const schedules = [
        { hours: 20, CAPESScore: 70, RMPScore: 65, studentScore: 55, gpa: 3.23},
        { hours: 22, CAPESScore: 68, RMPScore: 66, studentScore: 60, gpa: 3.19},
        { hours: 18, CAPESScore: 64, RMPScore: 62, studentScore: 48, gpa: 3.35},
    ];
    const fields = [
        {
            key: 'hours',
            label: 'Average Hours',
            sortable: true
        },
        {
            key: 'gpa',
            label: 'Average GPA',
            sortable: true,
        },
        {
            key: 'CAPESScore',
            label: 'Professor Score (CAPES)',
            sortable: true
        },
        {
            key: 'RMPScore',
            label: 'Professor Score (RateMyProfessor)',
            sortable: true,
        },
        {
            key: 'studentScore',
            label: 'Student Score (CAPES)',
            sortable: true,
        }
    ];
    const events = [
        {
            title  : 'event1',
            start  : '2010-01-01',
        },
        {
            title  : 'event2',
            start  : '2010-01-05',
            end    : '2010-01-07',
        },
        {
            title  : 'event3',
            start  : '2010-01-09T12:30:00',
            allDay : false,
        },
    ]
    let calendar = [
        {time: '8:00 am', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '8:30 am', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '9:00 am', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '9:30 am', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '10:00 am', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '10:30 am', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '11:00 am', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '11:30 am', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '12:00 am', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '12:30 am', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '1:00 pm', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '1:30 pm', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '2:00 pm', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '2:30 pm', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '3:00 pm', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '3:30 pm', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '4:00 pm', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '4:30 pm', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '5:00 pm', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '5:30 pm', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '6:00 pm', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '6:30 pm', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '7:00 pm', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '7:30 pm', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
    ]

  export default {
      data: function () {
          return {
              isHome: true,
              fallItems: fallItems,
              winterItems: winterItems,
              springItems: springItems,
              schedules: schedules,
              fields: fields,
              events: events,
              calendar: calendar,
              courseText: ''
      }
    },
    methods: {
        displayHome: function () {
            this.isHome = true;
        },
        displayScheduler: function () {
            this.isHome = false;
        },
        scheduleRowClicked: function (record, index) {
            console.log(record);
        },
        addToCalendar: function(course, dayString, startTime, endTime) {
            let days = [];
            for (let i = 0; i < dayString.length; i++) {
                switch(dayString.charAt(i)) {
                    case 'M':
                        days.push('monday');
                        break;
                    case 'T':
                        i++;
                        if(dayString.charAt(i) == 'u') days.push('tuesday');
                        else days.push('thursday')
                        break;
                    case 'W':
                        days.push('wednesday');
                        break;
                    case 'F':
                        days.push('friday');
                        break;
                }
            }
            let startIndex = 0;
            let endIndex = 0;

            let newStartTime = "";
            let endStartTime = "";

            newStartTime += startTime.split(':')[0];
            if(parseInt(startTime.split(':')[1].split(' ')[0], 10) >= 30) newStartTime += ':30 ';
            else newStartTime += ':00 ';
            newStartTime += startTime.split(':')[1].split(' ')[1];

            endStartTime += endTime.split(':')[0];
            if(parseInt(endTime.split(':')[1].split(' ')[0], 10) >= 30) endStartTime += ':30 ';
            else endStartTime += ':00 ';
            endStartTime += endTime.split(':')[1].split(' ')[1];

            for(let i = 0; i < calendar.length; i++) {
                if(newStartTime == calendar[i].time) {
                    startIndex = i;
                }
                if(endStartTime == calendar[i].time) {
                    endIndex = i;
                }
            }

            for(let dayIndex = 0; dayIndex < days.length; dayIndex++) {
                for (let i = startIndex; i <= endIndex; i++) {
                    calendar[i][days[dayIndex]] = course;
                    calendar[i]._cellVariants[days[dayIndex]] = "info";
                }
            }
        },
        generateCourseList: function () {
            this.fallItems = [];
            this.winterItems = [];
            this.springItems = [];

            let splitArray = this.courseText.split(';');
            let courseList = [];
            for(let i = 0; i < splitArray.length; i++) {
                courseList.push(splitArray[i]);
            }
            this.isHome = false;
            let schedule = scratch.createSchedule(courseList, data);
            console.log(schedule);
            for(let season in schedule) {
                for(let course in schedule[season]) {
                    if(season == 0) {
                        this.fallItems.push({
                            course: schedule[season][course].number,
                            name: schedule[season][course].name,
                            profName: schedule[season][course].prof_name,
                            profRec: schedule[season][course].prof_rec_percent,
                            studentRec: schedule[season][course].class_rec_precent,
                            rmpScore: schedule[season][course].rmpScore,
                            studyHr: schedule[season][course].study_hr,
                            units: schedule[season][course].units,
                            prereqs: schedule[season][course].prereqs,
                            description: schedule[season][course].description
                        });
                    }
                    else if(season == 1) {
                        this.winterItems.push({
                            course: schedule[season][course].number,
                            name: schedule[season][course].name,
                            profName: schedule[season][course].pKrof_name,
                            profRec: schedule[season][course].prof_rec_percent,
                            studentRec: schedule[season][course].class_rec_precent,
                            rmpScore: schedule[season][course].rmpScore,
                            studyHr: schedule[season][course].study_hr,
                            units: schedule[season][course].units,
                            prereqs: schedule[season][course].prereqs,
                            description: schedule[season][course].description
                        });
                    }
                    else {
                        this.springItems.push({
                            course: schedule[season][course].number,
                            name: schedule[season][course].name,
                            profName: schedule[season][course].prof_name,
                            profRec: schedule[season][course].prof_rec_percent,
                            studentRec: schedule[season][course].class_rec_precent,
                            rmpScore: schedule[season][course].rmpScore,
                            studyHr: schedule[season][course].study_hr,
                            units: schedule[season][course].units,
                            prereqs: schedule[season][course].prereqs,
                            description: schedule[season][course].description
                        });
                    }
                }
            }
            //for(let i = 0; i < items.length; i++) {
            //    this.addToCalendar(items[i].course, items[i].days, items[i].startTime, items[i].endTime);
            //}
        },
    },
    created: function () {
    }
  }
</script>

<style scoped>
</style>
