from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import User, Base, Category, Movie
 
engine = create_engine('sqlite:///movies_database.db')
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
session = DBSession()

user1 = User(name = "Ilyes Benmesbah", email = "ilyes.benmesbah@gmail.com", picture = "https://cdn.vox-cdn.com/thumbor/8UiAfXafpk7IZu2HXfmT03Z_dxQ=/0x0:3368x3368/1520x1013/filters:focal(1188x715:1726x1253):format(webp)/cdn.vox-cdn.com/uploads/chorus_image/image/62994726/AJ_Finn_author_photo_color_photo_courtesy_of_the_author.0.jpg")
session.add(user1)
session.commit()

category1 = Category(name = "Action", user_id = 1, user = user1)
session.add(category1)
session.commit()

movie1 = Movie(name = "VENOM", description = "Investigative journalist Eddie Brock attempts a comeback following a scandal, but accidentally becomes the host of Venom, a violent, super powerful alien symbiote. Soon, he must rely on his newfound powers to protect the world from a shadowy organization looking for a symbiote of their own.", photo = "https://static.cinebel.be/img/movie/poster/full/1017484_fr_venom_1538651096153.jpg", trailer = "https://www.youtube.com/watch?v=u9Mv98Gr5pY", category_id = 1, user_id = 1, user = user1, category = category1)
session.add(movie1)
session.commit()

movie2 = Movie(name = "DESTROYER", description = "Erin Bell is an LAPD detective who, as a young cop, was placed undercover with a gang in the California desert with tragic results. When the leader of that gang re-emerges many years later, she must work her way back through the remaining members and into her own history with them to finally reckon with the demons that destroyed her past.", photo = "https://m.media-amazon.com/images/M/MV5BODI4MTI2OTAyMV5BMl5BanBnXkFtZTgwNjY3NDY1NjM@._V1_SY1000_CR0,0,675,1000_AL_.jpg", trailer = "https://www.youtube.com/watch?v=9g-j4wuEOPo", category_id = 1, user_id = 1, user = user1, category = category1)
session.add(movie2)
session.commit()

category2 = Category(name = "Adventure", user_id = 1, user = user1)
session.add(category2)
session.commit()

movie1 = Movie(name = "TOMB RAIDER", description = "Lara Croft, the fiercely independent daughter of a missing adventurer, must push herself beyond her limits when she finds herself on the island where her father disappeared.", photo = "https://images-na.ssl-images-amazon.com/images/I/81jPImw2QAL._SY445_.jpg", trailer = "https://www.youtube.com/watch?v=8ndhidEmUbI", category_id = 2, user_id = 1, user = user1, category = category2)
session.add(movie1)
session.commit()

movie2 = Movie(name = "JUMANJI: WELCOME TO THE JUNGLE", description = "The tables are turned as four teenagers are sucked into Jumanji's world - pitted against rhinos, black mambas and an endless variety of jungle traps and puzzles. To survive, they'll play as characters from the game.", photo = "http://fr.web.img6.acsta.net/pictures/17/11/07/13/40/0517792.jpg", trailer = "https://www.youtube.com/watch?v=2QKg5SZ_35I", category_id = 2, user_id = 1, user = user1, category = category2)
session.add(movie2)
session.commit()

category3 = Category(name = "Comedy", user_id = 1, user = user1)
session.add(category3)
session.commit()

movie1 = Movie(name = "THE BOSS BABY", description = "A story about how a new baby's arrival impacts a family, told from the point of view of a delightfully unreliable narrator, a wildly imaginative 7 year old named Tim.", photo = "http://www.movienewsletters.net/photos/189707R1.jpg", trailer = "https://www.youtube.com/watch?v=tquIfapGVqs", category_id = 3, user_id = 1, user = user1, category = category3)
session.add(movie1)
session.commit()

movie2 = Movie(name = "NIGHT SCHOOL", description = "Teddy Walker is a successful salesman whose life takes an unexpected turn when he accidentally blows up his place of employment. Forced to attend night school to get his GED, Teddy soon finds himself dealing with a group of misfit students, his former high school nemesis and a feisty teacher who doesn't think he's too bright.", photo = "http://fr.web.img6.acsta.net/pictures/18/08/01/00/52/3506056.jpg", trailer = "https://www.youtube.com/watch?v=t9QtXGirWf0", category_id = 3, user_id = 1, user = user1, category = category3)
session.add(movie2)
session.commit()