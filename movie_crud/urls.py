from django.urls import path

from .views import createNewMovie, getMovie, updateMovie, deleteMovie

urlpatterns = [

	path('create-new-movie', createNewMovie, name="createNewMovie"),
	path('get-movies/<int:id>', getMovie, name="getMovie"),
	path('get-movies', getMovie, name="getMovies"),
	path('update_movie/<int:id>', updateMovie, name="updateMovie"),
	path('delete-movie/<int:id>', deleteMovie, name="deleteMovie")

]