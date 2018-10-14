class Api::OfferingsController < ActionController::API
  def post
    offerings = JSON.parse(request.raw_post)
    offerings.each do |offering|
      course = Course.find_by(number: offering['course_number'])
      offering['course_id'] = course.nil? ? nil : course.id
      offering.delete 'course_number'
      print(offering.to_s)
    end
    Offering.create(offerings)
    head :ok
  end

  def get
    render json: Course.all
  end

  # Clear all
  def delete
    Course.destroy_all
    head :ok
  end
end
