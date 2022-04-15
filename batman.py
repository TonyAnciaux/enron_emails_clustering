from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt #to display our wordcloud
from PIL import Image #to load our image
import numpy as np #to get the color of our image
from data.model import topics_union, topics

text = dict([value for topic in topics_union for value in topic])


bnw_mask = np.array(Image.open('batman.png'))

# wc1 = WordCloud(background_color = 'white',
#                 mask = bnw_mask,
#                 max_words = 500,
#                 collocations=False,
#                 contour_width = 2,
#                 contour_color = 'black')
# wc1.generate_from_frequencies(text)
# image_colors = ImageColorGenerator(bnw_mask)
# wc1.recolor(color_func = image_colors)
# plt.imshow(wc1, interpolation = 'bilinear')
# plt.axis('off')
# wc1.to_file("bat.png")

for idx, top in topics:

    wc1 = WordCloud(background_color = 'white',
                    mask = bnw_mask,
                    max_words = 500,
                    collocations=False,
                    contour_width = 2,
                    contour_color = 'black')
    wc1.generate_from_frequencies(dict(top))
    image_colors = ImageColorGenerator(bnw_mask)
    wc1.recolor(color_func = image_colors)
    plt.imshow(wc1, interpolation = 'bilinear')
    plt.axis('off')
    wc1.to_file(f"bat_topic_{idx}.png")
