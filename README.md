## Jemma
Jemma Australia is the first online service that connects customers and tradies while also offering financial protection, better work/life balance, automated scheduling and much more.

There are two kinds of accounts of this website, which are Tradie Account and Customer Account. Tradies can set up their work types (if the work type requires related qualifications, they will need to upload their qualifications) and available time. Customers are able to search available tradies by selecting the work type and location. Once a tradie is selected by the customer, the customer needs to send a quote with descriptions of the work to the tradie, then the tradie will see the quote on their dashboard. They can choose to accept or decline the quote.

This project is based on Python, using Django framework. The static html pages were developed by bootstrap, and were saved in 'templetes' directory. Database models were implemented in 'Home_app/models.py'. Back-end functions were implemented in Home_app/views.py. In Jemma/Encrypt.py, it implemented an AES algorithm for the encryption of user information. For security reason, the encryption key and the database connection information are saved in a local file named 'django_db.conf', which is not added to the git repo.

The demo of this website can be viewed on http://13.55.162.121/