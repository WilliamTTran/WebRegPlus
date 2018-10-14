const REQUIRED_COURSES = [
    ['CSE 8B', 'CSE 11'],
    ['CSE 12'],
    ['CSE 15L'],
    ['CSE 20'],
    ['CSE 21'],
    ['CSE 30'],
    ['CSE 100'],
    ['CSE 101'],
    ['CSE 103'],
    ['CSE 110'],
    ['CSE 140'],
    ['CSE 140L'],
    ['CSE 141'],
    ['CSE 141L'],
    ['CSE 120', 'CSE 123', 'CSE 124'],
    ['CSE 130', 'CSE 132A'],
    ['CSE 107', 'CSE 127'],
    ['CSE 150', 'CSE 151', 'CSE 152', 'CSE 158', 'CSE 167']
];

function createSchedule(taken, data) {
    if (taken.includes('CSE 8B') && !taken.includes('CSE 8A')) {
        taken.push('CSE 8A')
    }
    if (taken.includes('CSE 11') && !taken.includes('CSE 8B')) {
        taken.push('CSE 8A', 'CSE 8B')
    }
    data = data.filter(d => !taken.includes(d.number));

    let fall = [];
    let winter = [];
    let spring = [];
    let schedule = [fall, winter, spring];

    let courseScores = [];
    for(let index = 0; index < data.length; index++) {
        const offering = data[index];
        let bonus = 0;
        for (let i = 0; i < REQUIRED_COURSES.length; i++) {
            if (REQUIRED_COURSES[i].includes(offering.number)) bonus = 200 / Math.pow(REQUIRED_COURSES[i].length, 1.5)
        }
        courseScores.push({
            course: offering,
            score: bonus + offering.prof_rec_percent + offering.class_rec_percent + (offering.rmp_score) * 20.00
        });
    }

    courseScores.sort(function(a, b) {
       return b.score - a.score;
    });

    for(let c = 0; c < 3; c++) {
        for (let i = 0; i < courseScores.length; i++) {
            if(courseScores[i].course.season === 'winter') {
                console.log('\n' + courseScores[i].course.number)
                console.log(prereqCheck(courseScores[i].course, taken))
                console.log(prereqList(courseScores[i].course))
            }
            if (insertIntoSchedule(courseScores[i].course, schedule, taken)) {
                courseScores.splice(i, 1);
                i--;
            }
        }
    }

    console.log('\nFall');
    for (let index in schedule[0]) {
        console.log(schedule[0][index].number + '\t' + schedule[0][index].name)
    }
    console.log('\nWinter');
    for (let index in schedule[1]) {
        console.log(schedule[1][index].number + '\t' + schedule[1][index].name)
    }
    console.log('\nSpring');
    for (let index in schedule[2]) {
        console.log(schedule[2][index].number + '\t' + schedule[2][index].name)
    }

    return schedule;
}

function insertIntoSchedule(offering, schedule, taken) {
    if (schedule[0].length < 3 && offering.season === 'fall' && canTakeQuarter(offering, schedule, taken)) {
        if (!checkTimeConflict(schedule[0], offering)) {
            schedule[0].push(offering);
            return true;
        }
    } else if (schedule[1].length < 3 && offering.season === 'winter' && canTakeQuarter(offering, [schedule[1], schedule[2]], taken.concat(schedule[0].map(function(c) { return c.number; })))) {
        schedule[1].push(offering);
        return true;

    } else if (schedule[2].length < 3 && offering.season === 'spring' && canTakeQuarter(offering, [schedule[2]], taken.concat(schedule[0].concat(schedule[1]).map(function(c) { return c.number; })))) {
        schedule[2].push(offering);
        return true;
    }
    return false;
}

function canTakeQuarter(offering, seasonsNowAndAfter, taken) {
    if (taken.includes(offering.number) || prereqCheck(offering, taken).length > 0) return false;
    for (let s = 0; s < seasonsNowAndAfter.length; s++) {
        for (let c = 0; c < seasonsNowAndAfter[s].length; c++) {
            if (seasonsNowAndAfter[s][c].number === offering.number) {
                return false;
            }
        }
    }

    return true;
}

function prereqList(course) {
    if (course.prereqs === undefined || course.prereqs === null || course.prereqs.includes('none')) {
        return [];
    }
    let ands = course.prereqs.split('; ')[0].split('. ')[0].replace(/, (?!(and ))/g, ' and ').split(' and ');
    let prereqs = [];
    for (let i = 0; i < ands.length; i++) {
        let ors = ands[i].replace(/[^a-z0-9\s]/gmi, '').split(' or ').filter(function(req) {
            const parts = req.split(' ');
            let courseNumValid = !isNaN(parts[1].trim()) || !isNaN(parts[1].substring(0, parts[1].length - 1).trim());
            return parts.length === 2 && courseNumValid;
        });
        if (ors.length > 0) prereqs.push(ors);
    }
    return prereqs;
};

