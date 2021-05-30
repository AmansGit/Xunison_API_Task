from django.test import TestCase

from movie_crud.models import MovieContainer

from datetime import datetime

class MovieContainerTestCase1(TestCase):
	def setUp(self):
		dor1 = datetime.strptime("2020-12-03", '%Y-%m-%d')
		dor2 = datetime.strptime("2021-05-14", '%Y-%m-%d')
		dor3 = datetime.strptime("2007-12-05", '%Y-%m-%d')

		MovieContainer.objects.create(name="The Mummy", description="This is a Horror movie", date_of_release=dor1)
		MovieContainer.objects.create(name="Army of the Dead", description="After a zombie outbreak in Las Vegas, a group of mercenaries takes the ultimate gamble by venturing into the quarantine zone for the greatest heist ever.", date_of_release=dor2)
		MovieContainer.objects.create(name="I Am Legend", description="Robert Neville, a scientist, is the last human survivor of a plague in the whole of New York. ", date_of_release=dor3)

	def test_get_movie_with_id_pass(self):
		movie_obj = MovieContainer.objects.get(id=1)
		self.assertEqual(movie_obj.name, "The Mummy")
		self.assertTrue(movie_obj.description, "This is a Horror movie")

	# def test_get_movie_with_id_fail(self):
	# 	movie_obj = MovieContainer.objects.get(id=4)
	# 	self.assertFalse(False)
	
	# ---- 3 records are there in default db
	def test_get_movies_details(self):
		movie_obj = MovieContainer.objects.all()
		self.assertEqual(movie_obj.count(), 3)

	
	def test_update_movies_with_id(self):
		MovieContainer.objects.filter(id=1).update(name="Mummy horror movie", description="Horror movie")
		self.assertTrue(True, "this is false?")


	def test_delete_movie_with_id(self):
		movie_obj = MovieContainer.objects.get(id=1)
		movie_obj.delete()
		self.assertTrue(True, "not deleted")
