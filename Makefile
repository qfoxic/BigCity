init:
	workon bigcity 

run:
	./manage.py runserver 127.0.0.1:8001

test:
	./manage.py test

generate_data:
	./manage.py test tests.test_advert.createTestData
