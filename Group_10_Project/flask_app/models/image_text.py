from PIL import Image
from pytesseract import pytesseract

class Image_text:
    def __init__(self,image_path,total):
        self.image_path=image_path
        self.total=total
    @staticmethod
    def total_amount(image_path):
        #Define path to image
        path_to_image = image_path
        #Open image with PIL
        img = Image.open(path_to_image)

        #Extract text from image
        text = pytesseract.image_to_string(img)
        print(text)

        #Preparing Text data
        part1=(text.replace("\n"," ")).upper()
        part2=part1.split(" ")
        part3=(text.upper()).split("\n")
        price=""

        #Finding Total from image
        #Removing blanks values in list
        for a in part3:
            if a=='':
                part3.remove(a)
        #Splitting each list attribute int
        for b in part3:
                c=b.split(" ")
                x=-1
                #Finding 
                print (c)
                for d in c:
                    x+=1
                    if "SUB" in c:
                        continue
                    elif "TAX" in d:
                        continue
                    elif "TOTAL" or ("USD"and"TOTAL") in d:
                        for e in range(len(c)):
                            f=c[e].replace(",",".")
                            try:
                                if float(f)>0:
                                    price = f
                                    break
                            except:
                                g=f.replace("$","")
                                try:
                                    if float(g)>0:
                                        price = g
                                        break
                                except:
                                    continue
        if price=="":
            print("Image unclear.Resubmit more clear image")
        total=price
        return total