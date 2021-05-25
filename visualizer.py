import librosa
import numpy as np
import pygame
import cv2
import ffmpeg
import os


def make_video(screen):#screenshot

 
    _image_num = 0

 

    while True:

        _image_num += 1

        str_num = "000" + str(_image_num)
        file_name = "image" + str_num[-4:] + ".jpg"

        pygame.image.save(screen, file_name)
        yield

def clamp(min_value, max_value, value):

    if value < min_value:
        return min_value

    if value > max_value:
        return max_value

    return value


class AudioBar:

    def __init__(self, x, y, freq, color, width=50, min_height=10, max_height=100, min_decibel=-80, max_decibel=0):

        self.x, self.y, self.freq = x, y, freq

        self.color = color
 
        self.width, self.min_height, self.max_height = width, min_height, max_height

        self.height = min_height

        self.min_decibel, self.max_decibel = min_decibel, max_decibel

        self.__decibel_height_ratio = (self.max_height - self.min_height)/(self.max_decibel - self.min_decibel)

    def update(self, dt, decibel):

        desired_height = decibel * self.__decibel_height_ratio + self.max_height

        speed = (desired_height - self.height)/0.1

        self.height += speed * dt

        self.height = clamp(self.min_height, self.max_height, self.height)

    def render(self, screen):

        pygame.draw.rect(screen, self.color, (self.x, self.y + self.max_height - self.height, self.width, self.height))


filename = "tst.wav" #inputting audio

time_series, sample_rate = librosa.load(filename)  # getting information from the file

# getting a matrix which contains amplitude values according to frequency and time indexes
stft = np.abs(librosa.stft(time_series, hop_length=512, n_fft=2048*4))

spectrogram = librosa.amplitude_to_db(stft, ref=np.max)  # converting the matrix to decibel matrix

frequencies = librosa.core.fft_frequencies(n_fft=2048*4)  # getting an array of frequencies

# getting an array of time periodic
times = librosa.core.frames_to_time(np.arange(spectrogram.shape[1]), sr=sample_rate, hop_length=512, n_fft=2048*4)

time_index_ratio = len(times)/times[len(times) - 1]

frequencies_index_ratio = len(frequencies)/frequencies[len(frequencies)-1]


def get_decibel(target_time, freq):
    return spectrogram[int(freq * frequencies_index_ratio)][int(target_time * time_index_ratio)]


duration=librosa.get_duration(filename=filename) 

pygame.init()

infoObject = pygame.display.Info()

screen_w = int(infoObject.current_w/2.5)
screen_h = int(infoObject.current_w/2.5)

# Set up the drawing window
screen = pygame.display.set_mode([screen_w, screen_h])
save_screen = make_video(screen)
video = True 
bars = []


frequencies = np.arange(100, 8000, 100)

r = len(frequencies)


width = screen_w/r


x = (screen_w - width*r)/2

for c in frequencies:
    bars.append(AudioBar(x, 300, c, (255, 0, 0), max_height=400, width=width))
    x += width

t = pygame.time.get_ticks()
getTicksLastFrame = t

pygame.mixer.music.load(filename)
pygame.mixer.music.play(0)
k = 0
float(k)



print(duration)
while k<= duration:
    running=True
    while running == True:    
        if k <= duration: 
            t = pygame.time.get_ticks()
            deltaTime = (t - getTicksLastFrame) / 1000.0
            getTicksLastFrame = t

    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
           

            screen.fill((0, 0, 0))

            for b in bars:
                b.update(deltaTime, get_decibel(pygame.mixer.music.get_pos()/1000.0, b.freq))
                b.render(screen)

            pygame.display.flip()

             
            if video:

                next(save_screen)  

    
                print("PROCESSING")
            k = k+0.00699999999
        else:
            break         

pygame.display.quit()
pygame.quit()
#creating video from images
image_folder = '/home/adith/test'
video_name = 'pre.avi'

images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(video_name, 0, 1 ,(width,height))

for image in images:
    video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()
#combining video and input audio
video = ffmpeg.input('pre.avi')
audio = ffmpeg.input('tst.wav')
out = ffmpeg.output(video, audio,'output_video.mp4')
out.run()

#deleting the images

directory = "/home/adith/test"

files_in_directory = os.listdir(directory)
filtered_files = [file for file in files_in_directory if file.endswith(".jpg")]

for file in filtered_files:
	path_to_file = os.path.join(directory, file)
	os.remove(path_to_file)


os.remove('/home/adith/test/pre.avi')
