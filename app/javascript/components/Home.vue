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
          <b-button class="my-4 ml-auto" variant="secondary" @click="generateCourseList">
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
          Schedule statistics
        </h2>

        <!-- Select Schedule -->
        <b-table responsive :items="schedules" :fields="fields" style="background-color:white" @click="scheduleRowClicked"></b-table>

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
                <b-embed v-if="item.podcastUrl" type="iframe"
                         style="margin-bottom: 1rem"
                         aspect="16by9"
                         :src=item.podcastUrl
                         allowfullscreen
                ></b-embed>
                <p :class="['card-text', { 'my-3' : item.podcastUrl }]">
                  {{ item.description }}
                </p>
                <p v-if="item.prereqs">
                  Pre-requisites: {{ item.prereqs }}
                </p>
                <p v-if="item.profRec">
                  Professor Recommendation (CAPES): {{ item.profRec + '%' }}
                </p>
                <p v-if="item.rmpScore">
                  Professor Recommendation (RateMyProfessor): {{ item.rmpScore}}
                </p>
                <p v-if="item.studentRec">
                  Student Recommendation: {{ item.studentRec + '%' }}
                </p>
                <p v-if="item.avgGPA">
                  Average GPA: {{ item.avgGPA }}
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
                <b-embed v-if="item.podcastUrl" type="iframe"
                         aspect="16by9"
                         :src=item.podcastUrl
                         allowfullscreen
                ></b-embed>
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
                  Professor Recommendation (RateMyProfessor): {{ item.rmpScore}}
                </p>
                <p v-if="item.studentRec">
                  Student Recommendation: {{ item.studentRec + '%' }}
                </p>
                <p v-if="item.avgGPA">
                  Average GPA: {{ item.avgGPA }}
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
                <b-embed v-if="item.podcastUrl" type="iframe"
                         aspect="16by9"
                         :src=item.podcastUrl
                         allowfullscreen
                ></b-embed>
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
                  Professor Recommendation (RateMyProfessor): {{ item.rmpScore}}
                </p>
                <p v-if="item.studentRec">
                  Student Recommendation: {{ item.studentRec + '%' }}
                </p>
                <p v-if="item.avgGPA">
                  Average GPA: {{ item.avgGPA }}
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
    import scratch from '../scratch.js';
    import api from './api.js';
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
    /*const schedules = [
        { hours: 20, CAPESScore: 70, RMPScore: 65, studentScore: 55, gpa: 3.23},
        { hours: 22, CAPESScore: 68, RMPScore: 66, studentScore: 60, gpa: 3.19},
        { hours: 18, CAPESScore: 64, RMPScore: 62, studentScore: 48, gpa: 3.35},
    ];*/
    const fields = [
        {
            key: 'season',
        },
        {
            key: 'hours',
            label: 'Average Hours',
        },
        {
            key: 'gpa',
            label: 'Average GPA',
        },
        {
            key: 'profScore',
            label: 'Professor Rec.',
        },
        {
            key: 'studentRecommendation',
            label: 'Class Rec.',
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
    const original_calendar = [
        {time: '8:00 AM', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '8:30 AM', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '9:00 AM', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '9:30 AM', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '10:00 AM', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '10:30 AM', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '11:00 AM', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '11:30 AM', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '12:00 PM', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '12:30 PM', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '1:00 PM', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '1:30 PM', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '2:00 PM', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '2:30 PM', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '3:00 PM', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '3:30 PM', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '4:00 PM', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '4:30 PM', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '5:00 PM', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '5:30 PM', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '6:00 PM', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '6:30 PM', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '7:00 PM', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
        {time: '7:30 PM', monday: '', tuesday: '', wednesday: '', thursday: '', friday: '', _cellVariants:{}},
    ];

  export default {
      data: function () {
          return {
              isHome: true,
              fallItems: fallItems,
              winterItems: winterItems,
              springItems: springItems,
              schedules: [],
              fields: fields,
              events: events,
              calendar: [],
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
                        if(i + 1 < dayString.length && dayString.charAt(i + 1) == 'h') {
                            days.push('thursday');
                            i++;
                        }
                        else days.push('tuesday')
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

            for(let i = 0; i < this.calendar.length; i++) {
                if(newStartTime == this.calendar[i].time) {
                    startIndex = i;
                }
                if(endStartTime == this.calendar[i].time) {
                    endIndex = i;
                }
            }

            for(let dayIndex = 0; dayIndex < days.length; dayIndex++) {
                for (let i = startIndex; i <= endIndex; i++) {
                    this.calendar[i][days[dayIndex]] = course;
                    this.calendar[i]._cellVariants[days[dayIndex]] = "info";
                }
            }
        },
        generateCourseList: function () {
            this.fallItems = [];
            this.winterItems = [];
            this.springItems = [];
            this.schedules = [];
            this.calendar = JSON.parse(JSON.stringify(original_calendar));

            let splitArray = this.courseText.split(/[,;](?=\s*?)/gm);
            let courseList = [];
            for(let i = 0; i < splitArray.length; i++) {
                courseList.push(splitArray[i].trim());
            }
            this.isHome = false;
            let schedule = scratch.createSchedule(courseList, this.offerings);
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
                            rmpScore: schedule[season][course].rmp_score,
                            studyHr: schedule[season][course].study_hr,
                            avgGPA: schedule[season][course].avg_gpa,
                            units: schedule[season][course].units,
                            prereqs: schedule[season][course].prereqs,
                            podcastUrl: schedule[season][course].podcast_url,
                            days: schedule[season][course].lecture_days,
                            startTime: schedule[season][course].lecture_start,
                            endTime: schedule[season][course].lecture_end,
                            description: schedule[season][course].description
                        });
                    }
                    else if(season == 1) {
                        this.winterItems.push({
                            course: schedule[season][course].number,
                            name: schedule[season][course].name,
                            profName: schedule[season][course].prof_name,
                            profRec: schedule[season][course].prof_rec_percent,
                            studentRec: schedule[season][course].class_rec_precent,
                            rmpScore: schedule[season][course].rmp_score,
                            studyHr: schedule[season][course].study_hr,
                            avgGPA: schedule[season][course].avg_gpa,
                            units: schedule[season][course].units,
                            prereqs: schedule[season][course].prereqs,
                            podcastUrl: schedule[season][course].podcast_url,
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
                            rmpScore: schedule[season][course].rmp_score,
                            studyHr: schedule[season][course].study_hr,
                            avgGPA: schedule[season][course].avg_gpa,
                            units: schedule[season][course].units,
                            prereqs: schedule[season][course].prereqs,
                            podcastUrl: schedule[season][course].podcast_url,
                            description: schedule[season][course].description
                        });
                    }
                }
            }
            for(let i = 0; i < this.fallItems.length; i++) {
                if(this.fallItems[i].days != null) {
                    this.addToCalendar(this.fallItems[i].course, this.fallItems[i].days,
                        this.fallItems[i].startTime, this.fallItems[i].endTime);
                }
            }
            let scheduleData = scratch.calculateData(schedule);
            for(let i = 0; i < 3; i++)
            {
                if(i == 0) this.schedules.push({season: 'Fall', hours: scheduleData['fall'].study_hr,
                    profScore: scheduleData['fall'].season_prof_rec, studentRecommendation: scheduleData['fall'].season_class_rec,
                    gpa: scheduleData['fall'].avg_gpa});
                if(i == 1) this.schedules.push({season: 'Winter', hours: scheduleData['winter'].study_hr,
                    profScore: scheduleData['winter'].season_prof_rec, studentRecommendation: scheduleData['winter'].season_class_rec,
                    gpa: scheduleData['winter'].avg_gpa});
                if(i == 2) this.schedules.push({season: 'Spring', hours: scheduleData['spring'].study_hr,
                    profScore: scheduleData['spring'].season_prof_rec, studentRecommendation: scheduleData['spring'].season_class_rec,
                    gpa: scheduleData['spring'].avg_gpa});
            }
        },
    },
    created: async function () {
       this.offerings = (await api.getOfferings()).data;
    }
  }
</script>

<style scoped>
</style>