function prereqCheck(course, classesTaken) {
    const prereqs = prereqList(course);
    let needLeft = [];
    for (let i = 0; i < prereqs.length; i++) {
        let taken = false;
        for (let j = 0; j < prereqs[i].length; j++) {
            if (classesTaken.includes(prereqs[i][j])) {
                taken = true;
                break;
            }
        }
        if (!taken) needLeft.push(prereqs[i]);
    }
    return needLeft;
}

function checkTimeConflict(season, course) {
    const days = ['M', 'TU', 'W', 'TH', 'F'];
    for (let i = 0; i < season.length; i++) {
        if (season[i].lecture_days === null || course.lecture_days === null) {
            continue;
        }
        let lecConflict = false;
        for (let j = 0; j < days.length; j++) {
            if (season[i].lecture_days.includes(days[j]) && course.lecture_days.includes(days[j])) {
                lecConflict = true;
                break;
            }
        }
        if (!lecConflict) {
            const s_s = get24Hr(season[i].lecture_start);
            const s_e = get24Hr(season[i].lecture_end);
            const c_s = get24Hr(course.lecture_start);
            const c_e = get24Hr(course.lecture_end);
            // Lecture conflict
            if ((s_s <= c_s && s_e >= c_s) || (s_s <= c_e && s_e >= c_e)) return true;
        }

        if (season[i].final_day !== course.final_day) continue;
        const s_fs = get24Hr(season[i].final_start);
        const s_fe = get24Hr(season[i].final_end);
        const c_fs = get24Hr(course.final_start);
        const c_fe = get24Hr(course.final_end);
        // Finals conflict
        if ((s_fs <= c_fs && s_fe >= c_fs) || (s_fs <= c_fe && s_e >= c_fe)) return true;
    }
    return false;
}

function get24Hr(time) {
    if(time == null) return null;
    const hr = (Number.parseInt(time.split(':')[0]) + (time.includes('PM') ? 12 : 0) ) % 24;
    return hr + ':' + time.split(':')[1].replace(/[^0-9]/g, '');
}


function calculateData(schedule) {
    const seasons = ['fall', 'winter', 'spring'];
    let data = {
        avg_gpa: 0,
        prof_rec: 0,
        class_rec: 0,
        study_hr: 0
    };
    for(let i = 0; i < schedule.length; i++) {
        let season_gpa = 0;
        let season_prof_rec = 0;
        let season_class_rec = 0;
        let season_study_hr = 0;
        for(let j = 0; j < schedule[i].length; j++) {
            season_gpa += !schedule[i][j].avg_gpa ? 3 : schedule[i][j].avg_gpa;
            season_prof_rec += !schedule[i][j].prof_rec_percent || schedule[i][j].prof_rec_percent == null ? 50 : schedule[i][j].prof_rec_percent;
            season_class_rec += !schedule[i][j].class_rec_percent || schedule[i][j].class_rec_percent  == null? 50 : schedule[i][j].class_rec_percent;
            season_study_hr += !schedule[i][j].study_hr || schedule[i][j].study_hr == null ? 6 : schedule[i][j].study_hr;
        }

        data[seasons[i]] = {
            avg_gpa: schedule[i].length ? Math.round((season_gpa / schedule[i].length) * 100) / 100 : '?',
            season_prof_rec: schedule[i].length ? Math.round(season_prof_rec / schedule[i].length  * 100) / 100: '?',
            season_class_rec: schedule[i].length ? Math.round(season_class_rec / schedule[i].length  * 100) / 100: '?',
            study_hr: schedule[i].length ? Math.round(season_study_hr / schedule[i].length * 100) / 100 : '?',
        };
        data.avg_gpa += season_gpa;
        data.season_prof_rec += season_prof_rec;
        data.season_class_rec += season_class_rec;
        data.study_hr += season_study_hr;
    }

    data.avg_gpa = Math.round(data.avg_gpa / (schedule.length * schedule[0].length) * 100) / 100;
    data.season_prof_rec /= Math.round(data.avg_gpa / (schedule.length * schedule[0].length) * 100) / 100;
    data.season_class_rec /= Math.round(data.avg_gpa / (schedule.length * schedule[0].length) * 100) / 100;
    data.study_hr /= Math.round(data.avg_gpa / (schedule.length * schedule[0].length) * 100) / 100;

    return data;
}

export default { createSchedule, prereqList, calculateData };