import boto3 
import os
from matplotlib import pyplot as plt
import numpy as np

# this code works for one person images only

def emotion_encoder(emotion, dict, list):
    list.append(dict.get(emotion))

def get_emotions(photo, client):
    with open(photo, 'rb') as image:
        response = client.detect_faces(Image={'Bytes': image.read()}, Attributes=['ALL'])
        print(' - Requested face detection and analysis')

    if len(response) > 0:
        print(' - A face was detected')


    for item in response.get('FaceDetails'):
        face_emotion_confidence = 0
        face_emotion = None
        for emotion in item.get('Emotions'):
            if emotion.get('Confidence') >= face_emotion_confidence:
                face_emotion_confidence = emotion['Confidence']
                face_emotion = emotion.get('Type')
        return face_emotion, face_emotion_confidence
        

def plot_emotions(list):
    y = np.arange(len(list))
    # emotions trought time
    plt.style.use('seaborn-whitegrid')
    plt.plot(y, list, color='blue')
    # plt.show()
    y = np.arange(9)
    emotion_counter = [list.count(1), list.count(2), list.count(3), list.count(4),
                        list.count(5), list.count(6), list.count(7), list.count(8), list.count(9)]
    plt.bar(y, emotion_counter)
    plt.show()

def main():
    client = boto3.client('rekognition')
    
    folder_dir = './my_images'

    emotion_dictionary = {'HAPPY': 1,  'SAD': 6, 'ANGRY': 8,'CONFUSED': 5, 
                            'DISGUSTED': 7, 'SURPRISED': 2, 'CALM': 3, 'UNKNOWN': 4, 'FEAR': 9}

    list_of_emotions = []

    for image in os.listdir(folder_dir):
        if image.endswith('.jpg') or image.endswith('.jpeg') or image.endswith('.png'):
            print('- Requesting analysis for: ' + image)
            face_emotion, face_emotion_confidence = get_emotions(str(folder_dir + '/' + image), client)
            print(' - RESULTS', end='\n\n')
            print('\tMost probable emotion: ' + face_emotion)
            print('\tConfidence: ' + str(face_emotion_confidence), end='\n\n')
            emotion_encoder(face_emotion, emotion_dictionary, list_of_emotions)

    print('RESULTANT LIST OF EMOTIONS: ', end='')
    print(list_of_emotions)
    plot_emotions(list_of_emotions)
    

if __name__ == "__main__":
    main()

