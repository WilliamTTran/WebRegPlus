class CreateCourses < ActiveRecord::Migration[5.2]
  def change
    create_table :courses do |t|
      t.string :number
      t.string :name
      t.string :prereqs
      t.string :description
      t.boolean :required

      t.timestamps
    end
  end
end
