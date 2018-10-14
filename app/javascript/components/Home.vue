<template>
  <div>
    <b-navbar toggleable="md" type="dark" variant="info">
      <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>

      <b-navbar-brand href="#" @click="displayHome">WebReg+</b-navbar-brand>

      <b-collapse is-nav id="nav_collapse">

        <b-navbar-nav>
          <b-nav-item href="#" @click="displayScheduler">Scheduler</b-nav-item>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>

    <div class="mx-auto" style="width:80%">
        <div v-if="isHome">
          <h2 class="mt-2 mb-4">
            Welcome to WebReg+
          </h2>
        </div>

      <div v-if="!isHome" >
        <h2 class="mt-2 mb-4">
          Available Schedules
        </h2>
        <b-table hover :items="items" @row-clicked="classRowClicked"></b-table>
      </div>
    </div>
  </div>
</template>

<script>
    const items = [
        { course: 'CSE 20', name: 'Secret Math', prereqs: 'CSE 11', required: true,
            description: 'Basic discrete mathematical structures: sets, relations, functions, sequences, equivalence relations, partial orders, and number systems. Methods of reasoning and proofs: prepositional logic, predicate logic, induction, recursion, and pigeonhole principle. Infinite sets and diagonalization. Basic counting techniques; permutation and combinations. Applications will be given to digital logic design, elementary number theory, design of programs, and proofs of program correctness. Students who have completed Math 109 may not receive credit for CSE 20. Credit not offered for both Math 15A and CSE 20. Equivalent to Math 15A.'},
        { course: 'CSE 12', name: 'Data Structures', prereqs: 'CSE 11', required: true, description: 'xd'},
        { course: 'CSE 15L', name: 'Unix Lab', prereqs: 'CSE 11', required: true, description: 'xd'},
        { course: 'CSE 100', name: 'Super Data Structures', prereqs: 'CSE 30, CSE 21', required: false, description: 'xd'}
    ]

  export default {
    data: function () {
      return {
        isHome: true,

        items: items
      }
    },
    methods: {
        displayHome: function () {
            this.isHome = true
        },
        displayScheduler: function () {
            this.isHome = false
        },
        classRowClicked: function (record, index) {
            console.log(record)
        }
    }
  }
</script>

<style scoped>
</style>
