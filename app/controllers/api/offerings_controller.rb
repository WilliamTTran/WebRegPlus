class Api::OfferingsController < ActionController::API
  def post
    offerings = request.body.read
    offerings.each do |offering|
      offering['course_id'] = Course.find_by_number(offering['course_number'])
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
