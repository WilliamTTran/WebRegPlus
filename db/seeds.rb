# This file should contain all the record creation needed to seed the database with its default values.
# The data can then be loaded with the rails db:seed command (or created alongside the database with db:setup).
#
# Examples:
#
#   movies = Movie.create([{ name: 'Star Wars' }, { name: 'Lord of the Rings' }])
#   Character.create(name: 'Luke', movie: movies.first)
require 'tod'

course = Course.create(
  number: "CSE 11",
  name: "Introduction to Java",
  prof_rec_percent: "51.4",
  class_rec_percent: "86.6",
  study_hr: "11.2",
  avg_gpa: "3.8",
  rmp_score: "2.8",
  prof_name: "Rick Ord",
  required: "Boolean"
)

Offering.create(
  course_id: course.id,
  season: "fall",
  time_begin: TimeOfDay.new(8),
  time_end: TimeOfDay.new(8, 50)
)