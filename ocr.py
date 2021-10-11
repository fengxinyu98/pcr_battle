from cnocr import CnOcr


def ocr(screen):
    #image = Image.fromarray(cv2.cvtColor(screen,cv2.COLOR_BGR2RGB))
    ocr = CnOcr()
    res = ocr.ocr_for_single_line(screen)
    rank = 0
    print(res)
    if res[1] > 0.5:
        if res[0][-1] == '位':
            for i in range(len(res[0])-1):
                if res[0][i].isdigit():
                    rank *= 10
                    rank += int(res[0][i])
                else:
                    return 999
            return rank
        else:
            return 999
    else:
        return 999
