# How to run a project on your local machine?
1. Install Docker https://docs.docker.com/engine/install/
2. Rename example to .env
3. Run docker-compose up --build pgadmin
4. Open http://localhost:5050/browser/ with password: pass and create DB events_db with password: pass
5. Run docker-compose up --build If you have error /data/db: permission denied failed to solve run: sudo chmod -R 777 ./data/db
6. Run migrations by docker exec -it web_events python3 manage.py migrate
7. Run docker exec -it web_events python3 manage.py runscript load_db to create test data
8. Run to create admin user docker exec -it web_events python3 manage.py createsuperuser if needed
9. Register new users using http://localhost/auth/registration/ if needed
10. Use http://localhost/api/events/ to look list events
11. Use http://localhost/api/events/<int:pk> to look some event
12. Send post to http://localhost/api/events/<int:pk> for register into event
