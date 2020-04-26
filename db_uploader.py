import os
import mysql.connector
import datetime
import db_credentials

delete_after_save = True
images_folder = "not-in-db"
def send_images_to_db():
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(THIS_FOLDER, images_folder)

    images = os.listdir(path)

    for image in images:
        send_image(os.path.join(path, image))

def send_image(dir):
    creation_time = datetime.datetime.fromtimestamp(os.path.getmtime(dir))
    creation_time = creation_time.strftime("%Y-%m-%d %H:%M:%S")

    with open(dir, "rb") as file:
        binaryImage = file.read()

    try:
        connection = mysql.connector.connect(**db_credentials.config)
        if connection.is_connected():
            cursor = connection.cursor()
            query = """INSERT INTO images (time_taken, image)
                        VALUES (%s, %s)"""

            values = (creation_time, binaryImage)

            result = cursor.execute(query, values)
            connection.commit()
            print("Image successfully stored in the database")

            if (delete_after_save):
                os.remove(dir)
                print("Image deleted from local storage")


    except mysql.connector.Error as e:
        print("Error while uploading immage to database", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


if __name__ == "__main__":
    send_images_to_db()
