#参考文献
# [1] https://github.com/antimatter15/rgb-lab (Lab値からxyz値に変換する奴の元ネタ(JavaScript))
# [2] http://www.brucelindbloom.com/index.html?Eqn_Lab_to_XYZ.html (Lab値からXYZに変換)
# [3] http://www.brucelindbloom.com/index.html?Eqn_Lab_to_XYZ.html (XYZからRGBに変換)
# [4] https://www.w3.org/Graphics/Color/srgb                       ((XYZからRGBに変換_学会)
# [5] http://imagexcel.seesaa.net/article/435092808.html　(XYZからRGBに変換<日本語>)
#

import numpy as np



def lab2rgb(lab):

    y = (lab[0] + 16) / 116.0 #OK
    x = y + (lab[1] / 500.0)  #OK
    z = y - (lab[2] / 200.0)  #OK 


    # lluminant D65を基準といたWhite point　を採用する。※CASMATCHがD65光源
    # どの光源のホワイトスタンダートを採用するかで、かける値が変わる。
    # https://en.wikipedia.org/wiki/Illuminant_D65 (Illuminant D65)
    # https://en.wikipedia.org/wiki/White_point (White point)
    # https://jp.mathworks.com/help/images/ref/xyz2lab.html (D65のホワイトスタンダード)

    if (x * x * x > 0.008856): #OK
        X = 0.9504*(x * x * x) #OK
    else:
        X = 0.9504*(((116*x) - 16)/903.3) #OK 

    if (lab[0]) > ((903.3)*(0.008856)): #OK
        Y =  1.0000 * (y * y * y) #OK
    else:
        Y = 1.0000 * ((lab[0]) / 903.3) #OK

    if (z * z * z > 0.008856): #OK
        Z = 1.08883 * (z * z * z) #OK
    else:
        Z = 1.08883 *(((116*z) - 16)/903.3) #OK

    #XYZをRGBに変換する時に行う行列
    XYZ_Matrices = np.array([[3.2410,-1.5374,-0.4986],[-0.9692,1.8760,0.0416],[0.0556,-0.2040,1.0570]])
    XYZ_numbers = np.array([X , Y , Z])

    R = 0
    G = 0
    B = 0

    #以下のfor文はarray配列から、RGBに代入するだけ、もう少しましなものを考えたい
    for j  in range(len(XYZ_numbers)):
        if j == 0:
            R = XYZ_numbers[j]
        if j == 1:
            G = XYZ_numbers[j]
        if j == 2:
            B = XYZ_numbers[j]
    


    if R <= 0.0031308:
        R = R * 12.92
    else:
        R = (1.055 * (R**(1/2.4))) - 0.055
    
    if G <= 0.0031308:
        G = G * 12.92
    else:
        G = (1.055 * (G**(1/2.4))) - 0.055

    if B <= 0.0031308:
        B = B * 12.92
    else:
        B = (1.055 * (B**(1/2.4))) - 0.055
    

    #浮動小数点演算で、値がかなり振れるので、min()で制御。実際には0~1の値しか取らない。
    return [min(1,R),min(1,G),min(1,B)],XYZ_numbers

print(lab2rgb([118.81,-18,112]))