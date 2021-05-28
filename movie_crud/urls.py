from django.urls import path

from .views import createNewMovie, getMovie, updateMovie, deleteMovie

urlpatterns = [

	path('create-new-movie', createNewMovie),
	path('get-movies/<int:id>', getMovie),
	path('get-movies', getMovie),
	# path('update_movie/<int:id>', updateMovie),
	# path('delete-movie/<int:id>', deleteMovie)

]