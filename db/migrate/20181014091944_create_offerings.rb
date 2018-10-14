class CreateOfferings < ActiveRecord::Migration[5.2]
  def change
    create_table :offerings do |t|
      t.references :course, foreign_key: true
      t.string :prof_name
      t.float :prof_rec_percent
      t.float :class_rec_percent
      t.float :study_hr
      t.float :avg_gpa
      t.float :rmp_score
      t.string :season
      t.string :podcast_url
      t.string :days_of_week
      t.string :lecture_days
      t.string :lecture_room
      t.string :lecture_start
      t.string :lecture_end
      t.string :final_day
      t.string :final_start
      t.string :final_end

      t.timestamps
    end
  end
end
