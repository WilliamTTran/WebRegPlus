class Api::CoursesController < ActionController::API
  def post
    Course.create(JSON.parse(request.raw_post))
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
