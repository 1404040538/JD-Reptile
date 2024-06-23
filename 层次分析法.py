import numpy as np


def var():
    global message
    global goods_list
    global my_list
    global id_list
    global my_price
    global my_comment
    message = []
    goods_list = []
    my_list = []
    id_list = []
    my_price = []
    my_comment = []


def consistency():
    A = np.array([[1, 4 / 6],
                  [6 / 4, 1]])

    n = A.shape[0]

    eig_val, eig_vec = np.linalg.eig(A)
    Max_eig = max(eig_val)

    CI = (Max_eig - n) / (n - 1)
    RI = [0, 0.0001, 0.52, 0.89, 1.12, 1.26, 1.36, 1.41, 1.46, 1.49, 1.52, 1.54, 1.56, 1.58, 1.59]

    CR = CI / RI[n - 1]
    a = f"一致性指标CI={CI}"
    b = f"一致性比例RI={RI}"
    message.append(a)
    message.append(b)

    if CR < 0.10:
        c = "因为CR<0.10，所以判断该矩阵A的一致性检验可以接受"
        print(c)
    else:
        d = "因为CR>=0.10，请重新确定"
        print(d)



def target():
    f = open("./京东手机数据.txt", 'r', encoding='utf-8')
    for i in f.readlines():
        i = i.split()
        try:
            a = float(i[0])
            b = float(i[1])
            id = i[2]
            list1 = [a, b]
            my_price.append(a)
            my_comment.append(b)
            my_list.append(list1)
            id_list.append(id)
        except Exception as e:
            e = "数值存在缺陷，剔除此行数据"
            print(e)
            message.append(e)


    weights = np.array([0.4, 0.6])
    my_array = np.array(my_list)

    my_array[:, 0] = my_array[:, 0] / my_array[:, 0].sum()
    my_array[:, 1] = my_array[:, 1] / my_array[:, 1].sum()

    my_array = my_array * weights

    global scores
    scores = np.sum(my_array,axis=1)



def file():
    open("./得分.txt", "w", encoding="utf-8")
    for i in range(len(scores)):
        with open("./得分.txt", "a", encoding="utf-8") as fp:
            fp.write(f"{scores[i]}\t\t{my_price[i]}\t\t{my_comment[i]}\t\t{id_list[i]}\n")

    with open('./得分.txt', 'r', encoding='utf-8') as fp:
        messages = []
        for line in fp:
            messages.append(line.split())

    prices = []
    for message in messages:
        prices.append(float(message[0]))

    names = []
    for message in messages:
        names.append(message[3])

    sorted_messages = sorted(zip(prices, names, my_price, my_comment), key=lambda x: x[0], reverse=True)
    global goods_list
    goods_list = sorted_messages[0:10]

    with open('./得分2.txt', 'w', encoding='utf-8') as outfile:
        for score, name, price, comment in sorted_messages:
            outfile.write(f"{score}\t\t{price}\t\t\t{comment}\t\t\t{name}\n")

def run():
    var()
    consistency()
    target()
    file()
    return message,goods_list


if __name__ == '__main__':
    var()
    consistency()
    target()
    file()
