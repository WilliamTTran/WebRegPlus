Rails.application.routes.draw do

  namespace :api do
    post 'courses/' => 'courses#post'
    get 'courses/' => 'courses#get'

    post 'offering/' => 'offering#post'
    get 'offering/' => 'offering#get'
  end

  root to: 'hello#index'
  match '*path', to: 'hello#index', format: false, via: :get, constraints: lambda{ |req| !req.env['PATH_INFO'].start_with?('/api') }

  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
end
