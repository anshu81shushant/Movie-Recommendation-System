import gdown

url = "https://drive.google.com/file/d/1O1bpd5atxVG8OSpjL5o4m_Kdz3VEGHaE/view?usp=sharing"
output = "movie_data.pkl"
gdown.download(url, output, quiet=False)