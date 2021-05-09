# Sheet-music-player
Web based application integrated with machine learning.Users can upload their sheet music (Image) and the application will convert it into editable notes and then into audio via ML models.The app consists of a complete musical playground where users can upload and store their musical compositions ,play, update, delete and share the songs with other users.There is a seperate section which displays the user's favourite compositions. The songs have been clustered based on genre, users can follow / unfollow their favourite artists and connected users can view and play each other's compositions.Users can also share their music via codes or email. 

To run this project

1.FIRST TIME ( or in case of changes in database )
    1.Git clone / compress folder
    2.Open terminal in this directory and enter cd app
    3.Enter the command "python3 manage.py makemigrations"
    4.Enter the command "python3 manage.py migrate"
    3.Enter the command "python3 manage.py runserver"
    Website will be running on local host port 8080

2.Already existing 
    2.Open terminal in this directory and enter cd app
    3.Enter the command "python3 manage.py runserver"
    Website will be running on local host port 8080

Note : Use only python in all commands instead of python3 if by default your system uses python 3.


