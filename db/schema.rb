# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# Note that this schema.rb definition is the authoritative source for your
# database schema. If you need to create the application database on another
# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 2018_10_14_091953) do

  create_table "courses", force: :cascade do |t|
    t.string "number"
    t.string "name"
    t.string "prereqs"
    t.string "description"
    t.string "units"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "offerings", force: :cascade do |t|
    t.integer "course_id"
    t.string "prof_name"
    t.float "prof_rec_percent"
    t.float "class_rec_percent"
    t.float "study_hr"
    t.float "avg_gpa"
    t.float "rmp_score"
    t.string "season"
    t.string "podcast_url"
    t.string "days_of_week"
    t.string "lecture_days"
    t.string "lecture_room"
    t.string "lecture_start"
    t.string "lecture_end"
    t.string "final_day"
    t.string "final_start"
    t.string "final_end"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["course_id"], name: "index_offerings_on_course_id"
  end

end
