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
      t.string :time_begin
      t.string :datetime
      t.datetime :time_end

      t.timestamps
    end
  end
end
