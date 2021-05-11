# from datetime import datetime
# from webdriver_manager.chrome import ChromeDriverManager
# from PIL import Image

from mathFunctions import getRegression

x = [1,2,3,4,5,6,7,8,9,10]
y = [3,5,2,8,9,10,6,8,3,6]
class yes:
    X, Y = 0, 0

man = []
for i in range(len(x)):
    bruh = yes()
    bruh.X = x[i]
    bruh.Y = y[i]
    man.append(bruh)

a, b = getRegression(man)
print(a,b)
